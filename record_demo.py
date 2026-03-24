"""
ATHAR — Automated Demo Video Recorder
Records a full walkthrough of the frontend + backend API.
Output: athar/demo/athar_demo.webm  (convert to MP4 with ffmpeg if needed)

Requirements:
    pip install playwright
    playwright install chromium

Run both servers first, then:
    python record_demo.py
"""

import asyncio
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌  Run:  pip install playwright && playwright install chromium")
    sys.exit(1)

FRONTEND = "http://localhost:3000"
BACKEND  = "http://localhost:8000"

OUT_DIR  = Path(__file__).parent / "demo"
OUT_DIR.mkdir(exist_ok=True)

# ── Scene helpers ─────────────────────────────────────────────────────────────

async def pause(ms: int = 1200):
    await asyncio.sleep(ms / 1000)

async def slow_scroll(page, steps: int = 8, delay_ms: int = 180):
    """Smoothly scroll down the page."""
    for _ in range(steps):
        await page.mouse.wheel(0, 220)
        await asyncio.sleep(delay_ms / 1000)
    await asyncio.sleep(0.6)

async def slow_scroll_up(page, steps: int = 4, delay_ms: int = 150):
    for _ in range(steps):
        await page.mouse.wheel(0, -220)
        await asyncio.sleep(delay_ms / 1000)

async def highlight_click(page, selector: str):
    """Click an element after a brief hover pause."""
    await page.hover(selector)
    await pause(600)
    await page.click(selector)

# ── Scenes ────────────────────────────────────────────────────────────────────

async def scene_landing(page):
    print("  🎬  Scene 1 — Landing page")
    await page.goto(FRONTEND, wait_until="networkidle")
    await pause(2000)
    await slow_scroll(page, steps=4)
    await pause(1000)
    await slow_scroll_up(page, steps=4)
    await pause(1500)

async def scene_dashboard(page):
    print("  🎬  Scene 2 — Dashboard (default 90-day view)")
    await highlight_click(page, "a[href='/dashboard']")
    await page.wait_for_url("**/dashboard", timeout=10_000)
    await pause(3000)   # let charts + map render

    # Scroll to see all charts
    await slow_scroll(page, steps=10, delay_ms=200)
    await pause(1500)
    await slow_scroll_up(page, steps=10, delay_ms=150)
    await pause(1000)

async def scene_filters(page):
    print("  🎬  Scene 3 — Period filter interaction")
    # Switch to 30-day view
    try:
        btns = page.locator("button", has_text="آخر 30 يوم")
        await btns.first.click()
        await pause(2000)

        # Switch to 12-month view
        btns12 = page.locator("button", has_text="آخر 12 شهر")
        await btns12.first.click()
        await pause(2500)

        # Switch back to 90-day
        btns90 = page.locator("button", has_text="آخر 90 يوم")
        await btns90.first.click()
        await pause(1500)
    except Exception:
        await pause(1000)

async def scene_region_filter(page):
    print("  🎬  Scene 4 — Region filter (Jeddah)")
    try:
        select = page.locator("select")
        await select.select_option("Jeddah")
        await pause(2500)
        await slow_scroll(page, steps=6)
        await pause(1000)
        await slow_scroll_up(page, steps=6)
        await pause(800)
        # Reset to all regions
        await select.select_option("")
        await pause(1500)
    except Exception:
        await pause(1000)

async def scene_reports(page):
    print("  🎬  Scene 5 — Reports page")
    await highlight_click(page, "a[href='/reports']")
    await page.wait_for_url("**/reports", timeout=10_000)
    await pause(1500)
    await slow_scroll(page, steps=10, delay_ms=200)
    await pause(1000)
    await slow_scroll_up(page, steps=10, delay_ms=150)
    await pause(1500)

async def scene_api_docs(page):
    print("  🎬  Scene 6 — Backend API (Swagger UI)")
    await page.goto(f"{BACKEND}/docs", wait_until="networkidle")
    await pause(2000)
    await slow_scroll(page, steps=6)
    await pause(1200)

    # Expand /dashboard-data endpoint
    try:
        endpoint = page.locator("span.opblock-summary-path", has_text="dashboard-data")
        await endpoint.first.click()
        await pause(1800)
    except Exception:
        pass

    await slow_scroll(page, steps=4)
    await pause(2000)

async def scene_api_json(page):
    print("  🎬  Scene 7 — Live API JSON responses")
    endpoints = [
        f"{BACKEND}/health",
        f"{BACKEND}/regions",
        f"{BACKEND}/dashboard-data?period=90",
    ]
    for url in endpoints:
        await page.goto(url, wait_until="load")
        await pause(2000)

# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("\n🎥  ATHAR Demo Video Recorder")
    print(f"    Output: {OUT_DIR / 'athar_demo.webm'}\n")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu"],
        )

        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
            record_video_dir=str(OUT_DIR),
            record_video_size={"width": 1440, "height": 900},
        )

        page = await context.new_page()

        try:
            await scene_landing(page)
            await scene_dashboard(page)
            await scene_filters(page)
            await scene_region_filter(page)
            await scene_reports(page)
            await scene_api_docs(page)
            await scene_api_json(page)

            # Final pause before closing
            await pause(2000)

        except Exception as exc:
            print(f"  ⚠️  Scene error: {exc}")

        # Must close context to flush video
        video_path = await page.video.path()
        await context.close()
        await browser.close()

    # Rename the auto-generated file to a clean name
    import shutil
    final = OUT_DIR / "athar_demo.webm"
    if Path(video_path).exists() and video_path != str(final):
        shutil.move(video_path, final)

    print(f"\n✅  Video saved → {final}")
    print("    Duration: ~60–75 seconds\n")
    print("    To convert to MP4 (optional):")
    print("    ffmpeg -i demo/athar_demo.webm -c:v libx264 demo/athar_demo.mp4\n")


if __name__ == "__main__":
    asyncio.run(main())
