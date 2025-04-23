import json
import os
from datetime import datetime
import pytz
from tqdm import tqdm

CACHE_DIR = "backend/cache"
UNIVERSE_PATH = os.path.join(CACHE_DIR, "universe_cache.json")
TV_SIGNALS_PATH = os.path.join(CACHE_DIR, "tv_signals.json")
SECTOR_PRICES_PATH = os.path.join(CACHE_DIR, "sector_etf_prices.json")
CANDLES_PATH = os.path.join(CACHE_DIR, "candles_5m.json")
SHORT_INTEREST_PATH = os.path.join(CACHE_DIR, "short_interest.json")

current_date_str = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
OUTPUT_PATH = os.path.join(CACHE_DIR, f"universe_enriched_{current_date_str}.json")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def enrich_with_tv_signals(universe, tv_data):
    for symbol, info in universe.items():
        if symbol in tv_data:
            info.setdefault("signals", {}).update(tv_data[symbol])
    return universe

def enrich_with_sector(universe, sector_data):
    for symbol, info in universe.items():
        sector = info.get("sector")
        if not sector:
            continue
        etf = sector_data.get(sector)
        if etf:
            info["sector_etf"] = etf
    return universe

def enrich_with_candles(universe, candle_data):
    for symbol, info in universe.items():
        candles = candle_data.get(symbol, [])
        range_930_940 = [c for c in candles if any(
            c.get("timestamp", "").endswith(t) for t in (":30:00", ":35:00", ":40:00")
        )]
        if range_930_940:
            highs = [c.get("high", 0) for c in range_930_940]
            lows = [c.get("low", 0) for c in range_930_940]
            info["range_930_940_high"] = max(highs)
            info["range_930_940_low"] = min(lows)
    return universe

def enrich_with_short_interest(universe, short_data):
    for symbol, info in universe.items():
        si = short_data.get(symbol.upper())
        if si and si.get("shortPercentOfFloat", 0) >= 0.20:
            info.setdefault("signals", {})["squeeze_watch"] = True
    return universe

def inject_risk_flags(universe):
    for symbol, info in universe.items():
        vol = info.get("avg_volume")
        spread = info.get("spread")
        if vol is not None and vol < 500_000:
            info.setdefault("signals", {})["low_liquidity"] = True
        if spread is not None and spread > 0.30:
            info.setdefault("signals", {})["wide_spread"] = True
    return universe

def apply_signal_flags(universe):
    for symbol, info in universe.items():
        signals = info.setdefault("signals", {})
        price = signals.get("price")
        volume = signals.get("volume")
        change = signals.get("changePercent")
        open_price = info.get("open")
        prev_close = info.get("prevClose")
        high = info.get("range_930_940_high")
        low = info.get("range_930_940_low")

        # Tier 1: Gap up/down
        if open_price and prev_close:
            if open_price > prev_close * 1.01:
                signals["gap_up"] = True
            elif open_price < prev_close * 0.99:
                signals["gap_down"] = True

        # Tier 1: Breakout
        if price and high and price > high:
            signals["break_above_range"] = True
        if price and low and price < low:
            signals["break_below_range"] = True

        # Tier 2: Early move
        if change and abs(change) >= 2.5:
            signals["early_move"] = True

        # Tier 3: High volume
        if volume and volume >= 1_000_000:
            signals["high_volume"] = True

        # Tier 3: Near range high
        if price and high and 0 < (high - price) <= 0.25:
            signals["near_range_high"] = True

    return universe

def main():
    print("🚀 Starting enrichment...")
    universe = load_json(UNIVERSE_PATH)
    tv_signals = load_json(TV_SIGNALS_PATH)
    sector_prices = load_json(SECTOR_PRICES_PATH)
    candles = load_json(CANDLES_PATH)
    short_interest = load_json(SHORT_INTEREST_PATH)

    print(f"📦 Loaded {len(universe)} tickers")

    universe = enrich_with_tv_signals(universe, tv_signals)
    universe = enrich_with_sector(universe, sector_prices)
    universe = enrich_with_candles(universe, candles)
    universe = enrich_with_short_interest(universe, short_interest)
    universe = apply_signal_flags(universe)
    universe = inject_risk_flags(universe)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(universe, f, indent=2)
    print(f"✅ Enriched universe saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
