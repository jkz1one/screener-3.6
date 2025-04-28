# scrape_candles_5m.py (optimized + rounded)

import os
import json
import yfinance as yf
from datetime import datetime, timedelta
import pytz
from tqdm import tqdm

CACHE_DIR = "backend/cache"
UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")
OUTPUT_PATH = os.path.join(CACHE_DIR, "candles_5m.json")

def load_universe(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Universe file not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def main():
    print("\U0001F680 Fetching EXACT 9:30–9:40 5m candles...")

    est = pytz.timezone("America/New_York")
    now = datetime.now(est)

    # Fallback to previous weekday if weekend
    if now.weekday() >= 5:  # Saturday/Sunday
        offset = (now.weekday() - 4) % 7
        now -= timedelta(days=offset)

    universe = load_universe(UNIVERSE_PATH)
    tickers = list(universe.keys())

    result = {}

    for symbol in tqdm(tickers, desc="Scraping 5m candles"):
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="5m", prepost=True)
            if hist.empty:
                continue

            candles = []
            for idx, row in hist.iterrows():
                ts = idx.tz_convert('America/New_York').strftime("%H:%M:%S")
                if ts.endswith(":30:00") or ts.endswith(":35:00") or ts.endswith(":40:00"):
                    candles.append({
                        "timestamp": idx.tz_convert('America/New_York').strftime("%Y-%m-%d %H:%M:%S"),
                        "open": round(row["Open"], 2),
                        "high": round(row["High"], 2),
                        "low": round(row["Low"], 2),
                        "close": round(row["Close"], 2),
                        "volume": int(row["Volume"])
                    })

            if candles:
                result[symbol] = candles

        except Exception as e:
            print(f"⚠️ Failed {symbol}: {e}")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Candles saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
