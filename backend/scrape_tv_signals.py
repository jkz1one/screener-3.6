import json
import os
from datetime import datetime
import yfinance as yf
from tqdm import tqdm  # ✅ Add this if not already

# Define cache path
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
TV_OUTPUT = os.path.join(CACHE_DIR, "tv_signals.json")
UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")

# ✅ Load universe
with open(UNIVERSE_PATH, "r") as f:
    universe = json.load(f)
tickers = list(universe.keys())  # ✅ Define this before tqdm

# 📡 Progress-tracked data pull
tv_data = {}
for symbol in tqdm(tickers, desc="📡 Fetching TV signals"):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="11d")

        rel_vol = None
        avg_volume_10d = None
        if len(hist) >= 10:
            past_volumes = hist['Volume'][:-1]
            avg_volume_10d = past_volumes.mean()
            today_volume = hist['Volume'].iloc[-1]
            rel_vol = today_volume / avg_volume_10d if avg_volume_10d > 0 else 0

        tv_data[symbol] = {
            "price": info.get("regularMarketPrice"),
            "volume": info.get("volume"),
            "changePercent": info.get("regularMarketChangePercent"),
            "timestamp": datetime.now().isoformat()
        }

        if rel_vol is not None:
            tv_data[symbol]["rel_vol"] = round(rel_vol, 2)
        if avg_volume_10d is not None:
            tv_data[symbol]["avg_volume_10d"] = int(avg_volume_10d)

    except Exception as e:
        tqdm.write(f"⚠️ Failed to fetch {symbol}: {e}")

# ✅ Save
with open(TV_OUTPUT, "w") as f:
    json.dump(tv_data, f, indent=2)

print(f"✅ TradingView-style signals saved to {TV_OUTPUT} with {len(tv_data)} entries.")
