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
MULTI_DAY_PATH = os.path.join(CACHE_DIR, "multi_day_levels.json")
SHORT_INTEREST_PATH = os.path.join(CACHE_DIR, "short_interest.json")


current_date_str = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
OUTPUT_PATH = os.path.join(CACHE_DIR, f"universe_enriched_{current_date_str}.json")

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def enrich_with_tv_signals(universe, tv_data):
    normalized_tv_data = {}
    for k, v in tv_data.items():
        base = k.split(".")[0].upper()
        normalized_tv_data[base] = v

    for symbol, info in universe.items():
        tv = normalized_tv_data.get(symbol.upper())
        if tv:
            signals = info.setdefault("signals", {})
            if "price" in tv:
                signals["price"] = tv["price"]
                info["tv_price"] = tv["price"]
            if "volume" in tv:
                signals["volume"] = tv["volume"]
                info["tv_volume"] = tv["volume"]
            if "changePercent" in tv:
                signals["changePercent"] = tv["changePercent"]
                info["tv_changePercent"] = tv["changePercent"]
            if "rel_vol" in tv:
                info["rel_vol"] = tv["rel_vol"]
            if "avg_volume_10d" in tv:
                info["avg_volume_10d"] = tv["avg_volume_10d"]
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

def apply_sector_rotation_signals(universe, sector_data):
    SECTOR_ETFS = {
        "XLF": "Financial Services",
        "XLK": "Technology",
        "XLE": "Energy",
        "XLV": "Healthcare",
        "XLY": "Consumer Cyclical",
        "XLI": "Industrials",
        "XLP": "Consumer Defensive",
        "XLU": "Utilities",
        "XLRE": "Real Estate",
        "XLB": "Basic Materials",
        "XLCD": "Communication Services"
    }

    # Reverse map for easier matching
    SECTOR_TO_ETF = {v: k for k, v in SECTOR_ETFS.items()}

    sector_changes = {}
    for etf, sector in SECTOR_ETFS.items():
        etf_info = sector_data.get(etf)
        if not etf_info:
            continue
        price = etf_info.get("tv_price")
        prev_close = etf_info.get("prevClose")
        if price and prev_close:
            try:
                change = ((price - prev_close) / prev_close) * 100
                sector_changes[sector] = round(change, 2)
            except ZeroDivisionError:
                continue

    sorted_sectors = sorted(sector_changes.items(), key=lambda x: x[1], reverse=True)
    top_sectors = set(s for s, _ in sorted_sectors[:2])
    bottom_sectors = set(s for s, _ in sorted_sectors[-2:])

    for symbol, info in universe.items():
        sector = info.get("sector")
        if not sector:
            continue
        signals = info.setdefault("signals", {})
        if sector in top_sectors:
            signals["strong_sector"] = True
        elif sector in bottom_sectors:
            signals["weak_sector"] = True

    return universe


def enrich_with_candles(universe, candle_data):
    for symbol, info in universe.items():
        candles = candle_data.get(symbol, [])
        if not candles:
            continue

        highs = []
        lows = []

        for c in candles:
            high = c.get("high")
            low = c.get("low")
            if high is not None and low is not None:
                highs.append(high)
                lows.append(low)

        if highs and lows:
            info["range_930_940_high"] = max(highs)
            info["range_930_940_low"] = min(lows)

    return universe


def enrich_with_multi_day_levels(universe, multi_day_data):
    for symbol, info in universe.items():
        data = multi_day_data.get(symbol)
        if data and "high" in data and "low" in data:
            info["high_10d"] = data["high"]
            info["low_10d"] = data["low"]
    return universe

def enrich_with_short_interest(universe, short_data):
    for symbol, info in universe.items():
        si = short_data.get(symbol.upper())
        rel_vol = info.get("rel_vol", 0)
        change = info.get("signals", {}).get("changePercent", 0)

        if si:
            short_pct = si.get("shortPercentOfFloat", 0)
            if (
                short_pct >= 0.18 and
                rel_vol > 1.2 and
                abs(change) >= 1.5
            ):
                info.setdefault("signals", {})["squeeze_watch"] = True
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

        if open_price is not None and prev_close is not None:
            if open_price > prev_close * 1.01:
                signals["gap_up"] = True
            elif open_price < prev_close * 0.99:
                signals["gap_down"] = True

        if price is not None and high is not None and price > high:
            signals["break_above_range"] = True
        if price is not None and low is not None and price < low:
            signals["break_below_range"] = True

        if change is not None and abs(change) >= 2.5:
            signals["early_move"] = True

        if volume is not None and volume >= 1_000_000:
            signals["high_volume"] = True

        if price is not None and high is not None and 0 < (high - price) <= 0.25:
            signals["near_range_high"] = True

        if info.get("rel_vol", 0) > 1.5:
            signals["high_rel_vol"] = True

        if price is not None and info.get("high_10d") and price >= info["high_10d"] * 0.98:
            signals["near_multi_day_high"] = True

        if price is not None and info.get("low_10d") and price <= info["low_10d"] * 1.02:
            signals["near_multi_day_low"] = True

        if (
            volume is not None and volume >= 800_000 and  # lower vol threshold a bit
            info.get("rel_vol", 0) > 1.0 and              # loosen rel vol to 1.0
            high is not None and low is not None and
            price is not None and
            low * 0.99 <= price <= high * 1.01 and         # widen wiggle room from 0.5% → 1%
            not signals.get("break_above_range") and
            not signals.get("break_below_range") and
            (high - low) / low < 0.02                     # expand range limit from 1.5% → 2%
        ):
            signals["high_volume_no_breakout"] = True



        
    return universe

def flag_top_volume_gainers(universe, top_n=5):
    sorted_tickers = sorted(
        universe.items(),
        key=lambda x: x[1].get("tv_volume") or 0,
        reverse=True
    )
    for symbol, info in sorted_tickers[:top_n]:
        info.setdefault("signals", {})["top_volume_gainer"] = True
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

def main():
    print("🚀 Starting enrichment...")
    universe = load_json(UNIVERSE_PATH)
    tv_signals = load_json(TV_SIGNALS_PATH)
    sector_prices = load_json(SECTOR_PRICES_PATH)
    candles = load_json(CANDLES_PATH)
    short_interest = load_json(SHORT_INTEREST_PATH)
    multi_day_data = load_json(MULTI_DAY_PATH)

    print(f"📦 Loaded {len(universe)} tickers")

    universe = enrich_with_tv_signals(universe, tv_signals)
    universe = enrich_with_sector(universe, sector_prices)
    universe = apply_sector_rotation_signals(universe, sector_prices)
    universe = enrich_with_candles(universe, candles)
    universe = enrich_with_multi_day_levels(universe, multi_day_data)
    universe = enrich_with_short_interest(universe, short_interest)
    universe = apply_signal_flags(universe)
    universe = flag_top_volume_gainers(universe)
    universe = inject_risk_flags(universe)


    with open(OUTPUT_PATH, "w") as f:
        json.dump(universe, f, indent=2)
    print(f"✅ Enriched universe saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
