"""
notifier.py — sends Telegram alerts
Put your bot token and chat ID directly here.
"""

import requests
import logging

log = logging.getLogger(__name__)

# ✅ PASTE YOUR VALUES BELOW:
TELEGRAM_BOT_TOKEN = "8663391935:AAE3xLOt5JNd1sbvXliPyRSmh777T-Y3cOU"   # e.g. 7123456789:AAFxxx...
TELEGRAM_CHAT_ID   = "6569762456"     # e.g. 123456789

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram(message: str):
    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "Markdown",
    }
    try:
        resp = requests.post(TELEGRAM_API, json=payload, timeout=10)
        resp.raise_for_status()
        log.info("📨 Telegram message sent!")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send Telegram message: {e}")
        raise
