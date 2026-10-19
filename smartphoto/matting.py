from __future__ import annotations

import threading
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image

from .config import MODELS_DIR

@dataclass(frozen=True)
class ModelInfo:
    label: str
    desc: str
    eta_seconds: float  # 4 核笔记本 CPU 上的参考耗时


MODELS: dict[str, ModelInfo] = {
    "birefnet-general-lite": ModelInfo("精细 · BiRefNet-lite", "边缘最干净，推荐正式使用", 30),
    "hivision_modnet": ModelInfo("快速 · MODNet-Hivision", "约 1 秒，适合纯色背景的原图", 2),
    "modnet": ModelInfo("快速 · MODNet", "约 1 秒，发丝边缘偏柔和", 2),
    "birefnet-portrait": ModelInfo("极致 · BiRefNet 完整版", "需 8GB 以上空闲内存，CPU 需数分钟", 240),
}
DEFAULT_MODEL = "birefnet-general-lite"

MODNET_FILES = {
    "modnet": "modnet_photographic_portrait_matting.onnx",
    "hivision_modnet": "hivision_modnet.onnx",
}

_sessions: dict = {}
_lock = threading.Lock()


def _session(model: str):
    with _lock:
        if model not in _sessions:
            if model in MODNET_FILES:
                import onnxruntime as ort

                path = MODELS_DIR / MODNET_FILES[model]
                if not path.exists():
                    raise FileNotFoundError(f"缺少抠图模型：{path}")
                _sessions[model] = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
            else:
                from rembg import new_session

                _sessions[model] = new_session(model)
        return _sessions[model]


def _modnet(image_rgb: np.ndarray, model: str) -> np.ndarray:
    sess = _session(model)
    inp = sess.get_inputs()[0]
    h, w = image_rgb.shape[:2]
    if isinstance(inp.shape[2], int):
        th, tw = inp.shape[2], inp.shape[3]
    else:
        ref = 512
        k = ref / min(h, w) if max(h, w) < ref or min(h, w) > ref else 1.0
        th, tw = max(32, int(h * k) // 32 * 32), max(32, int(w * k) // 32 * 32)
    x = cv2.resize(image_rgb, (tw, th), interpolation=cv2.INTER_AREA).astype(np.float32)
    x = (x - 127.5) / 127.5
    x = x.transpose(2, 0, 1)[None]
    matte = sess.run(None, {inp.name: x})[0][0, 0]
    return cv2.resize(matte, (w, h), interpolation=cv2.INTER_LINEAR)


def estimate_alpha(image_rgb: np.ndarray, model: str = DEFAULT_MODEL) -> np.ndarray:
    """返回 float32 的 alpha 遮罩，取值 0～1，尺寸与输入一致。"""
    if model not in MODELS:
        raise ValueError(f"不支持的抠图模型：{model}")
    if model in MODNET_FILES:
        return np.clip(_modnet(image_rgb, model), 0.0, 1.0).astype(np.float32)

    from rembg import remove

    mask = remove(
        Image.fromarray(image_rgb),
        session=_session(model),
        only_mask=True,
        post_process_mask=False,
    )
    alpha = np.asarray(mask, dtype=np.float32) / 255.0
    if alpha.shape[:2] != image_rgb.shape[:2]:
        alpha = cv2.resize(alpha, (image_rgb.shape[1], image_rgb.shape[0]), interpolation=cv2.INTER_LINEAR)
    return alpha


def keep_subject(alpha: np.ndarray, seed: tuple[float, float]) -> np.ndarray:
    """只保留包含人脸的那块前景，去掉背景里误识别的零散区域。"""
    binary = (alpha > 0.1).astype(np.uint8)
    count, labels = cv2.connectedComponents(binary, connectivity=8)
    if count <= 2:
        return alpha
    sx = int(np.clip(seed[0], 0, alpha.shape[1] - 1))
    sy = int(np.clip(seed[1], 0, alpha.shape[0] - 1))
    label = labels[sy, sx]
    if label == 0:
        areas = np.bincount(labels.ravel())
        areas[0] = 0
        label = int(areas.argmax())
    subject = (labels == label).astype(np.uint8)
    # 外扩一圈，避免切掉阈值以下的细碎发丝
    radius = max(5, round(max(alpha.shape) * 0.01))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (radius * 2 + 1, radius * 2 + 1))
    keep = cv2.dilate(subject, kernel).astype(np.float32)
    return alpha * keep


def estimate_foreground(image_rgb: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """估计去除原背景色污染后的前景颜色，返回 float32 RGB，取值 0～1。"""
    img = image_rgb.astype(np.float64) / 255.0
    try:
        from pymatting import estimate_foreground_ml

        fg = estimate_foreground_ml(img, alpha.astype(np.float64))
    except Exception:
        fg = img
    return np.clip(fg, 0.0, 1.0).astype(np.float32)
