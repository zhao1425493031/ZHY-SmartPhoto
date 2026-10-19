from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import cv2
import numpy as np
from PIL import Image, ImageOps

from . import matting
from .config import Spec
from .face import Face, FaceDetector
from .quality import check_input

WORK_MAX_SIDE = 2000
DEFAULT_TOP_MARGIN = 0.09


class PhotoError(Exception):
    """原图无法制作证件照（如没有人脸），消息直接展示给用户。"""


@dataclass
class Prepared:
    image: np.ndarray  # uint8 RGB，已摆正
    alpha: np.ndarray  # float32 0～1
    foreground: np.ndarray  # float32 RGB 0～1，已去除原背景色污染
    face: Face
    head_top_y: float
    model: str
    warnings: list[str] = field(default_factory=list)
    roll_deg: float = 0.0


@dataclass
class Adjust:
    zoom: float = 1.0  # >1 人物变大
    offset_x: float = 0.0  # 正值人物右移，单位为照片宽度比例
    offset_y: float = 0.0  # 正值人物下移，单位为照片高度比例


@dataclass
class Layout:
    """人物在输出照片中的位置，单位为输出像素。"""

    head_top: float
    chin: float
    eye_y: float
    center_x: float
    width: int
    height: int

    @property
    def head_ratio(self) -> float:
        return (self.chin - self.head_top) / self.height

    @property
    def top_margin_ratio(self) -> float:
        return self.head_top / self.height

    @property
    def eye_from_bottom_ratio(self) -> float:
        return (self.height - self.eye_y) / self.height

    @property
    def center_offset_ratio(self) -> float:
        return (self.center_x - self.width / 2) / self.width


@dataclass
class Rendered:
    image: Image.Image  # 最终证件照，RGB，尺寸等于规格
    layout: Layout
    warnings: list[str] = field(default_factory=list)


_detector: FaceDetector | None = None


def _get_detector() -> FaceDetector:
    global _detector
    if _detector is None:
        _detector = FaceDetector()
    return _detector


def load_image(img: Image.Image) -> np.ndarray:
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
    img = img.convert("RGB")
    scale = min(1.0, WORK_MAX_SIDE / max(img.size))
    if scale < 1.0:
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    return np.asarray(img).copy()


