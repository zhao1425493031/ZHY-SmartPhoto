"""浏览器界面测试（Playwright + 系统 Edge）：需要先启动 app.py，截图输出到 outputs/ui。

用法：python tests/ui_test.py [--base http://127.0.0.1:7860] [--model hivision_modnet]
"""
import argparse
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright
from skimage import data

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = Path(__file__).resolve().parent.parent / "outputs" / "ui"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:7860")
    ap.add_argument("--model", default="hivision_modnet")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    sample = OUT / "sample.jpg"
    Image.fromarray(data.astronaut()).save(sample, quality=92)

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page.on("console", lambda m: m.type == "error" and errors.append(m.text))
        page.on("pageerror", lambda e: errors.append(str(e)))

        page.goto(args.base)
        page.evaluate(f"localStorage.setItem('smartphoto.model', JSON.stringify('{args.model}'))")
        page.reload()
        page.wait_for_selector("#specList .spec-item")
        page.screenshot(path=OUT / "01_empty.png")

        page.set_input_files("#fileInput", str(sample))
        page.wait_for_selector("#canvasView:not([hidden])", timeout=120_000)
        page.wait_for_function("document.querySelector('#photo').src.startsWith('data:')")
        page.wait_for_timeout(1200)
        page.screenshot(path=OUT / "02_result.png")

        page.click("#specList .spec-item[data-key='cn_passport']")
        page.wait_for_timeout(800)
        page.click("#swatches [data-key='blue']")
        page.wait_for_timeout(1500)
        page.screenshot(path=OUT / "03_passport_blue.png")

        page.click("#specList .spec-item[data-key='us_visa']")
        page.wait_for_timeout(800)
        box = page.locator("#frame").bounding_box()
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.mouse.down()
        page.mouse.move(box["x"] + box["width"] / 2 + 40, box["y"] + box["height"] / 2 + 60, steps=8)
        page.mouse.up()
        page.wait_for_timeout(1500)
        page.screenshot(path=OUT / "03b_visa_dragged.png")

        page.wait_for_selector("#sheetPreview:not([hidden])")
        page.click("#sheetPreview")
        page.wait_for_selector("#sheetModal:not([hidden])")
        page.wait_for_timeout(800)
        page.screenshot(path=OUT / "04_sheet.png")
        page.keyboard.press("Escape")

        page.click("#editSpecBtn")
        page.wait_for_selector("#specModal:not([hidden])")
        page.wait_for_timeout(300)
        page.screenshot(path=OUT / "05_spec_modal.png")
        page.keyboard.press("Escape")

        page.set_viewport_size({"width": 390, "height": 844})
        page.wait_for_timeout(600)
        page.screenshot(path=OUT / "06_mobile.png", full_page=True)
        browser.close()

    if errors:
        print("页面错误：")
        for e in errors:
            print("  ", e)
        sys.exit(1)
    print(f"界面测试完成，截图在 {OUT}")


if __name__ == "__main__":
    main()
