# backend/run_pipeline.py

import subprocess
import os
from datetime import datetime

def check_required_cache():
    today = datetime.now().strftime("%Y-%m-%d")
    CACHE_DIR = "backend/cache"
    required_files = [
        f"tv_signals.json",
        f"sector_etf_prices.json",
        f"candles_5m.json",
        f"multi_day_levels.json",
        f"short_interest.json",
    ]
    missing = []
    for fname in required_files:
        full_path = os.path.join(CACHE_DIR, fname)
        if not os.path.exists(full_path):
            missing.append(fname)

    enriched_file = os.path.join(CACHE_DIR, f"universe_enriched_{today}.json")
    if os.path.exists(enriched_file):
        pass  # ok
    else:
        missing.append(f"universe_enriched_{today}.json (expected from refresh)")

    if missing:
        print("\n❌ Missing or outdated cache files detected:")
        for m in missing:
            print(f" - {m}")
        raise SystemExit("\n🛑 Aborting pipeline! Run Daily Refresh first.\n")

print("🔎 Verifying cache freshness before pipeline...")
check_required_cache()

print("🔁 [1/2] Building base universe...")
subprocess.run(["python3", "backend/enrich_universe.py"], check=True)

print("⚙️ [2/2] Scoring and saving autowatchlist output...")
subprocess.run(["python3", "-m", "backend.screenbuilder"], check=True)

print("✅ Pipeline complete. Watchlist and cache updated.")
