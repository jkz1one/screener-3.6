import yfinance as yf
import json
import os
from datetime import datetime
import pytz

CACHE_PATH = "backend/cache/universe_cache.json"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def enrich_with_yfinance(universe):
    symbols = list(universe.keys())
    print(f"📡 Fetching yfinance data for {len(symbols)} tickers...")

    tickers = yf.Tickers(" ".join(symbols))

    for symbol in symbols:
        info = tickers.tickers.get(symbol)
        if not info:
            continue
        try:
            data = info.info
            if not data:
                continue

            universe[symbol]["open"] = data.get("open")
            universe[symbol]["prevClose"] = data.get("previousClose")
            universe[symbol]["yfinance_updated"] = datetime.now(pytz.timezone("America/New_York")).isoformat()
        except Exception as e:
            print(f"⚠️ Failed for {symbol}: {e}")
    return universe


def main():
    universe = load_json(CACHE_PATH)
    enriched = enrich_with_yfinance(universe)
    save_json(enriched, CACHE_PATH)
    print(f"✅ Updated universe with yfinance data saved to {CACHE_PATH}")


if __name__ == "__main__":
    main()
