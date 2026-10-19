from __future__ import annotations

import cv2
import numpy as np

from .face import Face

MIN_EYE_DISTANCE_PX = 60
MAX_YAW_DEG = 10.0
MAX_CHEEK_ASYMMETRY = 0.12
MIN_SHARPNESS = 60.0
BRIGHTNESS_RANGE = (70, 215)
MAX_LIGHT_IMBALANCE = 28


def check_input(image_rgb: np.ndarray, face: Face) -> list[str]:
    """检查原图质量，返回提示信息；空列表表示没有发现问题。"""
    warnings: list[str] = []

    if face.eye_distance < MIN_EYE_DISTANCE_PX:
        warnings.append(
            f"人脸偏小（眼距 {face.eye_distance:.0f}px），输出可能发糊，建议靠近一些拍摄或使用更高清的原图。"
        )

    if abs(face.yaw_deg) > MAX_YAW_DEG or abs(face.cheek_asymmetry) > MAX_CHEEK_ASYMMETRY:
        warnings.append(f"脸部可能有左右偏转（约 {abs(face.yaw_deg):.0f}°），证件照要求正脸平视镜头。")

    x, y, w, h = (int(round(v)) for v in face.box)
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, image_rgb.shape[1]), min(y + h, image_rgb.shape[0])
    region = image_rgb[y0:y1, x0:x1]
    if region.size == 0:
        return warnings

    gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    norm = cv2.resize(gray, (256, round(256 * gray.shape[0] / max(gray.shape[1], 1))))
    sharpness = cv2.Laplacian(norm, cv2.CV_64F).var()
    if sharpness < MIN_SHARPNESS:
        warnings.append(f"面部清晰度偏低（{sharpness:.0f}），可能存在对焦不准或抖动。")

    brightness = float(gray.mean())
    if brightness < BRIGHTNESS_RANGE[0]:
        warnings.append(f"面部偏暗（亮度 {brightness:.0f}），建议在光线充足处拍摄。")
    elif brightness > BRIGHTNESS_RANGE[1]:
        warnings.append(f"面部过亮（亮度 {brightness:.0f}），可能过曝。")

    mid = gray.shape[1] // 2
    if mid > 0:
        diff = abs(float(gray[:, :mid].mean()) - float(gray[:, mid:].mean()))
        if diff > MAX_LIGHT_IMBALANCE:
            warnings.append("面部左右明暗差异较大（侧光），审核可能要求光线均匀。")

    return warnings
