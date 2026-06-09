from locust import HttpUser, task, between
import random
import time

# ── PAGES ──────────────────────────────────────────────
PAGES = [
    "/",
    "/article.html",
    "/category.html",
    "/about.html",
]

# ── REAL DEVICE USER AGENTS ────────────────────────────
DEVICES = [
    # Android Phones
    {"name": "Samsung Galaxy S24 Ultra",     "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A54",           "ua": "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 8 Pro",           "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 7",               "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus 12",                   "ua": "Mozilla/5.0 (Linux; Android 14; CPH2583) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi 14 Pro",                "ua": "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Oppo Find X7",                 "ua": "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Edge 40 Pro",         "ua": "Mozilla/5.0 (Linux; Android 13; XT2301-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"},
    {"name": "Realme GT 5 Pro",              "ua": "Mozilla/5.0 (Linux; Android 14; RMX3888) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Vivo X100 Pro",                "ua": "Mozilla/5.0 (Linux; Android 14; V2309A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    # iPhones
    {"name": "iPhone 15 Pro Max",            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15",                    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Pro",                "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13",                    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone SE (3rd Gen)",          "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    # iPads
    {"name": "iPad Pro 12.9 M2",             "ua": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Air 5th Gen",             "ua": "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Mini 6",                  "ua": "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1"},
    # Windows Desktops / Laptops
    {"name": "Dell XPS 15 (Chrome/Win11)",   "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "HP Spectre x360 (Edge/Win11)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
    {"name": "Lenovo ThinkPad X1 (Firefox)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"},
    {"name": "Asus ROG Zephyrus (Chrome)",   "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
    {"name": "Microsoft Surface Pro 9",      "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"},
    # Macs
    {"name": "MacBook Pro M3 (Safari)",      "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"},
    {"name": "MacBook Air M2 (Chrome)",      "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "iMac 24 (Firefox/Mac)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0"},
    # Android Tablets
    {"name": "Samsung Galaxy Tab S9 Ultra",  "ua": "Mozilla/5.0 (Linux; Android 13; SM-X916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Lenovo Tab P12 Pro",           "ua": "Mozilla/5.0 (Linux; Android 12; TB-Q706F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
]

# ── REFERRERS ──────────────────────────────────────────
REFERRERS = [
    "https://www.google.com/",
    "https://www.google.com/search?q=daily+news",
    "https://twitter.com/",
    "https://www.facebook.com/",
    "https://www.reddit.com/",
    "https://news.ycombinator.com/",
    "https://www.bing.com/search?q=latest+news",
    "https://duckduckgo.com/?q=world+news",
    "", "", "",  # Direct visits (weighted higher)
]

# ── LANGUAGES ──────────────────────────────────────────
LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-CA,en;q=0.9",
    "en-AU,en;q=0.8",
    "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8",
    "es-ES,es;q=0.9,en;q=0.8",
    "pt-BR,pt;q=0.9,en;q=0.8",
    "it-IT,it;q=0.9,en;q=0.8",
    "nl-NL,nl;q=0.9,en;q=0.8",
]


class RealUserBot(HttpUser):
    wait_time = between(30, 18000)  # 30 seconds to 5 hours dwell time

    def on_start(self):
        self.device   = random.choice(DEVICES)
        self.referrer = random.choice(REFERRERS)
        self.language = random.choice(LANGUAGES)
        self.session_pages = []

        self.headers = {
            "User-Agent":                self.device["ua"],
            "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language":           self.language,
            "Accept-Encoding":           "gzip, deflate, br",
            "Connection":                "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest":            "document",
            "Sec-Fetch-Mode":            "navigate",
            "Sec-Fetch-Site":            "cross-site" if self.referrer else "none",
            "Referer":                   self.referrer,
            "Cache-Control":             "max-age=0",
        }

        print(f"[+] Session started — {self.device['name']} | {self.language[:5]}")
        self._visit("/", entry=True)

    def _visit(self, page, entry=False):
        if not entry and self.session_pages:
            self.headers["Referer"]        = self.host + self.session_pages[-1]
            self.headers["Sec-Fetch-Site"] = "same-origin"

        with self.client.get(page, headers=self.headers, catch_response=True, name=page) as resp:
            if resp.status_code == 200:
                resp.success()
                self.session_pages.append(page)
            else:
                resp.failure(f"Status {resp.status_code}")

    @task(4)
    def browse_random(self):
        self._visit(random.choice(PAGES))

    @task(3)
    def read_article(self):
        self._visit("/")
        time.sleep(random.uniform(5, 20))
        self._visit("/article.html")

    @task(2)
    def browse_category_then_article(self):
        self._visit("/category.html")
        time.sleep(random.uniform(8, 25))
        self._visit("/article.html")

    @task(1)
    def visit_about(self):
        self._visit("/about.html")

    @task(1)
    def deep_session(self):
        for page in ["/", "/category.html", "/article.html", "/about.html"]:
            self._visit(page)
            time.sleep(random.uniform(15, 60))
