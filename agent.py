#!/usr/bin/env python3
"""
Stock Price Alert Agent — GitHub Actions Version
Alerts only during active market hours (summer/DST-aware):
  US  : 04:00–20:00 ET  (pre-market open → after-hours close)
        = 08:00–00:00 UTC during EDT (summer, UTC-4)
        = 09:00–01:00 UTC during EST (winter, UTC-5)
  KOSPI: 09:00–15:30 KST = 00:00–06:30 UTC (KST is always UTC+9, no DST)
"""

import json, os, sys, logging
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from price_fetcher import get_price
from notifier import send_telegram, build_alert_message
from config import ALERTS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)
STATE_FILE = "alert_state.json"

ET  = ZoneInfo("America/New_York")   # handles EDT/EST automatically
KST = ZoneInfo("Asia/Seoul")


def is_market_active(market: str) -> bool:
    now_utc = datetime.now(timezone.utc)

    if market == "KOSPI":
        # KOSPI: Mon–Fri 09:00–15:30 KST
        now_kst = now_utc.astimezone(KST)
        if now_kst.weekday() >= 5:          # Saturday=5, Sunday=6
            return False
        t = now_kst.hour * 60 + now_kst.minute
        return 9 * 60 <= t < 15 * 60 + 30

    else:
        # US stocks: Mon–Fri 04:00–20:00 ET (pre-market → after-hours)
        now_et = now_utc.astimezone(ET)
        if now_et.weekday() >= 5:
            return False
        t = now_et.hour * 60 + now_et.minute
        return 4 * 60 <= t < 20 * 60


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    now_utc = datetime.now(timezone.utc)
    log.info(f"Stock Alert Agent running — {now_utc.strftime('%Y-%m-%d %H:%M UTC')}")
    log.info(f"Checking {len(ALERTS)} ticker(s)...")

    state = load_state()
    alerts_sent = 0
    timestamp = now_utc.strftime("%Y-%m-%d %H:%M UTC")

    for alert in ALERTS:
        symbol   = alert["symbol"]
        market   = alert["market"]
        above    = alert.get("alert_above")
        below    = alert.get("alert_below")
        label    = alert.get("label", symbol)
        currency = "KRW" if market == "KOSPI" else "USD"

        if not is_market_active(market):
            log.info(f"  [{market}] market closed — skipping {label}")
            continue

        try:
            price = get_price(symbol, market)
        except Exception as e:
            log.warning(f"Could not fetch {symbol}: {e}")
            continue

        log.info(f"{label} ({symbol}) -> {price:,.2f} {currency}")

        if above is not None:
            key = f"{symbol}_above_{above}"
            if price >= above:
                if not state.get(key):
                    send_telegram(build_alert_message(label, symbol, "above", price, above, currency, timestamp))
                    state[key] = True
                    if below is not None:
                        state[f"{symbol}_below_{below}"] = False
                    alerts_sent += 1
                    log.info(f"Alert sent: {label} above {above}")
            else:
                state[key] = False

        if below is not None:
            key = f"{symbol}_below_{below}"
            if price <= below:
                if not state.get(key):
                    send_telegram(build_alert_message(label, symbol, "below", price, below, currency, timestamp))
                    state[key] = True
                    if above is not None:
                        state[f"{symbol}_above_{above}"] = False
                    alerts_sent += 1
                    log.info(f"Alert sent: {label} below {below}")
            else:
                state[key] = False

    save_state(state)
    log.info(f"Done. {alerts_sent} alert(s) sent this run.")


if __name__ == "__main__":
    main()
