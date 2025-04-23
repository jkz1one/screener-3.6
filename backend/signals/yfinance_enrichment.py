
import yfinance as yf
import time
import pandas as pd
from datetime import datetime
import pytz

def format_ticker_for_yf(ticker):
    return ticker.replace(".", "-")

def get_latest_930_open(ticker):
    try:
        yf_ticker = yf.Ticker(format_ticker_for_yf(ticker))
        data = yf_ticker.history(interval="1m", period="2d", prepost=False)
        if data.empty:
            return None

        data = data.tz_convert("US/Eastern")
        data_930 = data.between_time("09:30", "09:30")
        if data_930.empty:
            return None

        candle_930 = data_930.iloc[-1]
        return candle_930["Open"]
    except Exception as e:
        print(f"⚠️ {ticker}: Failed to get 9:30 open - {e}")
        return None

def fetch_yfinance_signals(tickers):
    results = {}

    for ticker in tickers:
        try:
            yf_ticker = yf.Ticker(format_ticker_for_yf(ticker))
            info = yf_ticker.info

            open_930 = get_latest_930_open(ticker)
            prev_close = info.get("regularMarketPreviousClose")
            volume = info.get("volume")
            avg_volume = info.get("averageVolume")
            last_price = info.get("regularMarketPrice")

            if open_930 is None or prev_close is None:
                continue

            gap_percent = ((open_930 - prev_close) / prev_close) * 100 if prev_close > 0 else 0
            rel_volume = (volume / avg_volume) if volume and avg_volume else None

            results[ticker] = {
                "open930": round(open_930, 2),
                "prevClose": round(prev_close, 2),
                "gapPercent": round(gap_percent, 2),
                "relVolume": round(rel_volume, 2) if rel_volume is not None else None,
                "lastPrice": round(last_price, 2) if last_price is not None else None
            }

            time.sleep(0.5)

        except Exception as e:
            print(f"❌ {ticker}: Error {e}")

    return results

if __name__ == "__main__":
    test = fetch_yfinance_signals(["TSLA", "AAPL", "GME", "BRK.B", "BF.B"])
    from pprint import pprint
    pprint(test)
