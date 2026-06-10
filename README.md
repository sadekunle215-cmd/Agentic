# Agentic — Browser Bot System

Simulates 20,000 real-looking users browsing your site using actual headless Chromium.
Each bot opens the page, loads JavaScript, waits for ads to initialize, scrolls naturally, and reads content — exactly like a real visitor.

## Setup

```bash
pip install playwright --break-system-packages
playwright install chromium
```

## Run

```bash
python bots_browser.py                         # 20k bots, 5 concurrent
python bots_browser.py --concurrency 8         # faster
python bots_browser.py --bots 100 --visible    # debug, watch browser
```

## Files

| File             | Purpose                                    |
|------------------|--------------------------------------------|
| bots_browser.py  | Main bot — real browser, JS, ad detection  |
| bots.py          | Legacy HTTP-only bot (kept for reference)  |
| locustfile.py    | Locust load tester (HTTP only)             |
| requirements.txt | Python dependencies                        |
