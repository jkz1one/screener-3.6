import os
import json
from datetime import datetime, timedelta
import yfinance as yf
from pytz import timezone

RAW_PREFIX = "universe_"
ENRICHED_PREFIX = "universe_enriched_"
CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")


def get_latest_raw_universe_path():
    path = os.path.join(CACHE_DIR, "universe_cache.json")
    if not os.path.exists(path):
        return None
    return path


def get_yf_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="10d", interval="1d")
        if hist.empty or len(hist) < 2:
            return None, None, None, None
        prev_close = hist['Close'].iloc[-2]
        avg_volume = hist['Volume'].mean()
        high_5d = hist['High'].max()
        low_5d = hist['Low'].min()
        return prev_close, avg_volume, high_5d, low_5d
    except Exception as e:
        print(f"⚠️ Failed to fetch yfinance data for {symbol}: {e}")
        return None, None, None, None


def enrich_ticker(symbol, data, top_volume_symbols=None):
    import pandas as pd
    prev_close, avg_volume, high_5d, low_5d = get_yf_data(symbol)
    data["prevClose"] = round(prev_close, 2) if prev_close else None
    data["avgVolume"] = int(avg_volume) if avg_volume else None
    data["multiDayHigh"] = round(high_5d, 2) if high_5d else None
    data["multiDayLow"] = round(low_5d, 2) if low_5d else None
    if symbol is None:
        return None
    if '.' in symbol:
        symbol = symbol.replace('.', '-')
    tier1 = []
    tier2 = []
    tier3 = []
    tags = []

    gap = data.get("signals", {}).get("gapPercent", 0)
    rel_vol = data.get("signals", {}).get("relVolume", 1.0)
    momentum = data.get("signals", {}).get("momentumBullish", False)

    tv_price = data.get("tv_price")
    multi_high = data.get("multiDayHigh")
    multi_low = data.get("multiDayLow")

    if gap >= 0.75:
        tier1.append("Gap Up")
        tags.append("Strong Setup")
    elif gap <= -0.75:
        tier1.append("Gap Down")
        tags.append("Strong Setup")

    if tv_price and multi_high and tv_price > multi_high:
        tier1.append("Break Above Multi-Day High")
        tags.append("Strong Setup")

    if tv_price and multi_low and tv_price < multi_low:
        tier1.append("Break Below Multi-Day Low")
        tags.append("Strong Setup")

    if tv_price and multi_high and (multi_high - tv_price) / multi_high <= 0.02:
        tier3.append("Near Multi-Day High")

    if gap > 1.5 and rel_vol > 2.0:
        tier2.append("Squeeze Watch")

    if data.get("signals", {}).get("earlyMove"):
        tier2.append("Early Move")

    try:
        et = timezone("US/Eastern")
        now = datetime.now(et)
        today = now.date()
        yesterday = today - timedelta(days=1)

        ticker = yf.Ticker(symbol)
        df = ticker.history(start=(now - timedelta(days=5)).strftime("%Y-%m-%d"), interval="5m")
        df = df.tz_convert('US/Eastern')

        premarket_start = datetime.combine(today, datetime.min.time()).replace(hour=4, tzinfo=et)
        premarket_end = datetime.combine(today, datetime.min.time()).replace(hour=9, minute=30, tzinfo=et)
        premarket_df = df.loc[(df.index >= premarket_start) & (df.index < premarket_end)]

        rth_start = datetime.combine(yesterday, datetime.min.time()).replace(hour=9, minute=30, tzinfo=et)
        rth_end = datetime.combine(yesterday, datetime.min.time()).replace(hour=16, tzinfo=et)
        rth_df = df.loc[(df.index >= rth_start) & (df.index < rth_end)]

        data["premarketHigh"] = round(premarket_df["High"].max(), 2) if not premarket_df.empty else None
        data["premarketLow"] = round(premarket_df["Low"].min(), 2) if not premarket_df.empty else None
        data["prevHigh"] = round(rth_df["High"].max(), 2) if not rth_df.empty else None
        data["prevLow"] = round(rth_df["Low"].min(), 2) if not rth_df.empty else None
    except Exception as e:
        print(f"⚠️ Failed to fetch intraday data for {symbol}: {e}")
        data["premarketHigh"] = None
        data["premarketLow"] = None
        data["prevHigh"] = None
        data["prevLow"] = None

    if top_volume_symbols and symbol in top_volume_symbols:
        tier3.append("Top 5 Volume Gainer")

    score = 3 * len(tier1) + 2 * len(tier2) + 1 * len(tier3)
    data["tier1"] = tier1
    data["tier2"] = tier2
    data["tier3"] = tier3
    data["tags"] = tags
    data["score"] = score
    data["tier1_hits"] = len(tier1)
    data["tier2_hits"] = len(tier2)
    data["tier3_hits"] = len(tier3)

    if (
        tv_price is None or tv_price <= 0 or
        rel_vol is None or rel_vol < 0.3 or
        (avg_volume is not None and avg_volume < 1_000_000) or
        score == 0
    ):
        data["isBlocked"] = True
    else:
        data["isBlocked"] = False

    return data


def enrich_universe():
    print("🚀 Starting enrichment...")
    raw_path = get_latest_raw_universe_path()
    print(f"🧪 Using raw file: {raw_path}")

    if not raw_path:
        print("❌ No valid raw universe file found.")
        return

    with open(raw_path, "r") as f:
        raw_universe = json.load(f)

    print(f"📦 Loaded {len(raw_universe)} tickers to enrich")

    enriched_universe = {}
    test_symbols = {"SPY", "AAPL", "TSLA", "GOOGL", "NVDA"}

    volume_ranks = sorted(
        [
            (symbol, data.get("signals", {}).get("relVolume", 0))
            for symbol, data in raw_universe.items()
            if symbol in test_symbols
        ],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    top_volume_symbols = {symbol for symbol, _ in volume_ranks}

    for symbol, data in raw_universe.items():
        if symbol not in test_symbols:
            continue
        enriched = enrich_ticker(symbol, data, top_volume_symbols)
        enriched_universe[symbol] = enriched

    today = datetime.today().strftime("%Y-%m-%d")
    enriched_path = os.path.join(CACHE_DIR, f"{ENRICHED_PREFIX}{today}.json")
    with open(enriched_path, "w") as f:
        json.dump(enriched_universe, f, indent=2)

    passed = sum(1 for d in enriched_universe.values() if not d.get("isBlocked"))
    blocked = sum(1 for d in enriched_universe.values() if d.get("isBlocked"))
    print(f"✅ Enriched universe saved to {enriched_path}")
    print(f"✅ {passed} tickers passed filters")
    print(f"🚫 {blocked} tickers blocked by risk")

    os.makedirs("backend/cache", exist_ok=True)
    frontend_path = os.path.join("backend/cache/autowatchlist_cache.json")
    with open(frontend_path, "w") as f:
        json.dump(enriched_universe, f, indent=2)


if __name__ == "__main__":
    enrich_universe()
