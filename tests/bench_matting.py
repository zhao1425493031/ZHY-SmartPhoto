"""对比各抠图模型的速度和边缘效果，输出并排对比图到 outputs/bench。"""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from smartphoto import matting  # noqa: E402
from smartphoto.pipeline import load_image  # noqa: E402

OUT = ROOT / "outputs" / "bench"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    models = sys.argv[1:] or list(matting.MODELS)
    from skimage import data

    img = load_image(Image.fromarray(data.astronaut()))
    OUT.mkdir(parents=True, exist_ok=True)
    blue = np.array([67, 142, 219], dtype=np.float32) / 255
    tiles = []
    for name in models:
        matting.estimate_alpha(img, name)  # 预热，排除模型加载时间
        t = time.perf_counter()
        alpha = matting.estimate_alpha(img, name)
        cost = time.perf_counter() - t
        fg = matting.estimate_foreground(img, alpha)
        comp = fg * alpha[..., None] + blue * (1 - alpha[..., None])
        tile = Image.fromarray((comp * 255).astype(np.uint8)).crop((130, 10, 330, 210)).resize((400, 400), Image.LANCZOS)
        ImageDraw.Draw(tile).text((8, 8), f"{name}  {cost:.1f}s", fill="yellow")
        tiles.append(tile)
        print(f"{name:<40} {cost:6.2f}s")
    sheet = Image.new("RGB", (400 * len(tiles), 400))
    for i, t in enumerate(tiles):
        sheet.paste(t, (400 * i, 0))
    sheet.save(OUT / "compare.png")
    print(f"对比图：{OUT / 'compare.png'}")


if __name__ == "__main__":
    main()
