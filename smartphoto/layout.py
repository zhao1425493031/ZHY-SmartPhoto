from __future__ import annotations

from PIL import Image, ImageDraw

from .config import Spec

SHEET_DPI = 300
SHEET_INCH = (6, 4)  # 六寸相纸 6×4 英寸
MARGIN_MM = 0.8
GAP_MM = 1.5


def _mm(v: float) -> int:
    return round(v / 25.4 * SHEET_DPI)


def _plan(spec: Spec) -> tuple[int, int, int, int, int, int]:
    """返回 (照片宽, 照片高, 相纸宽, 相纸高, 列数, 行数)，单位为相纸像素。"""
    w_mm, h_mm = spec.physical_mm
    pw, ph = _mm(w_mm), _mm(h_mm)
    margin, gap = _mm(MARGIN_MM), _mm(GAP_MM)
    best = None
    for sw, sh in ((SHEET_INCH[0] * SHEET_DPI, SHEET_INCH[1] * SHEET_DPI), (SHEET_INCH[1] * SHEET_DPI, SHEET_INCH[0] * SHEET_DPI)):
        cols = max(0, (sw - 2 * margin + gap) // (pw + gap))
        rows = max(0, (sh - 2 * margin + gap) // (ph + gap))
        if best is None or cols * rows > best[4] * best[5]:
            best = (pw, ph, sw, sh, cols, rows)
    return best  # type: ignore[return-value]


def sheet_capacity(spec: Spec) -> int:
    _, _, _, _, cols, rows = _plan(spec)
    return cols * rows


def make_sheet(photo: Image.Image, spec: Spec) -> tuple[Image.Image, int]:
    """把证件照按实际物理尺寸平铺到六寸相纸上，返回 (相纸图, 张数)。"""
    pw, ph, sw, sh, cols, rows = _plan(spec)
    count = cols * rows
    tile = photo.convert("RGB").resize((pw, ph), Image.LANCZOS)
    gap = _mm(GAP_MM)

    sheet = Image.new("RGB", (sw, sh), "white")
    draw = ImageDraw.Draw(sheet)
    grid_w = cols * pw + max(cols - 1, 0) * gap
    grid_h = rows * ph + max(rows - 1, 0) * gap
    x0, y0 = (sw - grid_w) // 2, (sh - grid_h) // 2
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * (pw + gap), y0 + r * (ph + gap)
            sheet.paste(tile, (x, y))
            draw.rectangle([x - 1, y - 1, x + pw, y + ph], outline=(200, 200, 200), width=1)
    return sheet, count
