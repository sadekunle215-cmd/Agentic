import requests
import random
import time
import threading
import argparse
from datetime import datetime

# ── CONFIG ─────────────────────────────────────────────
TARGET     = "https://attacksveteran.com/qf4r7p808?key=c8cf5245691241e11abac3286b071e10"
SPAWN_RATE = 10

# ── PAGES ───────────────────────────────────────────────
PAGES = [
    "/",
    "/article.html",
    "/category.html",
    "/about.html",
    "/news/ai-revolution-2026.html",
    "/news/climate-accord-update.html",
    "/news/global-economy-recovery.html",
    "/news/tech-giants-antitrust.html",
    "/news/space-exploration-mars.html",
    "/news/crypto-market-surge.html",
    "/news/health-breakthrough-cancer.html",
    "/news/us-election-2026.html",
    "/news/ukraine-peace-talks.html",
    "/news/china-economy-slowdown.html",
    "/news/renewable-energy-record.html",
    "/news/social-media-regulation.html",
    "/news/housing-crisis-solutions.html",
    "/news/quantum-computing-leap.html",
    "/news/pandemic-preparedness.html",
    "/news/africa-tech-boom.html",
    "/news/middle-east-tensions.html",
    "/news/stock-market-record.html",
    "/news/electric-vehicles-future.html",
    "/news/education-reform-global.html",
    "/news/food-security-crisis.html",
    "/news/water-shortage-warning.html",
    "/news/nato-expansion-update.html",
    "/news/billionaire-space-race.html",
    "/news/mental-health-crisis.html",
    "/news/immigration-policy-shift.html",
    "/news/semiconductor-shortage.html",
    "/news/nuclear-energy-comeback.html",
    "/news/social-inequality-report.html",
]

