import asyncio
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

INTERVAL_HOURS = 5
DEBUG_PORT = 9222
USER_DATA_DIR = str(Path.home() / ".claude_browser_session")

def find_chrome():
    """Locate a real Chrome executable across platforms."""
    candidates = [
        shutil.which("chrome"),
        shutil.which("google-chrome"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
    ]
    for path in candidates:
        if path and Path(path).exists():
            return path
    return None

async def send_hello(browser):
    context = browser.contexts[0]
    page = context.pages[0] if context.pages else await context.new_page()

    # domcontentloaded (not networkidle) — claude.ai never goes network-idle
    await page.goto("https://claude.ai/new", wait_until="domcontentloaded", timeout=60000)

    # Wait for the input. On first run this also gives you time to log in
    # and clear any Cloudflare challenge manually (up to 2 minutes).
    chat_input = page.locator('[contenteditable="true"]').first
    await chat_input.wait_for(state="visible", timeout=120000)

    await chat_input.click()
    await chat_input.fill("hello")
    await chat_input.press("Enter")

    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Sent 'hello' to Claude.")
    await page.wait_for_timeout(2000)

async def main():
    chrome = find_chrome()
    if not chrome:
        print("Google Chrome not found. Install it from https://google.com/chrome and retry.")
        sys.exit(1)

    # Launch the user's REAL Chrome with remote debugging. Because Playwright
    # only *connects* (does not launch), no automation flags are set and
    # Cloudflare treats the browser as a normal human session.
    proc = subprocess.Popen([
        chrome,
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
    ])
    time.sleep(3)  # let Chrome open the debugging port

    print(f"Starting — will send 'hello' every {INTERVAL_HOURS} hours. Press Ctrl+C to stop.\n")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
        try:
            while True:
                await send_hello(browser)
                await asyncio.sleep(INTERVAL_HOURS * 3600)
        finally:
            await browser.close()
            proc.terminate()

if __name__ == "__main__":
    asyncio.run(main())
