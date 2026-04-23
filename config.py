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
        "symbol":      "SCCO",
        "market":      "US",
        "label":       "Southern Copper Corporation",
        "alert_above": 210.00,
        "alert_below": 188.00,
    },
 {
        "symbol":      "NEM",
        "market":      "US",
        "label":       "Newmont Corporation",
        "alert_above": 130.00,
        "alert_below": 118.00,
    },

    # ── KOSPI Stocks (KRW) ──────────────────────────────────
    {
        "symbol":      "005930",   # Samsung Electronics
        "market":      "KOSPI",
        "label":       "삼성전자",
        "alert_above": 200000,
        "alert_below": 190000,
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