# ── DEVICES ─────────────────────────────────────────────
DEVICES = [
    {"name": "Samsung Galaxy S24 Ultra",       "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S24+",            "ua": "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S24",             "ua": "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S23 Ultra",       "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S23",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A54",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A34",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Z Fold 5",        "ua": "Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Z Flip 5",        "ua": "Mozilla/5.0 (Linux; Android 13; SM-F731B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Tab S9 Ultra",    "ua": "Mozilla/5.0 (Linux; Android 13; SM-X916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Google Pixel 8 Pro",             "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 8",                 "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 7a",                "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus 12",                     "ua": "Mozilla/5.0 (Linux; Android 14; CPH2583) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus 11",                     "ua": "Mozilla/5.0 (Linux; Android 13; CPH2449) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus Nord 3",                 "ua": "Mozilla/5.0 (Linux; Android 13; CPH2491) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi 14 Pro",                  "ua": "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi 14",                      "ua": "Mozilla/5.0 (Linux; Android 14; 23127PN0CC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi Redmi Note 13 Pro",       "ua": "Mozilla/5.0 (Linux; Android 13; 23076RA4BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi POCO X6 Pro",             "ua": "Mozilla/5.0 (Linux; Android 14; 23122PC75G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Oppo Find X7 Ultra",             "ua": "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Realme GT 5 Pro",                "ua": "Mozilla/5.0 (Linux; Android 14; RMX3888) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Vivo X100 Pro",                  "ua": "Mozilla/5.0 (Linux; Android 14; V2309A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Edge 40 Pro",           "ua": "Mozilla/5.0 (Linux; Android 13; XT2301-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"},
    {"name": "iPhone 15 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15 Pro",                  "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Pro",                  "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone SE (3rd Gen)",            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Pro 12.9 M2",               "ua": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Air 5th Gen",               "ua": "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"},
    {"name": "Dell XPS 15 (Chrome)",           "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "HP Spectre x360 (Chrome)",       "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"},
    {"name": "Lenovo ThinkPad X1 (Chrome)",    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Microsoft Surface Pro 9 (Edge)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
    {"name": "Lenovo ThinkPad X1 (Firefox)",   "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"},
    {"name": "MacBook Pro M3 (Safari)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"},
    {"name": "MacBook Air M2 (Chrome)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "Ubuntu Desktop (Chrome)",        "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "Fedora Desktop (Firefox)",       "ua": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"},
]

# ── LOCATIONS ───────────────────────────────────────────
LOCATIONS = [
    {"country": "United States",  "lang": "en-US,en;q=0.9", "ref": "https://www.google.com/"},
    {"country": "United States",  "lang": "en-US,en;q=0.9", "ref": "https://www.bing.com/"},
    {"country": "United States",  "lang": "en-US,en;q=0.9", "ref": "https://twitter.com/"},
    {"country": "United Kingdom", "lang": "en-GB,en;q=0.9", "ref": "https://www.google.co.uk/"},
    {"country": "Canada",         "lang": "en-CA,en;q=0.9", "ref": "https://www.google.ca/"},
    {"country": "Australia",      "lang": "en-AU,en;q=0.9", "ref": "https://www.google.com.au/"},
    {"country": "Germany",        "lang": "de-DE,de;q=0.9,en;q=0.8", "ref": "https://www.google.de/"},
    {"country": "France",         "lang": "fr-FR,fr;q=0.9,en;q=0.8", "ref": "https://www.google.fr/"},
    {"country": "Netherlands",    "lang": "nl-NL,nl;q=0.9,en;q=0.8", "ref": "https://www.google.nl/"},
    {"country": "Spain",          "lang": "es-ES,es;q=0.9,en;q=0.8", "ref": "https://www.google.es/"},
    {"country": "Italy",          "lang": "it-IT,it;q=0.9,en;q=0.8", "ref": "https://www.google.it/"},
    {"country": "Brazil",         "lang": "pt-BR,pt;q=0.9,en;q=0.8", "ref": "https://www.google.com.br/"},
    {"country": "India",          "lang": "en-IN,en;q=0.9,hi;q=0.8", "ref": "https://www.google.co.in/"},
    {"country": "Singapore",      "lang": "en-SG,en;q=0.9",          "ref": "https://www.google.com.sg/"},
    {"country": "South Africa",   "lang": "en-ZA,en;q=0.9",          "ref": "https://www.google.co.za/"},
    {"country": "Nigeria",        "lang": "en-NG,en;q=0.9",          "ref": "https://www.google.com.ng/"},
    {"country": "Ghana",          "lang": "en-GH,en;q=0.9",          "ref": "https://www.google.com.gh/"},
    {"country": "Kenya",          "lang": "en-KE,en;q=0.9",          "ref": "https://www.google.co.ke/"},
    {"country": "Japan",          "lang": "ja-JP,ja;q=0.9,en;q=0.8", "ref": "https://www.google.co.jp/"},
    {"country": "South Korea",    "lang": "ko-KR,ko;q=0.9,en;q=0.8", "ref": "https://www.google.co.kr/"},
    {"country": "UAE",            "lang": "ar-AE,ar;q=0.9,en;q=0.8", "ref": "https://www.google.ae/"},
    {"country": "Sweden",         "lang": "sv-SE,sv;q=0.9,en;q=0.8", "ref": "https://www.google.se/"},
    {"country": "Mexico",         "lang": "es-MX,es;q=0.9,en;q=0.8", "ref": "https://www.google.com.mx/"},
    {"country": "New Zealand",    "lang": "en-NZ,en;q=0.9",          "ref": "https://www.google.co.nz/"},
    {"country": "Ireland",        "lang": "en-IE,en;q=0.9",          "ref": "https://www.google.ie/"},
]

# ── STATS ───────────────────────────────────────────────
stats = {"success": 0, "fail": 0, "active": 0}
stats_lock = threading.Lock()


def log(bot_id, device, location, page, status, dwell):
    now  = datetime.now().strftime("%H:%M:%S")
    mark = "✓" if status == 200 else "✗"
    print(f"[{now}] {mark} Bot#{bot_id:04d} | {device['name']} | {location['country']} | {page} | {status} | dwell {dwell}s")


def run_bot(bot_id):
    device   = random.choice(DEVICES)
    location = random.choice(LOCATIONS)
    session  = requests.Session()
    visited  = []

    headers = {
        "User-Agent":                device["ua"],
        "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":           location["lang"],
        "Accept-Encoding":           "gzip, deflate, br",
        "Connection":                "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest":            "document",
        "Sec-Fetch-Mode":            "navigate",
        "Sec-Fetch-Site":            "cross-site",
        "Referer":                   location["ref"],
        "Cache-Control":             "max-age=0",
    }

    with stats_lock:
        stats["active"] += 1

    try:
        num_pages = random.randint(2, 5)
        journey   = ["/"] + random.sample(PAGES[1:], k=num_pages)

        for page in journey:
            if visited:
                headers["Referer"]        = TARGET + visited[-1]
                headers["Sec-Fetch-Site"] = "same-origin"

            try:
                url  = TARGET + page
                resp = session.get(url, headers=headers, timeout=15)
                dwell = random.randint(30, 120)
                log(bot_id, device, location, page, resp.status_code, dwell)

                with stats_lock:
                    if resp.status_code in (200, 404):
                        stats["success"] += 1
                    else:
                        stats["fail"] += 1

                visited.append(page)
                time.sleep(dwell)

            except Exception:
                with stats_lock:
                    stats["fail"] += 1

    finally:
        with stats_lock:
            stats["active"] -= 1


def print_stats():
    while True:
        time.sleep(60)
        with stats_lock:
            print(f"\n══ STATS ══ Active: {stats['active']} | ✓ Success: {stats['success']} | ✗ Failed: {stats['fail']} ══\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agentic bot system")
    parser.add_argument("--bots", type=int, default=500, help="Number of bots to run")
    args = parser.parse_args()

    TOTAL_BOTS = args.bots

    print(f"🚀 Launching {TOTAL_BOTS} bots → {TARGET}")
    print(f"   Devices: {len(DEVICES)} | Locations: {len(LOCATIONS)} | Pages: {len(PAGES)}")
    print(f"   Dwell time: 30s–120s per page\n")

    threading.Thread(target=print_stats, daemon=True).start()

    threads = []
    for i in range(1, TOTAL_BOTS + 1):
        t = threading.Thread(target=run_bot, args=(i,), daemon=True)
        t.start()
        threads.append(t)
        if i % SPAWN_RATE == 0:
            print(f"[+] {i} bots launched...")
            time.sleep(1)

    print(f"\n✅ All {TOTAL_BOTS} bots running!\n")

    for t in threads:
        t.join()
