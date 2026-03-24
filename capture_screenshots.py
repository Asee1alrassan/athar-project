"""
ATHAR — Screenshot Capture Script
Captures screenshots of all frontend pages and backend API docs.
Saves them to: athar/screenshots/

Requirements:
    pip install playwright
    playwright install chromium

Make sure both servers are running first:
    Backend:  uvicorn app.main:app --reload --port 8000  (inside backend/)
    Frontend: npm run dev                                  (inside frontend/)
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from playwright.async_api import async_playwright, TimeoutError as PWTimeout
except ImportError:
    print("❌  Playwright not installed. Run:  pip install playwright && playwright install chromium")
    sys.exit(1)

# ── Config ────────────────────────────────────────────────────────────────────

FRONTEND_BASE = "http://localhost:3000"
BACKEND_BASE  = "http://localhost:8000"

OUT_DIR = Path(__file__).parent / "screenshots"
OUT_DIR.mkdir(exist_ok=True)

PAGES = [
    # (label, url, wait_selector, full_page)
    ("01_landing",              f"{FRONTEND_BASE}/",           "nav",              True),
    ("02_dashboard",            f"{FRONTEND_BASE}/dashboard",  ".leaflet-container, canvas, svg", True),
    ("03_reports",              f"{FRONTEND_BASE}/reports",    "h1",               True),
    ("04_backend_docs",         f"{BACKEND_BASE}/docs",        ".swagger-ui",      True),
    ("05_backend_health",       f"{BACKEND_BASE}/health",      None,               False),
    ("06_backend_regions",      f"{BACKEND_BASE}/regions",     None,               False),
    ("07_backend_sources",      f"{BACKEND_BASE}/sources",     None,               False),
    ("08_backend_dashboard_data", f"{BACKEND_BASE}/dashboard-data?period=90", None, False),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def _filename(label: str) -> Path:
    return OUT_DIR / f"{label}.png"


async def capture(page, label: str, url: str, wait_selector: str | None, full_page: bool):
    print(f"  📸  {label}  →  {url}")
    try:
        await page.goto(url, wait_until="networkidle", timeout=20_000)

        if wait_selector:
            try:
                await page.wait_for_selector(wait_selector, timeout=10_000)
            except PWTimeout:
                pass  # continue even if selector never appears

        # Extra wait for charts / map tiles to render
        await asyncio.sleep(2)

        path = str(_filename(label))
        await page.screenshot(path=path, full_page=full_page)
        print(f"         ✅  saved → {path}")
        return True

    except Exception as exc:
        print(f"         ⚠️  failed: {exc}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    print("\n🚀  ATHAR Screenshot Capture")
    print(f"    Output folder: {OUT_DIR}\n")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        # Desktop viewport (1440 × 900) — matches typical dashboard view
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
        )
        page = await context.new_page()

        for label, url, wait_sel, full in PAGES:
            ok = await capture(page, label, url, wait_sel, full)
            results.append((label, url, ok))

        await browser.close()

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'─'*55}")
    print(f"  ATHAR Screenshots — {ts}")
    print(f"{'─'*55}")
    for label, url, ok in results:
        status = "✅" if ok else "❌"
        print(f"  {status}  {label}")
    print(f"{'─'*55}")

    saved = sum(1 for _, _, ok in results if ok)
    print(f"\n  {saved}/{len(results)} screenshots saved to:  {OUT_DIR}\n")

    # Write a simple HTML index so you can view all at once
    _write_index(results, ts)


def _write_index(results, ts):
    """Generate an HTML gallery file for easy viewing."""
    rows = ""
    for label, url, ok in results:
        if ok:
            rows += f"""
      <div class="card">
        <h3>{label.replace('_', ' ').title()}</h3>
        <p class="url">{url}</p>
        <a href="{label}.png" target="_blank">
          <img src="{label}.png" alt="{label}" />
        </a>
      </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ATHAR — Screenshots</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #f1f5f9; margin: 0; padding: 24px; }}
    h1   {{ color: #0c4a6e; margin-bottom: 4px; }}
    p.ts {{ color: #64748b; font-size: 13px; margin-bottom: 32px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(620px, 1fr)); gap: 24px; }}
    .card {{ background: #fff; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,.1); }}
    .card h3   {{ margin: 0 0 4px; color: #1e293b; font-size: 15px; }}
    .card .url {{ margin: 0 0 10px; color: #64748b; font-size: 12px; }}
    .card img  {{ width: 100%; border-radius: 6px; border: 1px solid #e2e8f0; cursor: pointer; }}
  </style>
</head>
<body>
  <h1>أثر (ATHAR) — Screenshot Gallery</h1>
  <p class="ts">Generated: {ts}</p>
  <div class="grid">
    {rows}
  </div>
</body>
</html>"""

    index_path = OUT_DIR / "index.html"
    index_path.write_text(html, encoding="utf-8")
    print(f"  🖼️   HTML gallery → {index_path}\n")


if __name__ == "__main__":
    asyncio.run(main())
