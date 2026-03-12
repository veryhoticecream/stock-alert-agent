"""
notifier.py — sends Telegram alerts
Credentials are read from environment variables (set via GitHub Secrets).
"""

import os
import requests
import logging

log = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram(message: str):
    token   = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = TELEGRAM_API.format(token=token)
    payload = {
        "chat_id":    chat_id,
        "text":       message,
        "parse_mode": "Markdown",
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        log.info("📨 Telegram message sent!")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send Telegram message: {e}")
        raise
