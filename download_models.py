"""下载缺失的模型文件，已存在的会跳过。start.bat 每次启动都会调用。"""
from __future__ import annotations

import sys
import urllib.request

from smartphoto.config import MODELS_DIR
from smartphoto.matting import DEFAULT_MODEL, MODNET_FILES

FILES = {
    "face_detection_yunet_2023mar.onnx": "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    "face_landmarker.task": "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task",
    "modnet_photographic_portrait_matting.onnx": "https://github.com/Zeyi-Lin/HivisionIDPhotos/releases/download/pretrained-model/modnet_photographic_portrait_matting.onnx",
    "hivision_modnet.onnx": "https://github.com/Zeyi-Lin/HivisionIDPhotos/releases/download/pretrained-model/hivision_modnet.onnx",
}


def _progress(name: str):
    def hook(blocks: int, block_size: int, total: int) -> None:
        if total > 0:
            pct = min(100, blocks * block_size * 100 // total)
            print(f"\r  {name}: {pct}%", end="", flush=True)

    return hook


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    MODELS_DIR.mkdir(exist_ok=True)
    ok = True
    for name, url in FILES.items():
        path = MODELS_DIR / name
        if path.exists() and path.stat().st_size > 0:
            continue
        print(f"下载模型 {name} ...")
        tmp = path.with_suffix(path.suffix + ".part")
        try:
            urllib.request.urlretrieve(url, tmp, _progress(name))
            tmp.replace(path)
            print()
        except Exception as e:  # noqa: BLE001
            ok = False
            tmp.unlink(missing_ok=True)
            print(f"\n  下载失败：{e}\n  可以手动下载 {url} 放到 {path}")

    if DEFAULT_MODEL not in MODNET_FILES:
        from rembg.sessions import sessions_class

        cls = next(c for c in sessions_class if c.name() == DEFAULT_MODEL)
        try:
            cls.download_models()
        except Exception as e:  # noqa: BLE001
            ok = False
            print(f"  默认抠图模型 {DEFAULT_MODEL} 下载失败：{e}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
