import json
import os
from datetime import datetime
import pytz
from tqdm import tqdm

CACHE_DIR = "backend/cache"

def get_latest_universe_file():
    files = [
        os.path.join(CACHE_DIR, f)
        for f in os.listdir(CACHE_DIR)
        if f.startswith("universe_enriched_") and f.endswith(".json") and not f.endswith("_scored.json")
    ]
    if not files:
        raise FileNotFoundError("No enriched universe files found.")
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

UNIVERSE_PATH = get_latest_universe_file()
current_date_str = datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
OUTPUT_PATH = os.path.join(CACHE_DIR, f"universe_scored_{current_date_str}.json")

TIER_1 = {
    "gap_up": 3,
    "gap_down": 3,
    "break_above_range": 3,
    "break_below_range": 3,
    "high_rel_vol": 3,
}

TIER_2 = {
    "early_move": 2,
    "squeeze_watch": 2,
    "strong_sector": 2,
    "weak_sector": 2,
}

TIER_3 = {
    "near_range_high": 1,
    "high_volume": 1,
    "top_volume_gainer": 1,
    "near_multi_day_high": 1,
    "near_multi_day_low": 1,
    "high_volume_no_breakout": 1
}

RISK_FLAGS = {
    "low_liquidity": -3,
    "wide_spread": -3,
}

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def score(info):
    signals = info.get("signals", {})
    score = 0
    for sig in TIER_1:
        if signals.get(sig):
            score += TIER_1[sig]
    for sig in TIER_2:
        if signals.get(sig):
            score += TIER_2[sig]
    for sig in TIER_3:
        if signals.get(sig):
            score += TIER_3[sig]
    for risk in RISK_FLAGS:
        if signals.get(risk):
            score += RISK_FLAGS[risk]
    return score

def build_tier_hits(info):
    signals = info.get("signals", {})
    return {
        "T1": [sig for sig in TIER_1 if signals.get(sig)],
        "T2": [sig for sig in TIER_2 if signals.get(sig)],
        "T3": [sig for sig in TIER_3 if signals.get(sig)],
    }

def main():
    print("🚀 Starting enrichment and scoring...")
    universe = load_json(UNIVERSE_PATH)
    print(f"📦 Loaded {len(universe)} tickers to enrich")
    print("⚙️ Scoring tickers...")
    for symbol in tqdm(universe):
        s = score(universe[symbol])
        universe[symbol]["score"] = s
        universe[symbol]["tierHits"] = build_tier_hits(universe[symbol])  # ✅ Add this line!

    with open(OUTPUT_PATH, "w") as f:
        json.dump(universe, f, indent=2)
    print(f"✅ Enriched universe saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
