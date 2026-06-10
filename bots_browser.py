"""
bots_browser.py  —  Agentic Browser Bot System
Real headless Chromium: opens pages, loads JS, waits for ads, scrolls, reads.

Install:
    pip install playwright --break-system-packages
    playwright install chromium

Run:
    python bots_browser.py                          # default 50 bots, 5 concurrent
    python bots_browser.py --bots 200 --concurrency 8
    python bots_browser.py --bots 10 --visible      # watch browser windows (debug)
"""

import asyncio
import random
import argparse
import json
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── CONFIG ─────────────────────────────────────────────────────────────────
TARGET      = "https://attacksveteran.com/qf4r7p808?key=c8cf5245691241e11abac3286b071e10"
TOTAL_BOTS  = 20000
CONCURRENCY = 5
HEADLESS    = True

# ── PAGES ──────────────────────────────────────────────────────────────────
# Single landing/raffle page — TARGET is already the full entry URL
PAGES = [""]

# ── DEVICES (UA + viewport + sec-ch-ua fingerprint) ────────────────────────
DEVICES = [
    # ── Samsung ──
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 915}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy S24+", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 915}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy S24", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 360, "height": 780}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy S23 Ultra", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 915}, "mobile": True, "sec_ch_ua": '"Chromium";v="120", "Google Chrome";v="120"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy S23", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 360, "height": 780}, "mobile": True, "sec_ch_ua": '"Chromium";v="119", "Google Chrome";v="119"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy A54", "ua": "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 360, "height": 800}, "mobile": True, "sec_ch_ua": '"Chromium";v="122", "Google Chrome";v="122"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy A34", "ua": "Mozilla/5.0 (Linux; Android 13; SM-A346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 360, "height": 800}, "mobile": True, "sec_ch_ua": '"Chromium";v="120", "Google Chrome";v="120"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy Z Fold 5", "ua": "Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 904, "height": 832}, "mobile": True, "sec_ch_ua": '"Chromium";v="120", "Google Chrome";v="120"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Samsung Galaxy Tab S9", "ua": "Mozilla/5.0 (Linux; Android 13; SM-X916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
     "viewport": {"width": 1600, "height": 2560}, "mobile": False, "sec_ch_ua": '"Chromium";v="120", "Google Chrome";v="120"', "platform": '"Android"', "ch_mobile": "?0"},

    # ── Google Pixel ──
    {"name": "Google Pixel 8 Pro", "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 892}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Google Pixel 8", "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 393, "height": 851}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Google Pixel 7a", "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 892}, "mobile": True, "sec_ch_ua": '"Chromium";v="118", "Google Chrome";v="118"', "platform": '"Android"', "ch_mobile": "?1"},

    # ── OnePlus / Xiaomi ──
    {"name": "OnePlus 12", "ua": "Mozilla/5.0 (Linux; Android 14; CPH2583) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 412, "height": 919}, "mobile": True, "sec_ch_ua": '"Chromium";v="123", "Google Chrome";v="123"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Xiaomi 14 Pro", "ua": "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 393, "height": 873}, "mobile": True, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Android"', "ch_mobile": "?1"},
    {"name": "Xiaomi Redmi Note 13 Pro", "ua": "Mozilla/5.0 (Linux; Android 13; 23076RA4BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
     "viewport": {"width": 393, "height": 873}, "mobile": True, "sec_ch_ua": '"Chromium";v="119", "Google Chrome";v="119"', "platform": '"Android"', "ch_mobile": "?1"},

    # ── iPhones ──
    {"name": "iPhone 15 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
     "viewport": {"width": 430, "height": 932}, "mobile": True, "sec_ch_ua": '"Safari";v="17"', "platform": '"iOS"', "ch_mobile": "?1"},
    {"name": "iPhone 15 Pro", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
     "viewport": {"width": 393, "height": 852}, "mobile": True, "sec_ch_ua": '"Safari";v="17"', "platform": '"iOS"', "ch_mobile": "?1"},
    {"name": "iPhone 15", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
     "viewport": {"width": 390, "height": 844}, "mobile": True, "sec_ch_ua": '"Safari";v="17"', "platform": '"iOS"', "ch_mobile": "?1"},
    {"name": "iPhone 14 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
     "viewport": {"width": 430, "height": 932}, "mobile": True, "sec_ch_ua": '"Safari";v="16"', "platform": '"iOS"', "ch_mobile": "?1"},
    {"name": "iPhone 13", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
     "viewport": {"width": 390, "height": 844}, "mobile": True, "sec_ch_ua": '"Safari";v="15"', "platform": '"iOS"', "ch_mobile": "?1"},

    # ── Desktops ──
    {"name": "MacBook Air M2 (Chrome)", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
     "viewport": {"width": 1440, "height": 900}, "mobile": False, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"macOS"', "ch_mobile": "?0"},
    {"name": "MacBook Pro M3 (Safari)", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
     "viewport": {"width": 1440, "height": 900}, "mobile": False, "sec_ch_ua": '"Safari";v="17"', "platform": '"macOS"', "ch_mobile": "?0"},
    {"name": "Dell XPS 15 (Chrome)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
     "viewport": {"width": 1920, "height": 1080}, "mobile": False, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Windows"', "ch_mobile": "?0"},
    {"name": "HP Spectre x360 (Chrome)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
     "viewport": {"width": 1920, "height": 1080}, "mobile": False, "sec_ch_ua": '"Chromium";v="122", "Google Chrome";v="122"', "platform": '"Windows"', "ch_mobile": "?0"},
    {"name": "Lenovo ThinkPad (Firefox)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
     "viewport": {"width": 1366, "height": 768}, "mobile": False, "sec_ch_ua": '"Firefox";v="125"', "platform": '"Windows"', "ch_mobile": "?0"},
    {"name": "Ubuntu Desktop (Chrome)", "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
     "viewport": {"width": 1920, "height": 1080}, "mobile": False, "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124"', "platform": '"Linux"', "ch_mobile": "?0"},
]

# ── LOCATIONS ──────────────────────────────────────────────────────────────
LOCATIONS = [
    {"country": "United States",  "lang": "en-US", "tz": "America/New_York",              "ref": "https://www.google.com/"},
    {"country": "United States",  "lang": "en-US", "tz": "America/Chicago",               "ref": "https://www.bing.com/"},
    {"country": "United States",  "lang": "en-US", "tz": "America/Los_Angeles",           "ref": "https://twitter.com/"},
    {"country": "United Kingdom", "lang": "en-GB", "tz": "Europe/London",                 "ref": "https://www.google.co.uk/"},
    {"country": "Canada",         "lang": "en-CA", "tz": "America/Toronto",               "ref": "https://www.google.ca/"},
    {"country": "Australia",      "lang": "en-AU", "tz": "Australia/Sydney",              "ref": "https://www.google.com.au/"},
    {"country": "Germany",        "lang": "de-DE", "tz": "Europe/Berlin",                 "ref": "https://www.google.de/"},
    {"country": "France",         "lang": "fr-FR", "tz": "Europe/Paris",                  "ref": "https://www.google.fr/"},
    {"country": "Netherlands",    "lang": "nl-NL", "tz": "Europe/Amsterdam",              "ref": "https://www.google.nl/"},
    {"country": "India",          "lang": "en-IN", "tz": "Asia/Kolkata",                  "ref": "https://www.google.co.in/"},
    {"country": "Singapore",      "lang": "en-SG", "tz": "Asia/Singapore",               "ref": "https://www.google.com.sg/"},
    {"country": "South Africa",   "lang": "en-ZA", "tz": "Africa/Johannesburg",           "ref": "https://www.google.co.za/"},
    {"country": "Nigeria",        "lang": "en-NG", "tz": "Africa/Lagos",                  "ref": "https://www.google.com.ng/"},
    {"country": "Ghana",          "lang": "en-GH", "tz": "Africa/Accra",                  "ref": "https://www.google.com.gh/"},
    {"country": "Kenya",          "lang": "en-KE", "tz": "Africa/Nairobi",               "ref": "https://www.google.co.ke/"},
    {"country": "Japan",          "lang": "ja-JP", "tz": "Asia/Tokyo",                    "ref": "https://www.google.co.jp/"},
    {"country": "South Korea",    "lang": "ko-KR", "tz": "Asia/Seoul",                    "ref": "https://www.google.co.kr/"},
    {"country": "UAE",            "lang": "ar-AE", "tz": "Asia/Dubai",                    "ref": "https://www.google.ae/"},
    {"country": "Brazil",         "lang": "pt-BR", "tz": "America/Sao_Paulo",             "ref": "https://www.google.com.br/"},
    {"country": "Mexico",         "lang": "es-MX", "tz": "America/Mexico_City",           "ref": "https://www.google.com.mx/"},
    {"country": "Sweden",         "lang": "sv-SE", "tz": "Europe/Stockholm",              "ref": "https://www.google.se/"},
    {"country": "Ireland",        "lang": "en-IE", "tz": "Europe/Dublin",                 "ref": "https://www.google.ie/"},
    {"country": "New Zealand",    "lang": "en-NZ", "tz": "Pacific/Auckland",              "ref": "https://www.google.co.nz/"},
    {"country": "Argentina",      "lang": "es-AR", "tz": "America/Argentina/Buenos_Aires","ref": "https://www.google.com.ar/"},
]

# ── STATS ──────────────────────────────────────────────────────────────────
stats = {"completed": 0, "pages_loaded": 0, "ad_slots_seen": 0, "errors": 0}
stats_lock = asyncio.Lock()
log_lock   = asyncio.Lock()


def ts():
    return datetime.now().strftime("%H:%M:%S")


async def log(msg):
    async with log_lock:
        print(msg)


# ── PAGE READING ────────────────────────────────────────────────────────────
async def read_page_content(page):
    """Extract title + first 200 chars of text — proves the page actually loaded."""
    try:
        title = await page.title()
        text  = await page.evaluate("""() => {
            const body = document.body;
            if (!body) return '';
            return body.innerText.replace(/\\s+/g, ' ').trim().slice(0, 200);
        }""")
        return title, text
    except Exception:
        return "?", ""


async def check_ads(page):
    """Detect ad slots that initialized after JS ran."""
    try:
        return await page.evaluate("""() => {
            const sel = [
                'iframe[id*="google_ads"]',
                'iframe[src*="googleads"]',
                'iframe[src*="doubleclick"]',
                'ins.adsbygoogle',
                '[data-ad-client]',
                '[id*="div-gpt-ad"]',
                '[class*="adsbygoogle"]',
                'iframe[src*="googlesyndication"]',
            ];
            return sel.reduce((n, s) => n + document.querySelectorAll(s).length, 0);
        }""")
    except Exception:
        return 0


async def human_scroll(page):
    """Scroll naturally through the page — triggers viewability signals."""
    try:
        height = await page.evaluate("document.body.scrollHeight || 1000")
        steps  = random.randint(4, 9)
        pos    = 0
        for _ in range(steps):
            # Scroll down in chunks
            chunk = random.randint(150, 400)
            pos   = min(pos + chunk, height)
            await page.evaluate(f"window.scrollTo({{top: {pos}, behavior: 'smooth'}})")
            await asyncio.sleep(random.uniform(0.6, 2.5))
        # Scroll back up a bit (natural reading behaviour)
        await page.evaluate(f"window.scrollTo({{top: {int(pos * 0.4)}, behavior: 'smooth'}})")
        await asyncio.sleep(random.uniform(0.5, 1.5))
    except Exception:
        pass


async def wait_for_ads(page, timeout=8):
    """Give ad SDK time to fire after domcontentloaded."""
    try:
        await page.wait_for_load_state("networkidle", timeout=timeout * 1000)
    except PWTimeout:
        pass  # networkidle timeout is fine — ads may still have loaded


# ── SINGLE BOT ─────────────────────────────────────────────────────────────
async def run_bot(bot_id, playwright):
    device   = random.choice(DEVICES)
    location = random.choice(LOCATIONS)

    extra_headers = {
        "sec-ch-ua":          device["sec_ch_ua"],
        "sec-ch-ua-mobile":   device["ch_mobile"],
        "sec-ch-ua-platform": device["platform"],
        "Accept-Language":    f"{location['lang']},en;q=0.9",
        "Referer":            location["ref"],
        "Cache-Control":      "no-cache",
        "Pragma":             "no-cache",
    }

    browser = await playwright.chromium.launch(headless=HEADLESS)
    context = await browser.new_context(
        user_agent         = device["ua"],
        viewport           = device["viewport"],
        is_mobile          = device["mobile"],
        locale             = location["lang"],
        timezone_id        = location["tz"],
        extra_http_headers = extra_headers,
    )

    # Block media files — keep JS/CSS (needed for ads)
    await context.route(
        "**/*.{png,jpg,jpeg,gif,svg,woff,woff2,ttf,eot,mp4,webm}",
        lambda r: r.abort()
    )

    page = await context.new_page()

    # Journey: homepage → 2-4 random pages
    # Single page site — just load TARGET once per bot
    journey = [""]

    for i, path in enumerate(journey):
        url = TARGET + path
        try:
            # ── LOAD PAGE ──────────────────────────────────────────────────
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=25_000)
            status = resp.status if resp else 0

            # ── WAIT FOR JS / ADS ──────────────────────────────────────────
            await wait_for_ads(page)

            # ── READ THE PAGE ──────────────────────────────────────────────
            title, preview = await read_page_content(page)

            # ── SCROLL LIKE A HUMAN ────────────────────────────────────────
            await human_scroll(page)

            # ── COUNT AD SLOTS ─────────────────────────────────────────────
            ads = await check_ads(page)

            # ── DWELL (realistic reading time) ─────────────────────────────
            dwell = random.randint(8, 45)
            await asyncio.sleep(dwell)

            # ── LOG ────────────────────────────────────────────────────────
            status_mark = "✓" if status < 400 else f"✗{status}"
            ad_note     = f"ads:{ads}" if ads > 0 else "no ads"
            await log(
                f"[{ts()}] {status_mark} Bot#{bot_id:04d} | {device['name'][:20]:<20} | "
                f"{location['country']:<14} | {path:<38} | {ad_note} | \"{title[:40]}\""
            )

            async with stats_lock:
                stats["pages_loaded"]  += 1
                stats["ad_slots_seen"] += ads

            # Update referer for next page (internal navigation)
            extra_headers["Referer"] = url
            await context.set_extra_http_headers(extra_headers)

        except PWTimeout:
            await log(f"[{ts()}] ✗ Bot#{bot_id:04d} | TIMEOUT | {url}")
            async with stats_lock:
                stats["errors"] += 1
        except Exception as e:
            await log(f"[{ts()}] ✗ Bot#{bot_id:04d} | ERROR | {str(e)[:60]}")
            async with stats_lock:
                stats["errors"] += 1

    await browser.close()
    async with stats_lock:
        stats["completed"] += 1


# ── STATS PRINTER ──────────────────────────────────────────────────────────
async def stats_printer(total):
    while True:
        await asyncio.sleep(30)
        async with stats_lock:
            s = stats.copy()
        pct = int(s["completed"] / total * 100)
        print(
            f"\n══ STATS [{pct}%] ══  Done: {s['completed']}/{total} | "
            f"Pages loaded: {s['pages_loaded']} | "
            f"Ad slots seen: {s['ad_slots_seen']} | "
            f"Errors: {s['errors']} ══\n"
        )
        if s["completed"] >= total:
            break


# ── MAIN ───────────────────────────────────────────────────────────────────
async def main(total_bots, concurrency):
    print(f"\n🚀  Agentic Browser Bot — SimpleRead")
    print(f"    Target      : {TARGET}")
    print(f"    Bots        : {total_bots}")
    print(f"    Concurrency : {concurrency} parallel browsers")
    print(f"    Devices     : {len(DEVICES)}  |  Locations: {len(LOCATIONS)}")
    print(f"    Mode        : {'headless' if HEADLESS else 'visible (debug)'}\n")

    asyncio.create_task(stats_printer(total_bots))
    semaphore = asyncio.Semaphore(concurrency)

    async def guarded(bot_id, pw):
        async with semaphore:
            await run_bot(bot_id, pw)

    async with async_playwright() as pw:
        tasks = [guarded(i, pw) for i in range(1, total_bots + 1)]
        await asyncio.gather(*tasks)

    print(f"\n✅  All bots finished!")
    print(json.dumps(stats, indent=2))


# ── ENTRY POINT ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agentic browser bot system")
    parser.add_argument("--bots",        type=int, default=TOTAL_BOTS,  help="Number of bots")
    parser.add_argument("--concurrency", type=int, default=CONCURRENCY, help="Parallel browsers")
    parser.add_argument("--visible",     action="store_true",           help="Show browser (debug)")
    args = parser.parse_args()

    if args.visible:
        HEADLESS = False

    asyncio.run(main(args.bots, args.concurrency))
