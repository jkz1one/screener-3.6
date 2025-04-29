import json
import os
from datetime import datetime
from tqdm import tqdm
import yfinance as yf

# --- Paths ---
CACHE_DIR = os.path.join(os.path.dirname(__file__), "../cache")
TV_OUTPUT = os.path.join(CACHE_DIR, "tv_signals.json")
UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")

# --- Load Universe ---
with open(UNIVERSE_PATH, "r") as f:
    universe = json.load(f)

symbols = list(universe.keys())

# --- Fetch Data ---
print(f"\U0001F4F0 Fetching combined TV-style + YF enrichment data for {len(symbols)} tickers...")

batch = yf.Tickers(" ".join(symbols))
tv_data = {}

for symbol in tqdm(symbols, desc="\U0001F4F0 Scraping TV signals"):
    try:
        ticker = batch.tickers.get(symbol)
        if not ticker:
            continue

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
            "open": info.get("open"),
            "prevClose": info.get("previousClose"),
            "timestamp": datetime.now().isoformat()
        }

        if rel_vol is not None:
            tv_data[symbol]["rel_vol"] = round(rel_vol, 2)
        if avg_volume_10d is not None:
            tv_data[symbol]["avg_volume_10d"] = int(avg_volume_10d)

    except Exception as e:
        tqdm.write(f"⚠️ Failed for {symbol}: {e}")

# --- Save Output ---
os.makedirs(CACHE_DIR, exist_ok=True)
with open(TV_OUTPUT, "w") as f:
    json.dump(tv_data, f, indent=2)

print(f"✅ TV-style + YF enrichment signals saved to {TV_OUTPUT} with {len(tv_data)} entries.")
