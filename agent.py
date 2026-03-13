#!/usr/bin/env python3
"""
Stock Price Alert Agent — GitHub Actions Version
Runs every 5 minutes via GitHub Actions (free).
State is persisted in alert_state.json committed back to the repo,
so alerts don't repeat across runs.
"""

import json
import os
import sys
import logging
from datetime import datetime
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


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def main():
    log.info("Stock Alert Agent running via GitHub Actions")
    log.info(f"Checking {len(ALERTS)} ticker(s)...")

    state = load_state()
    alerts_sent = 0
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    for alert in ALERTS:
        symbol   = alert["symbol"]
        market   = alert["market"]
        above    = alert.get("alert_above")
        below    = alert.get("alert_below")
        label    = alert.get("label", symbol)
        currency = "KRW" if market == "KOSPI" else "USD"

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
                    msg = build_alert_message(label, symbol, "above", price, above, currency, timestamp)
                    send_telegram(msg)
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
                    msg = build_alert_message(label, symbol, "below", price, below, currency, timestamp)
                    send_telegram(msg)
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
