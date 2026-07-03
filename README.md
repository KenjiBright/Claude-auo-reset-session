# Claude Auto Reset Session

A Python script that automatically sends "hello" to [claude.ai](https://claude.ai) every 5 hours using browser automation. No API key required — it uses your existing browser session.

## Requirements

- Python 3.8+
- Chrome or Microsoft Edge installed

## Installation

```sh
pip install playwright
playwright install
```

## Usage

### First run

```sh
python hello_claude.py
```

A browser window will open. **Log in to claude.ai manually.** The script will then type "hello" and send it automatically. Your session is saved to `~/.claude_browser_session` so you only need to log in once.

### Subsequent runs

After the first login, open `hello_claude.py` and change:

```python
headless=False,  # set True after first login
```

to:

```python
headless=True,
```

The script will then run silently in the background.

## How it works

- Uses [Playwright](https://playwright.dev/python/) to open Chrome (or Edge if Chrome is not found)
- Navigates to `claude.ai/new`, types "hello", and presses Enter
- Waits 5 hours, then repeats
- Press `Ctrl+C` to stop

## Browser support

The script supports Chromium-based browsers only (Playwright limitation):

| Browser | Supported |
|---------|-----------|
| Chrome  | Yes (tried first) |
| Edge    | Yes (fallback, always available on Windows) |
| Firefox | No |
| Safari  | No |

## Output

```
Starting — will send 'hello' every 5 hours. Press Ctrl+C to stop.

[2026-07-03 12:00:00] Sent 'hello' to Claude.
[2026-07-03 17:00:00] Sent 'hello' to Claude.
```
