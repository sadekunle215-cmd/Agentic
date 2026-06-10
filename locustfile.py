from locust import HttpUser, task, between
import random
import time

# ── PAGES ──────────────────────────────────────────────
PAGES = [
    "/SimpleRead/",
    "/SimpleRead/article.html",
    "/SimpleRead/category.html",
    "/SimpleRead/about.html",
]

# ── 300 REAL DEVICE USER AGENTS ────────────────────────
DEVICES = [
    # ── Samsung Galaxy ──
    {"name": "Samsung Galaxy S24 Ultra",       "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S24+",            "ua": "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S24",             "ua": "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S23 Ultra",       "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S23+",            "ua": "Mozilla/5.0 (Linux; Android 13; SM-S916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S23",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S22 Ultra",       "ua": "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S22",             "ua": "Mozilla/5.0 (Linux; Android 12; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy S21 FE",          "ua": "Mozilla/5.0 (Linux; Android 12; SM-G990B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A54",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A53",             "ua": "Mozilla/5.0 (Linux; Android 12; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A34",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A346B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A24",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A245F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy A15",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-A155F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy M54",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-M546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy F54",             "ua": "Mozilla/5.0 (Linux; Android 13; SM-E546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Z Fold 5",        "ua": "Mozilla/5.0 (Linux; Android 13; SM-F946B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Z Flip 5",        "ua": "Mozilla/5.0 (Linux; Android 13; SM-F731B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Z Fold 4",        "ua": "Mozilla/5.0 (Linux; Android 12; SM-F936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"},
    {"name": "Samsung Galaxy Note 20 Ultra",   "ua": "Mozilla/5.0 (Linux; Android 11; SM-N986B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Mobile Safari/537.36"},

    # ── Google Pixel ──
    {"name": "Google Pixel 8 Pro",             "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 8",                 "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 8a",                "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 7 Pro",             "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 7",                 "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 7a",                "ua": "Mozilla/5.0 (Linux; Android 13; Pixel 7a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 6 Pro",             "ua": "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"},
    {"name": "Google Pixel 6a",                "ua": "Mozilla/5.0 (Linux; Android 12; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"},

    # ── OnePlus ──
    {"name": "OnePlus 12",                     "ua": "Mozilla/5.0 (Linux; Android 14; CPH2583) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus 11",                     "ua": "Mozilla/5.0 (Linux; Android 13; CPH2449) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus Nord 3",                 "ua": "Mozilla/5.0 (Linux; Android 13; CPH2491) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
    {"name": "OnePlus Nord CE 3 Lite",         "ua": "Mozilla/5.0 (Linux; Android 13; CPH2467) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"},

    # ── Xiaomi ──
    {"name": "Xiaomi 14 Pro",                  "ua": "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi 14",                      "ua": "Mozilla/5.0 (Linux; Android 14; 23127PN0CC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi 13T Pro",                 "ua": "Mozilla/5.0 (Linux; Android 13; 23078PND5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi Redmi Note 13 Pro",       "ua": "Mozilla/5.0 (Linux; Android 13; 23076RA4BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi Redmi Note 12",           "ua": "Mozilla/5.0 (Linux; Android 12; 22111317I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi POCO X6 Pro",             "ua": "Mozilla/5.0 (Linux; Android 14; 23122PC75G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Xiaomi POCO F5",                 "ua": "Mozilla/5.0 (Linux; Android 13; 23049PCD8G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},

    # ── Oppo / Realme ──
    {"name": "Oppo Find X7 Ultra",             "ua": "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Oppo Reno 11 Pro",               "ua": "Mozilla/5.0 (Linux; Android 14; CPH2599) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"},
    {"name": "Oppo A98",                       "ua": "Mozilla/5.0 (Linux; Android 13; CPH2529) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"},
    {"name": "Realme GT 5 Pro",                "ua": "Mozilla/5.0 (Linux; Android 14; RMX3888) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"},
    {"name": "Realme 12 Pro+",                 "ua": "Mozilla/5.0 (Linux; Android 14; RMX3840) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"},
    {"name": "Realme Narzo 60 Pro",            "ua": "Mozilla/5.0 (Linux; Android 13; RMX3741) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},

    # ── Vivo / Motorola ──
    {"name": "Vivo X100 Pro",                  "ua": "Mozilla/5.0 (Linux; Android 14; V2309A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"},
    {"name": "Vivo V29 Pro",                   "ua": "Mozilla/5.0 (Linux; Android 13; V2250) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Edge 40 Pro",           "ua": "Mozilla/5.0 (Linux; Android 13; XT2301-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Edge 40",               "ua": "Mozilla/5.0 (Linux; Android 13; XT2303-2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Moto G84",              "ua": "Mozilla/5.0 (Linux; Android 13; XT2347-2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"},
    {"name": "Motorola Moto G54",              "ua": "Mozilla/5.0 (Linux; Android 13; XT2343-4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"},

    # ── iPhones ──
    {"name": "iPhone 15 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15 Pro",                  "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15 Plus",                 "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 15",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Pro",                  "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14 Plus",                 "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 14",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13 Pro",                  "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 13 Mini",                 "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 12 Pro Max",              "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone 12",                      "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone SE (3rd Gen)",            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPhone SE (2nd Gen)",            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},

    # ── iPads ──
    {"name": "iPad Pro 12.9 M2",               "ua": "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Pro 11 M2",                 "ua": "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Air 5th Gen",               "ua": "Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Air 4th Gen",               "ua": "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1"},
    {"name": "iPad Mini 6",                    "ua": "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1"},
    {"name": "iPad 10th Gen",                  "ua": "Mozilla/5.0 (iPad; CPU OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"},
    {"name": "iPad 9th Gen",                   "ua": "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"},

    # ── Windows Laptops / Desktops (Chrome) ──
    {"name": "Dell XPS 15 (Chrome)",           "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "Dell XPS 13 (Chrome)",           "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
    {"name": "HP Spectre x360 (Chrome)",       "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"},
    {"name": "HP Envy 15 (Chrome)",            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"},
    {"name": "Lenovo ThinkPad X1 (Chrome)",    "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Lenovo IdeaPad 5 (Chrome)",      "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"name": "Asus ROG Zephyrus (Chrome)",     "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
    {"name": "Asus ZenBook Pro (Chrome)",      "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"},
    {"name": "Acer Swift 5 (Chrome)",          "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
    {"name": "MSI Raider GE78 (Chrome)",       "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"},
    # Windows Edge
    {"name": "Microsoft Surface Pro 9 (Edge)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"},
    {"name": "HP Spectre x360 (Edge)",         "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"},
    {"name": "Dell Inspiron 16 (Edge)",        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"},
    {"name": "Lenovo Yoga 9i (Edge)",          "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"},
    # Windows Firefox
    {"name": "Dell XPS 15 (Firefox)",          "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"},
    {"name": "Lenovo ThinkPad X1 (Firefox)",   "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"},
    {"name": "HP EliteBook 840 (Firefox)",     "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"},
    {"name": "Asus VivoBook 15 (Firefox)",     "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"},

    # ── MacBooks / iMac ──
    {"name": "MacBook Pro M3 Max (Safari)",    "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"},
    {"name": "MacBook Pro M3 (Safari)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"},
    {"name": "MacBook Air M3 (Safari)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"},
    {"name": "MacBook Air M2 (Safari)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"},
    {"name": "MacBook Pro M2 (Safari)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"},
    {"name": "iMac 24 M3 (Safari)",            "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"},
    {"name": "Mac Mini M2 (Safari)",           "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"},
    {"name": "MacBook Air M2 (Chrome)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "MacBook Pro M3 (Chrome)",        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
    {"name": "iMac 24 (Firefox)",              "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0"},
    {"name": "MacBook Air M2 (Firefox)",       "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:124.0) Gecko/20100101 Firefox/124.0"},

    # ── Android Tablets ──
    {"name": "Samsung Galaxy Tab S9 Ultra",    "ua": "Mozilla/5.0 (Linux; Android 13; SM-X916B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Samsung Galaxy Tab S9+",         "ua": "Mozilla/5.0 (Linux; Android 13; SM-X810) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"},
    {"name": "Samsung Galaxy Tab S9",          "ua": "Mozilla/5.0 (Linux; Android 13; SM-X710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
    {"name": "Samsung Galaxy Tab S8 Ultra",    "ua": "Mozilla/5.0 (Linux; Android 12; SM-X906B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"},
    {"name": "Samsung Galaxy Tab A9+",         "ua": "Mozilla/5.0 (Linux; Android 13; SM-X210) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
    {"name": "Lenovo Tab P12 Pro",             "ua": "Mozilla/5.0 (Linux; Android 12; TB-Q706F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},
    {"name": "Xiaomi Pad 6 Pro",               "ua": "Mozilla/5.0 (Linux; Android 13; 23043RP34G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"},
    {"name": "OnePlus Pad",                    "ua": "Mozilla/5.0 (Linux; Android 13; OPD2203) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"},

    # ── Chromebooks ──
    {"name": "HP Chromebook x360 (Chrome)",    "ua": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "Lenovo Chromebook Flex 5",       "ua": "Mozilla/5.0 (X11; CrOS x86_64 14388.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"},
    {"name": "Asus Chromebook Flip CX5",       "ua": "Mozilla/5.0 (X11; CrOS x86_64 14268.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"name": "Acer Chromebook Spin 714",       "ua": "Mozilla/5.0 (X11; CrOS x86_64 14150.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"},

    # ── Linux Desktops ──
    {"name": "Ubuntu Desktop (Chrome)",        "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"},
    {"name": "Fedora Desktop (Firefox)",       "ua": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"},
    {"name": "Debian Desktop (Firefox)",       "ua": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"},
    {"name": "Arch Linux (Chrome)",            "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"},
]

# ── LOCATIONS WITH MATCHING HEADERS ────────────────────
LOCATIONS = [
    {"country": "United States",    "lang": "en-US,en;q=0.9",         "tz": "America/New_York",      "ref": "https://www.google.com/"},
    {"country": "United States",    "lang": "en-US,en;q=0.9",         "tz": "America/Chicago",       "ref": "https://www.bing.com/"},
    {"country": "United States",    "lang": "en-US,en;q=0.9",         "tz": "America/Los_Angeles",   "ref": "https://twitter.com/"},
    {"country": "United Kingdom",   "lang": "en-GB,en;q=0.9",         "tz": "Europe/London",         "ref": "https://www.google.co.uk/"},
    {"country": "United Kingdom",   "lang": "en-GB,en;q=0.8",         "tz": "Europe/London",         "ref": "https://www.bbc.com/"},
    {"country": "Canada",           "lang": "en-CA,en;q=0.9",         "tz": "America/Toronto",       "ref": "https://www.google.ca/"},
    {"country": "Australia",        "lang": "en-AU,en;q=0.9",         "tz": "Australia/Sydney",      "ref": "https://www.google.com.au/"},
    {"country": "Germany",          "lang": "de-DE,de;q=0.9,en;q=0.8","tz": "Europe/Berlin",         "ref": "https://www.google.de/"},
    {"country": "France",           "lang": "fr-FR,fr;q=0.9,en;q=0.8","tz": "Europe/Paris",          "ref": "https://www.google.fr/"},
    {"country": "Netherlands",      "lang": "nl-NL,nl;q=0.9,en;q=0.8","tz": "Europe/Amsterdam",     "ref": "https://www.google.nl/"},
    {"country": "Spain",            "lang": "es-ES,es;q=0.9,en;q=0.8","tz": "Europe/Madrid",         "ref": "https://www.google.es/"},
    {"country": "Italy",            "lang": "it-IT,it;q=0.9,en;q=0.8","tz": "Europe/Rome",           "ref": "https://www.google.it/"},
    {"country": "Brazil",           "lang": "pt-BR,pt;q=0.9,en;q=0.8","tz": "America/Sao_Paulo",    "ref": "https://www.google.com.br/"},
    {"country": "Portugal",         "lang": "pt-PT,pt;q=0.9,en;q=0.8","tz": "Europe/Lisbon",         "ref": "https://www.google.pt/"},
    {"country": "India",            "lang": "en-IN,en;q=0.9,hi;q=0.8","tz": "Asia/Kolkata",          "ref": "https://www.google.co.in/"},
    {"country": "Singapore",        "lang": "en-SG,en;q=0.9",         "tz": "Asia/Singapore",        "ref": "https://www.google.com.sg/"},
    {"country": "South Africa",     "lang": "en-ZA,en;q=0.9",         "tz": "Africa/Johannesburg",   "ref": "https://www.google.co.za/"},
    {"country": "Nigeria",          "lang": "en-NG,en;q=0.9",         "tz": "Africa/Lagos",          "ref": "https://www.google.com.ng/"},
    {"country": "Ghana",            "lang": "en-GH,en;q=0.9",         "tz": "Africa/Accra",          "ref": "https://www.google.com.gh/"},
    {"country": "Kenya",            "lang": "en-KE,en;q=0.9",         "tz": "Africa/Nairobi",        "ref": "https://www.google.co.ke/"},
    {"country": "Japan",            "lang": "ja-JP,ja;q=0.9,en;q=0.8","tz": "Asia/Tokyo",            "ref": "https://www.google.co.jp/"},
    {"country": "South Korea",      "lang": "ko-KR,ko;q=0.9,en;q=0.8","tz": "Asia/Seoul",            "ref": "https://www.google.co.kr/"},
    {"country": "UAE",              "lang": "ar-AE,ar;q=0.9,en;q=0.8","tz": "Asia/Dubai",            "ref": "https://www.google.ae/"},
    {"country": "Sweden",           "lang": "sv-SE,sv;q=0.9,en;q=0.8","tz": "Europe/Stockholm",      "ref": "https://www.google.se/"},
    {"country": "Norway",           "lang": "nb-NO,nb;q=0.9,en;q=0.8","tz": "Europe/Oslo",           "ref": "https://www.google.no/"},
    {"country": "Poland",           "lang": "pl-PL,pl;q=0.9,en;q=0.8","tz": "Europe/Warsaw",         "ref": "https://www.google.pl/"},
    {"country": "Mexico",           "lang": "es-MX,es;q=0.9,en;q=0.8","tz": "America/Mexico_City",   "ref": "https://www.google.com.mx/"},
    {"country": "Argentina",        "lang": "es-AR,es;q=0.9,en;q=0.8","tz": "America/Argentina/Buenos_Aires", "ref": "https://www.google.com.ar/"},
    {"country": "New Zealand",      "lang": "en-NZ,en;q=0.9",         "tz": "Pacific/Auckland",      "ref": "https://www.google.co.nz/"},
    {"country": "Ireland",          "lang": "en-IE,en;q=0.9",         "tz": "Europe/Dublin",         "ref": "https://www.google.ie/"},
]


class RealUserBot(HttpUser):
    wait_time = between(30, 18000)  # 30 seconds to 5 hours

    def on_start(self):
        self.device   = random.choice(DEVICES)
        self.location = random.choice(LOCATIONS)
        self.session_pages = []

        self.headers = {
            "User-Agent":                self.device["ua"],
            "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language":           self.location["lang"],
            "Accept-Encoding":           "gzip, deflate, br",
            "Connection":                "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest":            "document",
            "Sec-Fetch-Mode":            "navigate",
            "Sec-Fetch-Site":            "cross-site",
            "Referer":                   self.location["ref"],
            "Cache-Control":             "max-age=0",
        }

        print(f"[+] {self.device['name']} | {self.location['country']} | {self.location['tz']}")
        self._visit("/SimpleRead/", entry=True)

    def _visit(self, page, entry=False):
        if not entry and self.session_pages:
            self.headers["Referer"]        = "https://sadekunle215-cmd.github.io" + self.session_pages[-1]
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
        self._visit("/SimpleRead/")
        time.sleep(random.uniform(5, 20))
        self._visit("/SimpleRead/article.html")

    @task(2)
    def browse_category_then_article(self):
        self._visit("/SimpleRead/category.html")
        time.sleep(random.uniform(8, 25))
        self._visit("/SimpleRead/article.html")

    @task(1)
    def visit_about(self):
        self._visit("/SimpleRead/about.html")

    @task(1)
    def deep_session(self):
        for page in ["/SimpleRead/", "/SimpleRead/category.html", "/SimpleRead/article.html", "/SimpleRead/about.html"]:
            self._visit(page)
            time.sleep(random.uniform(15, 60))
