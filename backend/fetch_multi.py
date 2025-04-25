import os
import json
import yfinance as yf
from datetime import datetime
from tqdm import tqdm  # ✅ Add this

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")
OUTPUT_PATH = os.path.join(CACHE_DIR, "multi_day_levels.json")

LOOKBACK_DAYS = 10

def main():
    with open(UNIVERSE_PATH, "r") as f:
        universe = json.load(f)
    tickers = list(universe.keys())

    levels = {}

    print(f"📡 Fetching {LOOKBACK_DAYS}-day highs/lows for {len(tickers)} tickers...")

    for symbol in tqdm(tickers, desc="🔄 Processing"):
        try:
            hist = yf.Ticker(symbol).history(period=f"{LOOKBACK_DAYS + 1}d")
            if not hist.empty:
                high = hist["High"][:-1].max()
                low = hist["Low"][:-1].min()
                levels[symbol] = {
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "days": LOOKBACK_DAYS,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            levels[symbol] = {"error": str(e)}

    with open(OUTPUT_PATH, "w") as f:
        json.dump(levels, f, indent=2)

    print(f"✅ Multi-day levels saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
