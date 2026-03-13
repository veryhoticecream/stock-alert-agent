"""
notifier.py — sends Telegram alerts
Uses MarkdownV2 with proper escaping to avoid 400 Bad Request errors.
"""

import re
import requests
import logging

log = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "8663391935:AAE3xLOt5JNd1sbvXliPyRSmh777T-Y3cOU"
TELEGRAM_CHAT_ID   = "6569762456"

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Characters that must be escaped in MarkdownV2 (outside of ` ` and * * blocks)
_ESCAPE_RE = re.compile(r'([_\[\]()~`>#+\-=|{}.!\\])')


def _esc(text: str) -> str:
    """Escape a plain string for use in MarkdownV2 outside of formatting marks."""
    return _ESCAPE_RE.sub(r'\\\1', str(text))


def send_telegram(message: str):
    """
    Send a Telegram message.
    `message` is expected to already be valid MarkdownV2 text
    (bold with *…*, code with `…`, etc.) — call build_alert_message()
    to construct it safely.
    """
    payload = {
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "MarkdownV2",
    }
    try:
        resp = requests.post(TELEGRAM_API, json=payload, timeout=10)
        resp.raise_for_status()
        log.info("📨 Telegram message sent!")
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to send Telegram message: {e}")
        raise


def build_alert_message(
    label: str,
    symbol: str,
    direction: str,       # "above" or "below"
    price: float,
    threshold: float,
    currency: str,
    timestamp: str,
) -> str:
    """
    Build a properly escaped MarkdownV2 alert message.
    All dynamic values are escaped before insertion.
    """
    arrow  = "📈" if direction == "above" else "📉"
    word   = "rose ABOVE" if direction == "above" else "dropped BELOW"

    price_str     = _esc(f"{price:,.2f} {currency}")
    threshold_str = _esc(f"{threshold:,.2f}")
    label_esc     = _esc(label)
    ts_esc        = _esc(timestamp)

    return (
        f"🚨 *PRICE ALERT*\n"
        f"{arrow} *{label_esc}* {_esc(word)} threshold\\!\n\n"
        f"💰 Current: `{price_str}`\n"
        f"🎯 Threshold: `{threshold_str}`\n"
        f"🕐 {ts_esc}"
    )
