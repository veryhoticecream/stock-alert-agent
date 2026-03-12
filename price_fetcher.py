"""
price_fetcher.py — fetches live prices via yfinance (free, no API key needed)
US:    standard ticker symbol  (NVDA, AAPL, TSLA...)
KOSPI: 6-digit KRX code        (005930 → 005930.KS)
"""

import yfinance as yf
import logging

log = logging.getLogger(__name__)


def get_price(symbol: str, market: str) -> float:
    ticker_symbol = f"{symbol}.KS" if market == "KOSPI" else symbol
    ticker = yf.Ticker(ticker_symbol)

    # Fast path
    try:
        price = ticker.fast_info["last_price"]
        if price and price > 0:
            return float(price)
    except Exception:
        pass

    # Fallback: recent history
    hist = ticker.history(period="1d", interval="1m")
    if hist.empty:
        raise ValueError(f"No price data for {ticker_symbol}")

    return float(hist["Close"].iloc[-1])
