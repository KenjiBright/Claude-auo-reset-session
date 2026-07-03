# Claude Auto Reset Session

A Python script that automatically sends "hello" to [claude.ai](https://claude.ai) every 5 hours using browser automation. No API key required — it drives a real Google Chrome window using your own login session.

## Requirements

- Python 3.8+
- **Google Chrome** installed (a real Chrome install is required — not Playwright's bundled Chromium)

## Installation

```sh
pip install playwright
playwright install
```

> On Windows, if `pip`/`python` aren't recognized, install Python from
> [python.org](https://python.org/downloads) and check **"Add Python to PATH"**,
> then use `python -m pip install playwright`.

## Usage

### First run

```sh
python hello_claude.py
```

Chrome opens to claude.ai. **Log in manually** and, if a Cloudflare check appears, clear it once — the script waits up to 2 minutes for the chat box to appear. Once you're in, it types "hello" and sends it. Your session is saved to `~/.claude_browser_session`, so you only log in once.

### Subsequent runs

Just run `python hello_claude.py` again. It reuses the saved session and Cloudflare clearance — no login needed. Leave the window open; every 5 hours it re-navigates and sends "hello". Press `Ctrl+C` to stop.

## How it works

Cloudflare's bot protection blocks browsers that Playwright *launches* directly, because Playwright sets automation flags (`navigator.webdriver`, `--enable-automation`) that get fingerprinted. To avoid this, the script:

1. Launches your **real Google Chrome** as a separate process with remote debugging enabled (`--remote-debugging-port=9222`) and a dedicated profile directory.
2. **Connects** to that Chrome over CDP with `playwright.chromium.connect_over_cdp(...)` — it only attaches, it doesn't launch. So no automation flags are set and Cloudflare treats it as a normal human session.
3. Navigates to `claude.ai/new` using `wait_until="domcontentloaded"` (claude.ai never reaches network-idle, which is why the old `networkidle` wait timed out), then waits for the chat input, types "hello", and presses Enter.
4. Sleeps 5 hours and repeats.

## Troubleshooting

- **"Google Chrome not found"** — install Chrome from [google.com/chrome](https://www.google.com/chrome/), or edit the `candidates` list in `find_chrome()` to point at your Chrome path.
- **Cloudflare still blocking** — make sure no other Chrome instance is already using the `~/.claude_browser_session` profile, and complete the human check manually on first run.
- **Only Chrome is supported.** Playwright can automate Chromium-based browsers only; this tool specifically drives real Chrome to defeat Cloudflare.

## Output

```
Starting — will send 'hello' every 5 hours. Press Ctrl+C to stop.

[2026-07-03 12:00:00] Sent 'hello' to Claude.
[2026-07-03 17:00:00] Sent 'hello' to Claude.
```
