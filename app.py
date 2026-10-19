from __future__ import annotations

import argparse
import base64
import io
import logging
import socket
import sys
import threading
import time
import traceback
import uuid
import webbrowser
from collections import OrderedDict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Literal
from urllib.parse import quote

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel, Field, field_validator

from smartphoto import matting
from smartphoto.config import (
    OUTPUT_DIR,
    ROOT,
    Spec,
    delete_user_spec,
    hex_to_rgb,
    load_catalog,
    save_user_spec,
    spec_from_dict,
    spec_to_dict,
)
from smartphoto.export import Encoded, encode, validate
from smartphoto.layout import make_sheet, sheet_capacity
from smartphoto.pipeline import Adjust, PhotoError, Prepared, prepare, render

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    pass

WEB_DIR = ROOT / "web"
MAX_UPLOAD_BYTES = 30 * 1024 * 1024
MAX_SESSIONS = 6
JOB_TTL_SECONDS = 600

log = logging.getLogger("smartphoto")


@dataclass
class LastRender:
    spec: Spec
    enc: Encoded
    render_id: int


@dataclass
class Session:
    prep: Prepared
    last: LastRender | None = None
    renders: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)


@dataclass
class Job:
    model: str
    stage: str = "queue"
    progress: float = 0.0
    status: str = "running"  # running / done / error
    error: str = ""
    result: dict | None = None
    created: float = field(default_factory=time.time)


sessions: OrderedDict[str, Session] = OrderedDict()
jobs: dict[str, Job] = {}
measured_seconds: dict[str, float] = {}
store_lock = threading.Lock()
analysis_slot = threading.Semaphore(1)

app = FastAPI(title="SmartPhoto", docs_url=None, redoc_url=None)


# ---------- 配置与规格 ----------


def _config_payload() -> dict:
    catalog = load_catalog()
    return {
        "specs": [spec_to_dict(s) for s in catalog.specs.values()],
        "colors": [{"key": c.key, "name": c.name, "hex": c.hex} for c in catalog.colors.values()],
        "models": [
            {"key": k, "label": m.label, "desc": m.desc, "eta": measured_seconds.get(k, m.eta_seconds)}
            for k, m in matting.MODELS.items()
        ],
        "default_model": matting.DEFAULT_MODEL,
    }


class SpecIn(BaseModel):
    key: str = "custom"
    name: str = Field("自定义", min_length=1, max_length=40)
    size_px: tuple[int, int]
    size_mm: tuple[float, float] | None = None
    dpi: int = Field(300, ge=72, le=1200)
    head_height_ratio: tuple[float, float]
    top_margin_ratio: tuple[float, float] | None = None
    eye_from_bottom_ratio: tuple[float, float] | None = None
    background: str = "white"
    format: Literal["jpg", "png"] = "jpg"
    kb_range: tuple[float, float] | None = None
    note: str = ""

    @field_validator("size_px")
    @classmethod
    def _size(cls, v):
        if not all(50 <= x <= 4000 for x in v):
            raise ValueError("照片宽高需在 50～4000 像素之间")
        return v

    @field_validator("head_height_ratio", "top_margin_ratio", "eye_from_bottom_ratio")
    @classmethod
    def _ratio(cls, v):
        if v is None:
            return v
        lo, hi = v
        if not (0 <= lo <= hi < 1):
            raise ValueError("比例范围需满足 0 ≤ 下限 ≤ 上限 < 100%")
        return v

    @field_validator("kb_range")
    @classmethod
    def _kb(cls, v):
        if v is None:
            return v
        lo, hi = v
        if lo < 0 or hi < 0 or (hi and lo > hi):
            raise ValueError("文件大小范围填写有误")
        return v

    def to_spec(self) -> Spec:
        return spec_from_dict(self.key, self.model_dump())


@app.get("/api/config")
def get_config():
    return _config_payload()


@app.post("/api/specs")
def create_spec(spec: SpecIn):
    key = save_user_spec(spec.to_spec())
    return {"key": key, **_config_payload()}


@app.delete("/api/specs/{key}")
def remove_spec(key: str):
    if not delete_user_spec(key):
        raise HTTPException(404, "只能删除“我的规格”中的条目")
    return _config_payload()


# ---------- 分析任务 ----------


def _store_session(prep: Prepared) -> str:
    sid = uuid.uuid4().hex
    with store_lock:
        sessions[sid] = Session(prep=prep)
        while len(sessions) > MAX_SESSIONS:
            sessions.popitem(last=False)
    return sid


def _get_session(sid: str) -> Session:
    with store_lock:
        sess = sessions.get(sid)
        if sess is not None:
            sessions.move_to_end(sid)
    if sess is None:
        raise HTTPException(410, "照片会话已过期，请重新上传")
    return sess


def _run_job(job_id: str, data: bytes) -> None:
    job = jobs[job_id]
    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception:
        job.status, job.error = "error", "无法识别这张图片，请使用 JPG、PNG 或 HEIC 格式。"
        return

    def progress(stage: str, value: float) -> None:
        job.stage, job.progress = stage, value

    with analysis_slot:
        start = time.time()
        try:
            prep = prepare(img, job.model, progress=progress)
        except PhotoError as e:
            job.status, job.error = "error", str(e)
            return
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            job.status, job.error = "error", f"处理失败：{e}"
            return
        elapsed = time.time() - start
    measured_seconds[job.model] = elapsed
    job.result = {
        "session_id": _store_session(prep),
        "warnings": prep.warnings,
        "roll": round(prep.roll_deg, 1),
        "model": job.model,
        "elapsed": round(elapsed, 1),
    }
    job.stage, job.progress, job.status = "done", 1.0, "done"


