from __future__ import annotations

import io
from dataclasses import dataclass, field

import numpy as np
from PIL import Image

from .config import Spec
from .pipeline import Layout

MAX_COMMENT_BYTES = 65000
BG_TOLERANCE = 8


@dataclass
class Encoded:
    data: bytes
    ext: str
    quality: int | None = None
    padded_bytes: int = 0
    notes: list[str] = field(default_factory=list)

    @property
    def kb(self) -> float:
        return len(self.data) / 1024


@dataclass
class Check:
    key: str  # size / format / dpi / filesize / head / top / eye / center / background / note
    name: str
    status: str  # pass / fail / warn
    value: str
    requirement: str = ""


def _jpeg(img: Image.Image, dpi: int, quality: int, subsampling: int = 0, comment: bytes | None = None) -> bytes:
    buf = io.BytesIO()
    kwargs = dict(format="JPEG", quality=quality, subsampling=subsampling, optimize=True, dpi=(dpi, dpi))
    if comment:
        kwargs["comment"] = comment
    img.save(buf, **kwargs)
    return buf.getvalue()


def _first_true(pred, lo: int, hi: int) -> int | None:
    """在 [lo, hi] 里找让单调谓词 pred 成立的最小整数。"""
    found = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if pred(mid):
            found, hi = mid, mid - 1
        else:
            lo = mid + 1
    return found


def encode(img: Image.Image, spec: Spec) -> Encoded:
    img = img.convert("RGB")
    if spec.format == "png":
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True, dpi=(spec.dpi, spec.dpi))
        return Encoded(data=buf.getvalue(), ext="png")

    lo_kb, hi_kb = spec.kb_range or (0.0, 0.0)
    lo, hi = lo_kb * 1024, (hi_kb * 1024 if hi_kb else float("inf"))
    cache: dict[int, bytes] = {}

    def at(q: int) -> bytes:
        if q not in cache:
            cache[q] = _jpeg(img, spec.dpi, q)
        return cache[q]

    def fits(q: int) -> bool:
        return len(at(q)) <= hi

    # 满足上限的最高质量（默认不超过 95，再高体积暴涨但肉眼无差别）
    over = _first_true(lambda q: not fits(q), 10, 95)
    q = 95 if over is None else over - 1
    if q < 10:
        for q2 in (40, 25, 15, 10):
            data = _jpeg(img, spec.dpi, q2, subsampling=2)
            if len(data) <= hi:
                return Encoded(data=data, ext="jpg", quality=q2, notes=["为满足大小上限，已降低色度采样。"])
        data = _jpeg(img, spec.dpi, 10, subsampling=2)
        return Encoded(data=data, ext="jpg", quality=10, notes=["已压到最低质量仍超过大小上限。"])

    if len(at(q)) >= lo:
        return Encoded(data=at(q), ext="jpg", quality=q)

    # 体积不足下限：找达到下限的最低质量
    q_lo = _first_true(lambda x: len(at(x)) >= lo, q + 1, 100)
    if q_lo is not None and fits(q_lo):
        return Encoded(data=at(q_lo), ext="jpg", quality=q_lo)

    # 仍不行：用满足上限的最高质量，在 JPEG 注释段补足体积
    over = _first_true(lambda x: not fits(x), q, 100)
    q_max = 100 if over is None else over - 1
    need = int(lo - len(at(q_max))) + 64
    if 0 < need <= MAX_COMMENT_BYTES:
        padded = _jpeg(img, spec.dpi, q_max, comment=b" " * need)
        if lo <= len(padded) <= hi:
            return Encoded(
                data=padded,
                ext="jpg",
                quality=q_max,
                padded_bytes=need,
                notes=["图片内容不足最小体积，已在 JPEG 注释段补足，不影响画面。"],
            )
    return Encoded(data=at(q_max), ext="jpg", quality=q_max, notes=["无法达到最小文件大小要求。"])


def _in(value: float, rng: tuple[float, float]) -> bool:
    return rng[0] - 1e-6 <= value <= rng[1] + 1e-6


def _pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def _rng(r: tuple[float, float]) -> str:
    return f"{_pct(r[0])} ～ {_pct(r[1])}"


def validate(enc: Encoded, spec: Spec, layout: Layout, bg_rgb: tuple[int, int, int], gradient: bool) -> list[Check]:
    checks: list[Check] = []
    img = Image.open(io.BytesIO(enc.data))
    img.load()

    checks.append(Check(
        "size", "像素尺寸", "pass" if img.size == spec.size_px else "fail",
        f"{img.width} × {img.height}", f"{spec.width} × {spec.height}",
    ))

    fmt = {"JPEG": "jpg", "PNG": "png"}.get(img.format or "", img.format or "?")
    checks.append(Check("format", "文件格式", "pass" if fmt == spec.format else "fail", fmt.upper(), spec.format.upper()))

    dpi = round(float(img.info.get("dpi", (0, 0))[0]))
    checks.append(Check("dpi", "分辨率", "pass" if dpi == spec.dpi else "fail", f"{dpi} DPI", f"{spec.dpi} DPI"))

    kb = enc.kb
    if spec.kb_range:
        lo, hi = spec.kb_range
        size_ok = (not lo or kb >= lo) and (not hi or kb <= hi)
        req = f"{lo:g} ～ {hi:g} KB" if lo and hi else (f"≥ {lo:g} KB" if lo else f"≤ {hi:g} KB")
        checks.append(Check("filesize", "文件大小", "pass" if size_ok else "fail", f"{kb:.1f} KB", req))
    else:
        checks.append(Check("filesize", "文件大小", "pass", f"{kb:.1f} KB", "不限"))

    head = layout.head_ratio
    checks.append(Check(
        "head", "头部比例", "pass" if _in(head, spec.head_height_ratio) else "fail",
        _pct(head), _rng(spec.head_height_ratio),
    ))

    if spec.top_margin_ratio:
        top = layout.top_margin_ratio
        checks.append(Check(
            "top", "头顶留白", "pass" if _in(top, spec.top_margin_ratio) else "fail",
            _pct(top), _rng(spec.top_margin_ratio),
        ))
    elif layout.head_top < 0:
        checks.append(Check("top", "头顶留白", "fail", "超出上边缘", "头顶完整可见"))

    if spec.eye_from_bottom_ratio:
        eye = layout.eye_from_bottom_ratio
        checks.append(Check(
            "eye", "眼睛高度", "pass" if _in(eye, spec.eye_from_bottom_ratio) else "fail",
            _pct(eye), _rng(spec.eye_from_bottom_ratio),
        ))

    off = layout.center_offset_ratio
    checks.append(Check("center", "水平居中", "pass" if abs(off) <= 0.03 else "warn", f"偏移 {_pct(abs(off))}", "≤ 3.0%"))

    if not gradient:
        arr = np.asarray(img.convert("RGB"), dtype=np.float32)
        patch = max(4, min(img.size) // 30)
        corners = [arr[:patch, :patch], arr[:patch, -patch:]]
        diff = max(float(np.abs(c.reshape(-1, 3).mean(axis=0) - np.array(bg_rgb)).max()) for c in corners)
        checks.append(Check(
            "background", "背景颜色", "pass" if diff <= BG_TOLERANCE else "warn",
            f"色差 {diff:.1f}", f"≤ {BG_TOLERANCE}",
        ))

    for note in enc.notes:
        checks.append(Check("note", "编码说明", "warn", note))
    return checks
