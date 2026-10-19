from __future__ import annotations

from PIL import Image, ImageDraw

from .config import Spec
from .pipeline import Layout

PREVIEW_HEIGHT = 640
BAND = (34, 197, 94, 60)
BAND_EDGE = (22, 163, 74, 200)
LINE = (239, 68, 68, 255)
CENTER = (59, 130, 246, 160)


def guide_overlay(photo: Image.Image, spec: Spec, layout: Layout) -> Image.Image:
    """在放大的预览图上画出允许范围（绿色带）和实际位置（红线）。"""
    k = PREVIEW_HEIGHT / photo.height
    W, H = round(photo.width * k), PREVIEW_HEIGHT
    base = photo.convert("RGBA").resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    def band(y0: float, y1: float) -> None:
        y0, y1 = y0 * k, y1 * k
        d.rectangle([0, y0, W, y1], fill=BAND)
        d.line([0, y0, W, y0], fill=BAND_EDGE, width=1)
        d.line([0, y1, W, y1], fill=BAND_EDGE, width=1)

    h = layout.height
    lo, hi = spec.head_height_ratio
    if spec.top_margin_ratio:
        band(spec.top_margin_ratio[0] * h, spec.top_margin_ratio[1] * h)
    if spec.eye_from_bottom_ratio:
        band((1 - spec.eye_from_bottom_ratio[1]) * h, (1 - spec.eye_from_bottom_ratio[0]) * h)
    band(layout.head_top + lo * h, layout.head_top + hi * h)

    d.line([W / 2, 0, W / 2, H], fill=CENTER, width=1)
    for y in (layout.head_top, layout.chin):
        d.line([0, y * k, W, y * k], fill=LINE, width=2)
    if spec.eye_from_bottom_ratio:
        d.line([0, layout.eye_y * k, W, layout.eye_y * k], fill=LINE, width=1)

    return Image.alpha_composite(base, overlay).convert("RGB")
