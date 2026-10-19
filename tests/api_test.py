"""HTTP 接口端到端测试：需要先启动 app.py。

用法：python tests/api_test.py [--base http://127.0.0.1:7860] [--model hivision_modnet]
"""
import argparse
import io
import sys
import time

import httpx
from PIL import Image
from skimage import data

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:7860")
    ap.add_argument("--model", default="hivision_modnet")
    args = ap.parse_args()
    c = httpx.Client(base_url=args.base, timeout=120)

    assert c.get("/").status_code == 200
    for path in ("/assets/app.js", "/assets/styles.css", "/assets/favicon.svg"):
        assert c.get(path).status_code == 200, path
    cfg = c.get("/api/config").json()
    print(f"规格 {len(cfg['specs'])} 个，颜色 {len(cfg['colors'])} 个，模型 {list(cfg['models'])}")

    buf = io.BytesIO()
    Image.fromarray(data.astronaut()).save(buf, "JPEG", quality=92)
    job = c.post("/api/jobs", files={"file": ("测试.jpg", buf.getvalue(), "image/jpeg")},
                 data={"model": args.model}).json()
    t0 = time.time()
    while True:
        st = c.get(f"/api/jobs/{job['job_id']}").json()
        if st["status"] in ("done", "error"):
            break
        time.sleep(0.3)
    assert st["status"] == "done", st
    sid = st["result"]["session_id"]
    print(f"分析完成 {time.time() - t0:.1f}s，提示：{st['result']['warnings']}")

    by_key = {s["key"]: s for s in cfg["specs"]}
    hex_of = {col["key"]: col["hex"] for col in cfg["colors"]}
    for key, spec in by_key.items():
        body = {"session_id": sid, "spec": spec, "color": hex_of[spec["background"]],
                "gradient": False, "zoom": 1.0, "offset_x": 0, "offset_y": 0}
        r = c.post("/api/render", json=body)
        assert r.status_code == 200, (key, r.text)
        res = r.json()
        fails = [ck["name"] for ck in res["checks"] if ck["status"] == "fail"]
        print(f"  {spec['name']:<10} {res['size'][0]}x{res['size'][1]} {res['kb']:.1f}KB "
              f"{'通过' if res['ok'] else '未通过 ' + ','.join(fails)} 排版 {res['sheet_count']} 张")

    body["zoom"], body["offset_x"] = 1.2, 0.1
    assert c.post("/api/render", json=body).status_code == 200
    bad = dict(body, zoom=3)
    assert c.post("/api/render", json=bad).status_code == 422

    photo = c.get(f"/api/sessions/{sid}/photo")
    assert photo.status_code == 200 and photo.content[:2] == b"\xff\xd8"
    print(f"下载照片 {len(photo.content) / 1024:.1f}KB，{photo.headers['content-disposition']}")
    prev = c.get(f"/api/sessions/{sid}/sheet")
    full = c.get(f"/api/sessions/{sid}/sheet", params={"download": 1})
    assert prev.status_code == full.status_code == 200
    print(f"排版预览 {Image.open(io.BytesIO(prev.content)).size}，下载 {Image.open(io.BytesIO(full.content)).size}")

    spec = {k: v for k, v in by_key["one_inch"].items() if k not in ("user", "group")}
    spec.update(name="测试规格", key="custom", note="接口测试")
    r = c.post("/api/specs", json=spec)
    assert r.status_code == 200, r.text
    key = r.json()["key"]
    assert any(s["key"] == key and s["user"] for s in r.json()["specs"])
    assert c.delete(f"/api/specs/{key}").status_code == 200
    assert c.delete("/api/specs/one_inch").status_code in (400, 404)
    print(f"自定义规格保存/删除正常（{key}）")

    assert c.post("/api/render", json=dict(body, session_id="nope")).status_code == 410
    assert c.post("/api/jobs", files={"file": ("x.jpg", b"not image", "image/jpeg")},
                  data={"model": args.model}).status_code in (200, 400)
    print("全部通过")


if __name__ == "__main__":
    main()
