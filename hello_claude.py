import asyncio
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

INTERVAL_HOURS = 5
USER_DATA_DIR = str(Path.home() / ".claude_browser_session")

# Playwright can only automate Chromium-based browsers.
# Tries Chrome first (most common), then Edge (always present on Windows).
BROWSER_CHANNELS = ["chrome", "msedge"]

async def send_hello():
    async with async_playwright() as p:
        context = None
        for channel in BROWSER_CHANNELS:
            try:
                context = await p.chromium.launch_persistent_context(
                    USER_DATA_DIR,
                    channel=channel,
                    headless=False,  # set True after first login
                )
                break
            except Exception:
                continue

        if context is None:
            raise RuntimeError(
                f"No supported browser found. Install Chrome or Edge, then retry."
            )

        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto("https://claude.ai/new", wait_until="networkidle")

        chat_input = page.locator('[contenteditable="true"]').first
        await chat_input.click()
        await chat_input.fill("hello")
        await chat_input.press("Enter")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sent 'hello' to Claude.")

        await page.wait_for_timeout(2000)
        await context.close()

async def main():
    print(f"Starting — will send 'hello' every {INTERVAL_HOURS} hours. Press Ctrl+C to stop.\n")
    while True:
        await send_hello()
        await asyncio.sleep(INTERVAL_HOURS * 3600)

if __name__ == "__main__":
    asyncio.run(main())
