# backend/cache_manager.py

import os
import time
from datetime import datetime

# Files we want to manage
CACHE_DIR = "backend/cache"
IMPORTANT_FILES = [
    "tv_signals.json",
    "sector_etf_prices.json",
    "candles_5m.json",
    "multi_day_levels.json",
    "short_interest.json",
    # Universe files generated per day
    "universe_enriched",
    "universe_scored"
]

# Helper

def is_today(file_path):
    try:
        modified_time = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(modified_time).date()
        today = datetime.now().date()
        return file_date == today
    except Exception:
        return False

def cleanup_old_files():
    print("🧹 Starting Cache Cleanup...")
    
    deleted_count = 0
    skipped_count = 0

    for base_name in IMPORTANT_FILES:
        found_today = False
        candidates = []

        for fname in os.listdir(CACHE_DIR):
            if fname.startswith(base_name):
                full_path = os.path.join(CACHE_DIR, fname)
                candidates.append(full_path)
                if is_today(full_path):
                    found_today = True

        if found_today:
            for path in candidates:
                if not is_today(path):
                    os.remove(path)
                    deleted_count += 1
        else:
            skipped_count += 1
            print(f"⚠️ No fresh {base_name} file today. Skipping delete.")

    print(f"✅ Cache cleanup complete: {deleted_count} files deleted, {skipped_count} skipped.")

if __name__ == "__main__":
    cleanup_old_files()
