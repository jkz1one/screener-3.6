import json
import os
from datetime import datetime
import yfinance as yf

# Define cache path
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
TV_OUTPUT = os.path.join(CACHE_DIR, "tv_signals.json")

# Load universe symbols
UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")
with open(UNIVERSE_PATH, "r") as f:
    universe = json.load(f)
tickers = list(universe.keys())

# Pull last price, volume, and changePercent using yfinance (as TV proxy)
tv_data = {}
for symbol in tickers:
    try:
        info = yf.Ticker(symbol).info
        tv_data[symbol] = {
            "price": info.get("regularMarketPrice"),
            "volume": info.get("volume"),
            "changePercent": info.get("regularMarketChangePercent"),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"⚠️ Failed to fetch {symbol}: {e}")

# Save to cache
with open(TV_OUTPUT, "w") as f:
    json.dump(tv_data, f, indent=2)

print(f"✅ TradingView-style signals saved to {TV_OUTPUT} with {len(tv_data)} entries.")