def _rotate(image: np.ndarray, angle: float, center: tuple[float, float]) -> tuple[np.ndarray, np.ndarray]:
    h, w = image.shape[:2]
    m = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos, sin = abs(m[0, 0]), abs(m[0, 1])
    nw, nh = int(math.ceil(h * sin + w * cos)), int(math.ceil(h * cos + w * sin))
    m[0, 2] += nw / 2 - center[0]
    m[1, 2] += nh / 2 - center[1]
    rotated = cv2.warpAffine(image, m, (nw, nh), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated, m


def _find_head_top(alpha: np.ndarray, face: Face) -> tuple[float, bool]:
    """从抠图遮罩里找头顶（含头发）的位置，返回 (y, 是否被画面上边截断)。"""
    x, y, w, _ = face.box
    x0 = int(max(0, x + w * 0.2))
    x1 = int(min(alpha.shape[1], x + w * 0.8))
    y_limit = int(max(1, min(alpha.shape[0], face.eye_y)))
    column = alpha[:y_limit, x0:x1].max(axis=1)
    rows = np.nonzero(column > 0.5)[0]
    if rows.size == 0:
        return float(y), False
    top = int(rows[0])
    if top == 0:
        return 0.0, True
    # 在 0.5 阈值附近做亚像素插值
    a0, a1 = column[top - 1], column[top]
    frac = (0.5 - a0) / max(a1 - a0, 1e-6)
    return float(top - 1 + frac), False


def prepare(
    img: Image.Image,
    model: str = matting.DEFAULT_MODEL,
    progress: Callable[[str, float], None] | None = None,
) -> Prepared:
    """progress(stage, value)：stage 依次为 load / face / matting / refine / done。"""
    report = progress or (lambda stage, value: None)
    report("load", 0.03)
    image = load_image(img)
    report("face", 0.12)
    detector = _get_detector()
    boxes = detector.detect_boxes(image)
    if len(boxes) > 1 and boxes[1][2] * boxes[1][3] > boxes[0][2] * boxes[0][3] * 0.25:
        raise PhotoError(f"检测到 {len(boxes)} 张人脸，证件照只能有一个人，请裁掉其他人后再试。")
    face = detector.landmarks(image, boxes[0] if boxes else None)
    if face is None:
        raise PhotoError("没有检测到人脸。请使用正脸、光线充足、脸部无遮挡的照片。")

    warnings: list[str] = []
    if len(boxes) > 1:
        warnings.append("背景里还有较小的人脸，已自动忽略，请确认抠图结果中没有残留。")

    roll = face.roll_deg
    if abs(roll) > 0.3:
        image, m = _rotate(image, roll, (face.center_x, face.eye_y))
        face = face.transformed(m)
    if abs(roll) > 8:
        warnings.append(f"原图头部倾斜约 {abs(roll):.1f}°，已自动摆正，请确认效果自然。")

    warnings.extend(check_input(image, face))

    report("matting", 0.3)
    alpha = matting.estimate_alpha(image, model)
    alpha = matting.keep_subject(alpha, (face.center_x, (face.eye_y + face.chin_y) / 2))
    head_top, cut = _find_head_top(alpha, face)
    if cut:
        warnings.append("原图头顶被画面截断，头部比例无法准确计算，请使用头顶上方留有空间的照片。")
    if head_top >= face.box[1]:
        head_top = face.box[1] - face.box[3] * 0.25
        warnings.append("抠图没有识别到头发区域，头顶位置为估算值，请仔细核对预览参考线。")

    report("refine", 0.85)
    foreground = matting.estimate_foreground(image, alpha)
    report("done", 1.0)
    return Prepared(
        image=image,
        alpha=alpha,
        foreground=foreground,
        face=face,
        head_top_y=head_top,
        model=model,
        warnings=warnings,
        roll_deg=roll,
    )


def _crop_geometry(prep: Prepared, spec: Spec, adjust: Adjust) -> tuple[float, float, float]:
    """返回 (scale, left, top)：输出像素 = (源像素 - left/top) * scale。"""
    W, H = spec.size_px
    face = prep.face
    head_src = max(face.chin_y - prep.head_top_y, 1.0)
    target_ratio = sum(spec.head_height_ratio) / 2 * adjust.zoom
    scale = target_ratio * H / head_src
    crop_w, crop_h = W / scale, H / scale

    left = face.center_x - crop_w / 2 - adjust.offset_x * crop_w
    if spec.top_margin_ratio:
        top = prep.head_top_y - sum(spec.top_margin_ratio) / 2 * crop_h
    elif spec.eye_from_bottom_ratio:
        eye_from_top = 1 - sum(spec.eye_from_bottom_ratio) / 2
        top = face.eye_y - eye_from_top * crop_h
    else:
        top = prep.head_top_y - DEFAULT_TOP_MARGIN * crop_h
    top -= adjust.offset_y * crop_h
    return scale, left, top


def _warp(src: np.ndarray, scale: float, left: float, top: float, size: tuple[int, int]) -> np.ndarray:
    W, H = size
    if scale < 1.0:
        ss = int(min(4, max(1, round(1 / scale))))
        s = scale * ss
        m = np.array([[s, 0, -left * s], [0, s, -top * s]], dtype=np.float64)
        big = cv2.warpAffine(src, m, (W * ss, H * ss), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        return cv2.resize(big, (W, H), interpolation=cv2.INTER_AREA)
    m = np.array([[scale, 0, -left * scale], [0, scale, -top * scale]], dtype=np.float64)
    return cv2.warpAffine(src, m, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def _background(size: tuple[int, int], rgb: tuple[int, int, int], gradient: bool) -> np.ndarray:
    W, H = size
    color = np.array(rgb, dtype=np.float32) / 255.0
    if not gradient:
        return np.broadcast_to(color, (H, W, 3)).copy()
    light = color + (1.0 - color) * 0.55
    t = np.linspace(0.0, 1.0, H, dtype=np.float32)[:, None, None]
    return np.broadcast_to(color * (1 - t) + light * t, (H, W, 3)).copy()


def _edge_warnings(prep: Prepared, scale: float, left: float, top: float, spec: Spec) -> list[str]:
    h, w = prep.alpha.shape
    W, H = spec.size_px
    right, bottom = left + W / scale, top + H / scale
    out: list[str] = []
    if top < 0 and prep.alpha[0, :].mean() > 0.02:
        out.append("照片上方超出原图范围，已自动延伸填充。")
    if bottom > h and prep.alpha[-1, :].mean() > 0.02:
        out.append("照片下方超出原图范围（肩部不够），已自动延伸填充，建议使用拍到胸口以下的原图。")
    if left < 0 and prep.alpha[:, 0].mean() > 0.02:
        out.append("照片左侧超出原图范围，人物被截断处已自动延伸填充。")
    if right > w and prep.alpha[:, -1].mean() > 0.02:
        out.append("照片右侧超出原图范围，人物被截断处已自动延伸填充。")
    if scale > 1.3:
        out.append(f"原图分辨率不足，人像被放大了 {scale:.1f} 倍，可能不够清晰。")
    return out


def render(
    prep: Prepared,
    spec: Spec,
    rgb: tuple[int, int, int],
    adjust: Adjust | None = None,
    gradient: bool = False,
) -> Rendered:
    adjust = adjust or Adjust()
    size = spec.size_px
    scale, left, top = _crop_geometry(prep, spec, adjust)

    fg = _warp(prep.foreground, scale, left, top, size)
    alpha = _warp(prep.alpha, scale, left, top, size)[..., None]
    alpha = np.clip(alpha, 0.0, 1.0)
    bg = _background(size, rgb, gradient)
    out = fg * alpha + bg * (1.0 - alpha)
    image = Image.fromarray(np.clip(out * 255.0 + 0.5, 0, 255).astype(np.uint8), "RGB")

    face = prep.face
    layout = Layout(
        head_top=(prep.head_top_y - top) * scale,
        chin=(face.chin_y - top) * scale,
        eye_y=(face.eye_y - top) * scale,
        center_x=(face.center_x - left) * scale,
        width=size[0],
        height=size[1],
    )
    return Rendered(image=image, layout=layout, warnings=_edge_warnings(prep, scale, left, top, spec))
