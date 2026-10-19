from __future__ import annotations

import math
import os
import threading
from dataclasses import dataclass, replace

import cv2
import numpy as np

from .config import MODELS_DIR

os.environ.setdefault("GLOG_minloglevel", "2")

YUNET_PATH = MODELS_DIR / "face_detection_yunet_2023mar.onnx"
LANDMARKER_PATH = MODELS_DIR / "face_landmarker.task"

# MediaPipe Face Mesh 关键点编号
IRIS_A, IRIS_B = 468, 473
NOSE_TIP = 1
CHIN = 152
CHEEK_A, CHEEK_B = 234, 454

Box = tuple[float, float, float, float]  # x, y, w, h


@dataclass
class Face:
    points: np.ndarray  # (478, 2)，原图像素坐标
    yaw_deg: float  # 左右转头角度，正脸约为 0

    def _p(self, i: int) -> tuple[float, float]:
        return float(self.points[i, 0]), float(self.points[i, 1])

    @property
    def eye_a(self) -> tuple[float, float]:
        """画面左侧的眼睛（瞳孔中心）。"""
        a, b = self._p(IRIS_A), self._p(IRIS_B)
        return a if a[0] <= b[0] else b

    @property
    def eye_b(self) -> tuple[float, float]:
        a, b = self._p(IRIS_A), self._p(IRIS_B)
        return b if a[0] <= b[0] else a

    @property
    def nose(self) -> tuple[float, float]:
        return self._p(NOSE_TIP)

    @property
    def box(self) -> Box:
        x0, y0 = self.points[:468].min(axis=0)
        x1, y1 = self.points[:468].max(axis=0)
        return float(x0), float(y0), float(x1 - x0), float(y1 - y0)

    @property
    def area(self) -> float:
        _, _, w, h = self.box
        return w * h

    @property
    def center_x(self) -> float:
        return (self.eye_a[0] + self.eye_b[0]) / 2

    @property
    def eye_y(self) -> float:
        return (self.eye_a[1] + self.eye_b[1]) / 2

    @property
    def eye_distance(self) -> float:
        return math.dist(self.eye_a, self.eye_b)

    @property
    def chin_y(self) -> float:
        return float(self.points[CHIN, 1])

    @property
    def roll_deg(self) -> float:
        (ax, ay), (bx, by) = self.eye_a, self.eye_b
        return math.degrees(math.atan2(by - ay, bx - ax))

    @property
    def cheek_asymmetry(self) -> float:
        """鼻尖到两侧脸颊距离的不对称度，正脸约为 0。"""
        da = math.dist(self.nose, self._p(CHEEK_A))
        db = math.dist(self.nose, self._p(CHEEK_B))
        return (da - db) / max(da + db, 1e-6)

    def transformed(self, matrix: np.ndarray) -> Face:
        pts = np.hstack([self.points, np.ones((len(self.points), 1))]) @ matrix.T
        return replace(self, points=pts.astype(np.float64))


class FaceDetector:
    """YuNet 负责找人脸和数人数，MediaPipe Face Landmarker 负责精确关键点。"""

    def __init__(self, score_threshold: float = 0.7):
        for path in (YUNET_PATH, LANDMARKER_PATH):
            if not path.exists():
                raise FileNotFoundError(f"缺少人脸模型：{path}")
        self._yunet = cv2.FaceDetectorYN.create(str(YUNET_PATH), "", (320, 320), score_threshold, 0.3, 5000)

        from mediapipe.tasks.python import BaseOptions, vision

        options = vision.FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(LANDMARKER_PATH)),
            num_faces=4,
            output_facial_transformation_matrixes=True,
            min_face_detection_confidence=0.4,
        )
        self._landmarker = vision.FaceLandmarker.create_from_options(options)
        self._lock = threading.Lock()

    def detect_boxes(self, image_rgb: np.ndarray) -> list[Box]:
        h, w = image_rgb.shape[:2]
        scale = min(1.0, 1280 / max(h, w))
        bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        if scale < 1.0:
            bgr = cv2.resize(bgr, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA)
        with self._lock:
            self._yunet.setInputSize((bgr.shape[1], bgr.shape[0]))
            _, raw = self._yunet.detect(bgr)
        if raw is None:
            return []
        boxes = [tuple(float(v) / scale for v in row[:4]) for row in raw]
        return sorted(boxes, key=lambda b: b[2] * b[3], reverse=True)  # type: ignore[return-value]

    def _run_landmarker(self, image_rgb: np.ndarray) -> list[Face]:
        import mediapipe as mp

        h, w = image_rgb.shape[:2]
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(image_rgb))
        with self._lock:
            result = self._landmarker.detect(mp_image)
        faces = []
        for i, lms in enumerate(result.face_landmarks):
            pts = np.array([[p.x * w, p.y * h] for p in lms], dtype=np.float64)
            yaw = 0.0
            if result.facial_transformation_matrixes:
                r = np.asarray(result.facial_transformation_matrixes[i])[:3, :3]
                yaw = math.degrees(math.atan2(-r[2, 0], math.hypot(r[2, 1], r[2, 2])))
            faces.append(Face(points=pts, yaw_deg=yaw))
        return faces

    def landmarks(self, image_rgb: np.ndarray, box: Box | None = None) -> Face | None:
        """在人脸框附近裁剪后提取关键点；不给框时在整张图上找最大的人脸。"""
        if box is None:
            h, w = image_rgb.shape[:2]
            scale = min(1.0, 1280 / max(h, w))
            small = cv2.resize(image_rgb, (round(w * scale), round(h * scale))) if scale < 1 else image_rgb
            faces = self._run_landmarker(small)
            if not faces:
                return None
            face = max(faces, key=lambda f: f.area)
            return replace(face, points=face.points / scale)

        x, y, bw, bh = box
        side = max(bw, bh) * 2.2
        cx, cy = x + bw / 2, y + bh / 2
        out = int(min(768, max(256, side)))
        k = out / side
        m = np.array([[k, 0, -(cx - side / 2) * k], [0, k, -(cy - side / 2) * k]], dtype=np.float64)
        crop = cv2.warpAffine(image_rgb, m, (out, out), flags=cv2.INTER_AREA if k < 1 else cv2.INTER_LINEAR,
                              borderMode=cv2.BORDER_REPLICATE)
        faces = self._run_landmarker(crop)
        if not faces:
            return None
        center = np.array([out / 2, out / 2])
        face = min(faces, key=lambda f: np.linalg.norm(f.points[:468].mean(axis=0) - center))
        inv = cv2.invertAffineTransform(m)
        return face.transformed(inv)
