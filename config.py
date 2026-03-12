# ============================================================
#  config.py  —  EDIT THIS FILE TO SET YOUR STOCK ALERTS
#  Telegram credentials are loaded from GitHub Secrets (secure)
#  — you do NOT put them here
# ============================================================

# ── Your stock alerts ────────────────────────────────────────
#
# market: "US"    → NYSE/NASDAQ, price in USD
# market: "KOSPI" → KRX, price in KRW (use 6-digit KRX code)
#
# alert_above: send alert when price rises TO or ABOVE this
# alert_below: send alert when price drops TO or BELOW this

ALERTS = [

    # ── US Stocks (USD) ─────────────────────────────────────
    {
        "symbol":      "NVDA",
        "market":      "US",
        "label":       "NVIDIA",
        "alert_above": 160.00,
        "alert_below": 100.00,
    },
    {
        "symbol":      "AAPL",
        "market":      "US",
        "label":       "Apple",
        "alert_above": 240.00,
        "alert_below": 180.00,
    },
    {
        "symbol":      "TSM",
        "market":      "US",
        "label":       "TSMC ADR",
        "alert_above": 220.00,
        "alert_below": 150.00,
    },
    {
        "symbol":      "AVGO",
        "market":      "US",
        "label":       "Broadcom",
        "alert_above": 400.00,
        "alert_below": 280.00,
    },

    # ── KOSPI Stocks (KRW) ──────────────────────────────────
    {
        "symbol":      "005930",   # Samsung Electronics
        "market":      "KOSPI",
        "label":       "삼성전자",
        "alert_above": 80000,
        "alert_below": 55000,
    },
    {
        "symbol":      "000660",   # SK Hynix
        "market":      "KOSPI",
        "label":       "SK하이닉스",
        "alert_above": 220000,
        "alert_below": 150000,
    },

    # ── Add more stocks here ─────────────────────────────────
    # {
    #     "symbol":      "TSLA",
    #     "market":      "US",
    #     "label":       "Tesla",
    #     "alert_above": 300.00,
    #     "alert_below": 200.00,
    # },
    # {
    #     "symbol":      "035420",   # NAVER
    #     "market":      "KOSPI",
    #     "label":       "NAVER",
    #     "alert_above": 250000,
    #     "alert_below": 170000,
    # },
]
