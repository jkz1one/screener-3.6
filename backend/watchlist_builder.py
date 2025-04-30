# backend/watchlist_builder.py

import os
import json

CACHE_DIR = "backend/cache"

def build_autowatchlist(scored_path=None):
    if scored_path is None:
        # Default to latest scored file if not provided
        files = [f for f in os.listdir(CACHE_DIR) if f.startswith("universe_scored_") and f.endswith(".json")]
        if not files:
            raise FileNotFoundError("No scored universe file found.")
        files.sort(key=lambda f: os.path.getmtime(os.path.join(CACHE_DIR, f)), reverse=True)
        scored_path = os.path.join(CACHE_DIR, files[0])

    with open(scored_path, "r") as f:
        universe = json.load(f)

    watchlist = {}
    for symbol, info in universe.items():
        score = info.get("score", 0)
        signals = info.get("signals", {})
        reasons = []
        if signals.get("low_liquidity"):
                reasons.append("Low Liquidity")
        if signals.get("wide_spread"):
                reasons.append("Wide Spread")

        is_blocked = len(reasons) > 0

        if score >= 3 or is_blocked:

            tags = []

            # Tag: Strong Setup = at least 2 Tier 1 confluence
            t1_signals = ["gap_up", "gap_down", "break_above_range", "break_below_range"]
            t1_hits = sum(1 for k in t1_signals if signals.get(k))
            if t1_hits >= 2:
                tags.append("Strong Setup")


            # Tag: Squeeze Watch
            if signals.get("squeeze_watch"):
                tags.append("Squeeze Watch")

            # Tag: Early Watch
            if signals.get("early_move"):
                tags.append("Early Watch")

            info["tags"] = tags
            info["isBlocked"] = is_blocked
            info["reasons"] = reasons
            watchlist[symbol] = info

    out_path = os.path.join(CACHE_DIR, "autowatchlist_cache.json")
    with open(out_path, "w") as f:
        json.dump(watchlist, f, indent=2)

    print(f"✅ AutoWatchlist built with {len(watchlist)} entries → {out_path}")
    return watchlist
