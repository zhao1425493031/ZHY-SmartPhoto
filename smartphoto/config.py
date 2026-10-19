from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPECS_PATH = ROOT / "specs.yaml"
USER_SPECS_PATH = ROOT / "user_specs.yaml"
MODELS_DIR = ROOT / "models"
OUTPUT_DIR = ROOT / "outputs"
USER_GROUP = "我的规格"

Range = tuple[float, float]


@dataclass
class Spec:
    key: str
    name: str
    size_px: tuple[int, int]
    dpi: int = 300
    head_height_ratio: Range = (0.52, 0.62)
    top_margin_ratio: Range | None = None
    eye_from_bottom_ratio: Range | None = None
    background: str = "white"
    format: str = "jpg"
    kb_range: Range | None = None
    size_mm: tuple[float, float] | None = None
    note: str = ""
    group: str = ""
    user: bool = False

    @property
    def width(self) -> int:
        return self.size_px[0]

    @property
    def height(self) -> int:
        return self.size_px[1]

    @property
    def physical_mm(self) -> tuple[float, float]:
        if self.size_mm:
            return self.size_mm
        return (self.width / self.dpi * 25.4, self.height / self.dpi * 25.4)


@dataclass
class Color:
    key: str
    name: str
    hex: str

    @property
    def rgb(self) -> tuple[int, int, int]:
        return hex_to_rgb(self.hex)


@dataclass
class Catalog:
    specs: dict[str, Spec] = field(default_factory=dict)
    colors: dict[str, Color] = field(default_factory=dict)


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip()
    if value.startswith("rgb"):
        nums = value[value.index("(") + 1 : value.index(")")].split(",")
        return tuple(int(round(float(n))) for n in nums[:3])  # type: ignore[return-value]
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        raise ValueError(f"无效的颜色值：#{value}")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _range(value) -> Range | None:
    if not value:
        return None
    lo, hi = float(value[0]), float(value[1])
    if lo == 0 and hi == 0:
        return None
    return (lo, hi)


def spec_from_dict(key: str, s: dict, *, group: str = "", user: bool = False) -> Spec:
    dpi = int(s.get("dpi", 300))
    size_mm = tuple(float(v) for v in s["size_mm"]) if s.get("size_mm") else None
    if s.get("size_px"):
        size_px = (int(s["size_px"][0]), int(s["size_px"][1]))
    elif size_mm:
        size_px = (round(size_mm[0] / 25.4 * dpi), round(size_mm[1] / 25.4 * dpi))
    else:
        raise ValueError(f"规格 {key} 缺少 size_px 或 size_mm")
    return Spec(
        key=key,
        name=s.get("name", key),
        size_px=size_px,
        dpi=dpi,
        head_height_ratio=_range(s.get("head_height_ratio")) or (0.52, 0.62),
        top_margin_ratio=_range(s.get("top_margin_ratio")),
        eye_from_bottom_ratio=_range(s.get("eye_from_bottom_ratio")),
        background=s.get("background", "white"),
        format=str(s.get("format", "jpg")).lower(),
        kb_range=_range(s.get("kb_range")),
        size_mm=size_mm,  # type: ignore[arg-type]
        note=s.get("note", ""),
        group=s.get("group", group),
        user=user,
    )


def spec_to_dict(spec: Spec) -> dict:
    return {
        "key": spec.key,
        "name": spec.name,
        "group": spec.group,
        "user": spec.user,
        "size_px": list(spec.size_px),
        "size_mm": [round(v, 2) for v in spec.physical_mm],
        "dpi": spec.dpi,
        "head_height_ratio": list(spec.head_height_ratio),
        "top_margin_ratio": list(spec.top_margin_ratio) if spec.top_margin_ratio else None,
        "eye_from_bottom_ratio": list(spec.eye_from_bottom_ratio) if spec.eye_from_bottom_ratio else None,
        "background": spec.background,
        "format": spec.format,
        "kb_range": list(spec.kb_range) if spec.kb_range else None,
        "note": spec.note,
    }


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_catalog(path: Path = SPECS_PATH) -> Catalog:
    data = _read_yaml(path)
    catalog = Catalog()
    for key, c in (data.get("colors") or {}).items():
        catalog.colors[key] = Color(key=key, name=c["name"], hex=c["hex"])
    for key, s in (_read_yaml(USER_SPECS_PATH).get("specs") or {}).items():
        catalog.specs[key] = spec_from_dict(key, s, group=USER_GROUP, user=True)
    for key, s in (data.get("specs") or {}).items():
        catalog.specs[key] = spec_from_dict(key, s)
    return catalog


def save_user_spec(spec: Spec) -> str:
    data = _read_yaml(USER_SPECS_PATH)
    specs = data.setdefault("specs", {}) or {}
    data["specs"] = specs
    key = spec.key if spec.key.startswith("user_") and spec.key in specs else f"user_{uuid.uuid4().hex[:8]}"
    entry = {k: v for k, v in spec_to_dict(spec).items() if k not in ("key", "group", "user") and v not in (None, "")}
    entry["size_mm"] = list(spec.size_mm) if spec.size_mm else None
    specs[key] = {k: v for k, v in entry.items() if v is not None}
    USER_SPECS_PATH.write_text(
        "# 在界面中保存的“我的规格”，格式与 specs.yaml 相同\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return key


def delete_user_spec(key: str) -> bool:
    data = _read_yaml(USER_SPECS_PATH)
    specs = data.get("specs") or {}
    if key not in specs:
        return False
    del specs[key]
    USER_SPECS_PATH.write_text(
        "# 在界面中保存的“我的规格”，格式与 specs.yaml 相同\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return True
