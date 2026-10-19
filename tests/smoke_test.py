"""用样图跑通所有规格并打印校验结果。

用法：
    .venv\\Scripts\\python.exe tests\\smoke_test.py [照片路径 ...] [--model 模型名]
不传照片时使用 scikit-image 自带的公有领域人像样图，并额外生成一张倾斜版本测试自动摆正。
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402

from smartphoto import matting  # noqa: E402
from smartphoto.config import load_catalog  # noqa: E402
from smartphoto.export import encode, validate  # noqa: E402
from smartphoto.layout import make_sheet  # noqa: E402
from smartphoto.pipeline import prepare, render  # noqa: E402
from smartphoto.preview import guide_overlay  # noqa: E402

OUT = ROOT / "outputs" / "smoke"


def sample_images() -> dict[str, Image.Image]:
    from skimage import data

    base = Image.fromarray(data.astronaut())
    tilted = base.rotate(-7, resample=Image.BICUBIC, expand=False, fillcolor=(40, 40, 40))
    return {"astronaut": base, "astronaut_tilted": tilted}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("photos", nargs="*")
    parser.add_argument("--model", default=matting.DEFAULT_MODEL, choices=list(matting.MODELS))
    args = parser.parse_args()

    images = {Path(p).stem: Image.open(p) for p in args.photos} if args.photos else sample_images()
    catalog = load_catalog()
    OUT.mkdir(parents=True, exist_ok=True)
    failed = 0

    for name, img in images.items():
        t = time.perf_counter()
        prep = prepare(img, args.model)
        print(f"\n=== {name}：分析耗时 {time.perf_counter() - t:.1f}s，倾斜 {prep.roll_deg:+.1f}°")
        for w in prep.warnings:
            print(f"  [原图提示] {w}")

        for key, spec in catalog.specs.items():
            color = catalog.colors[spec.background]
            t = time.perf_counter()
            result = render(prep, spec, color.rgb)
            enc = encode(result.image, spec)
            checks = validate(enc, spec, result.layout, color.rgb, gradient=False)
            ms = (time.perf_counter() - t) * 1000
            bad = [c for c in checks if c.status == "fail"]
            failed += bool(bad)
            flag = "OK  " if not bad else "FAIL"
            print(f"  {flag} {spec.name:<24} {ms:6.0f}ms  " + "；".join(f"{c.name}:{c.value}（{c.requirement}）" for c in checks if c.status != "pass" or c.key in ("head", "filesize")))
            for w in result.warnings:
                print(f"       [构图提示] {w}")
            (OUT / f"{name}_{key}.{enc.ext}").write_bytes(enc.data)
            guide_overlay(result.image, spec, result.layout).save(OUT / f"{name}_{key}_guide.png")
            if key == "one_inch":
                sheet, n = make_sheet(result.image, spec)
                sheet.save(OUT / f"{name}_{key}_sheet{n}.jpg", quality=92)

        blue = catalog.colors["blue"].rgb
        render(prep, catalog.specs["one_inch"], blue).image.save(OUT / f"{name}_one_inch_blue.png")
        render(prep, catalog.specs["one_inch"], catalog.colors["red"].rgb).image.save(OUT / f"{name}_one_inch_red.png")

    print(f"\n输出目录：{OUT}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