@app.post("/api/jobs")
async def create_job(file: UploadFile = File(...), model: str = Form(matting.DEFAULT_MODEL)):
    if model not in matting.MODELS:
        raise HTTPException(400, "不支持的抠图模型")
    data = await file.read()
    if not data:
        raise HTTPException(400, "图片为空")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "图片超过 30MB，请压缩后再上传")

    now = time.time()
    for jid in [k for k, j in jobs.items() if now - j.created > JOB_TTL_SECONDS]:
        jobs.pop(jid, None)

    job_id = uuid.uuid4().hex
    jobs[job_id] = Job(model=model)
    threading.Thread(target=_run_job, args=(job_id, data), daemon=True).start()
    eta = measured_seconds.get(model, matting.MODELS[model].eta_seconds)
    return {"job_id": job_id, "eta": eta}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(404, "任务不存在")
    return {
        "status": job.status,
        "stage": job.stage,
        "progress": job.progress,
        "error": job.error,
        "result": job.result,
    }


# ---------- 渲染与下载 ----------


class RenderIn(BaseModel):
    session_id: str
    spec: SpecIn
    color: str = "#FFFFFF"
    gradient: bool = False
    zoom: float = Field(1.0, ge=0.6, le=1.5)
    offset_x: float = Field(0.0, ge=-0.5, le=0.5)
    offset_y: float = Field(0.0, ge=-0.5, le=0.5)


@app.post("/api/render")
def render_photo(req: RenderIn):
    sess = _get_session(req.session_id)
    spec = req.spec.to_spec()
    try:
        rgb = hex_to_rgb(req.color)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e

    with sess.lock:
        result = render(sess.prep, spec, rgb, Adjust(req.zoom, req.offset_x, req.offset_y), gradient=req.gradient)
        enc = encode(result.image, spec)
        checks = validate(enc, spec, result.layout, rgb, req.gradient)
        sess.renders += 1
        sess.last = LastRender(spec=spec, enc=enc, render_id=sess.renders)
        render_id = sess.renders

    lay = result.layout
    mime = "image/jpeg" if enc.ext == "jpg" else "image/png"
    return {
        "render_id": render_id,
        "image": f"data:{mime};base64,{base64.b64encode(enc.data).decode()}",
        "ext": enc.ext,
        "kb": round(enc.kb, 1),
        "quality": enc.quality,
        "size": list(spec.size_px),
        "size_mm": [round(v, 1) for v in spec.physical_mm],
        "dpi": spec.dpi,
        "ok": not any(c.status == "fail" for c in checks),
        "checks": [asdict(c) for c in checks],
        "warnings": result.warnings,
        "layout": {
            "head_top": lay.head_top,
            "chin": lay.chin,
            "eye_y": lay.eye_y,
            "center_x": lay.center_x,
            "width": lay.width,
            "height": lay.height,
        },
        "ranges": {
            "head": spec.head_height_ratio,
            "top": spec.top_margin_ratio,
            "eye": spec.eye_from_bottom_ratio,
        },
        "sheet_count": sheet_capacity(spec),
    }


def _file_stem(spec: Spec) -> str:
    name = spec.name.split("（")[0]
    for ch in '/\\:*?"<>| ':
        name = name.replace(ch, "")
    return f"{name}_{spec.width}x{spec.height}_{datetime.now():%Y%m%d_%H%M%S}"


def _attachment(data: bytes, filename: str, media_type: str) -> Response:
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / filename).write_bytes(data)
    return Response(
        data,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"},
    )


def _last(sid: str) -> LastRender:
    sess = _get_session(sid)
    if sess.last is None:
        raise HTTPException(404, "还没有生成证件照")
    return sess.last


@app.get("/api/sessions/{sid}/photo")
def download_photo(sid: str):
    last = _last(sid)
    mime = "image/jpeg" if last.enc.ext == "jpg" else "image/png"
    return _attachment(last.enc.data, f"{_file_stem(last.spec)}.{last.enc.ext}", mime)


@app.get("/api/sessions/{sid}/sheet")
def sheet(sid: str, download: bool = False):
    last = _last(sid)
    photo = Image.open(io.BytesIO(last.enc.data)).convert("RGB")
    img, count = make_sheet(photo, last.spec)
    buf = io.BytesIO()
    if download:
        img.save(buf, format="JPEG", quality=95, subsampling=0, dpi=(300, 300))
        return _attachment(buf.getvalue(), f"{_file_stem(last.spec)}_六寸排版{count}张.jpg", "image/jpeg")
    img.thumbnail((1000, 1000), Image.LANCZOS)
    img.save(buf, format="JPEG", quality=88)
    return Response(buf.getvalue(), media_type="image/jpeg", headers={"Cache-Control": "no-store"})


# ---------- 页面 ----------


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html", headers={"Cache-Control": "no-cache"})


app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")


def _lan_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "本机IP"


def main() -> None:
    import uvicorn

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="SmartPhoto 证件照工作台")
    parser.add_argument("--lan", action="store_true", help="允许同一局域网的手机等设备访问")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--no-browser", action="store_true", help="启动后不自动打开浏览器")
    args = parser.parse_args()

    host = "0.0.0.0" if args.lan else "127.0.0.1"
    url = f"http://127.0.0.1:{args.port}"
    print(f"SmartPhoto 已启动：{url}", flush=True)
    if args.lan:
        print(f"手机访问地址：http://{_lan_ip()}:{args.port}", flush=True)
    if not args.no_browser:
        threading.Timer(1.2, webbrowser.open, args=(url,)).start()
    uvicorn.run(app, host=host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
