import json
import pandas as pd
import os
from datetime import datetime
from backend.path_helpers import get_latest_universe_path
from backend.fetch_fallback_price import fetch_fallback_price

CACHE_PATH = "backend/cache/autowatchlist_cache.json"

def is_cache_fresh(path):
    if not os.path.exists(path):
        return False
    modified_time = datetime.fromtimestamp(os.path.getmtime(path))
    return modified_time.date() == datetime.now().date()

def build_screening_output():
    enriched_path = get_latest_universe_path()
    if not enriched_path:
        raise FileNotFoundError("❌ No enriched universe file found.")

    with open(enriched_path, "r") as f:
        raw = json.load(f)

    for symbol, row in raw.items():
        row["symbol"] = symbol

    df = pd.DataFrame(list(raw.values()))

    for col in ["tier1_hits", "tier2_hits", "tier3_hits", "isBlocked"]:
        if col not in df.columns:
            df[col] = 0 if "hits" in col else False

    df["score"] = (
        df["tier1_hits"] * 3 +
        df["tier2_hits"] * 2 +
        df["tier3_hits"]
    )

    df = df[df["isBlocked"] == False].copy()
    df["price"] = df.apply(fetch_fallback_price, axis=1)
    df.sort_values("score", ascending=False, inplace=True)

    # Save to cache
    cache_dict = {row["symbol"]: row for row in df.to_dict("records")}
    with open(CACHE_PATH, "w") as f:
        json.dump(cache_dict, f, indent=2)

    return df.reset_index(drop=True)
