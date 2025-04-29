# backend/cache_manager.py

import os
import json
import time
from datetime import datetime

# --- Config ---
CACHE_DIR = "backend/cache"
IMPORTANT_FILES = [
    "tv_signals.json",
    "sector_etf_prices.json",
    "candles_5m.json",
    "multi_day_levels.json",
    "short_interest.json",
    "universe_enriched",
    "universe_scored"
]

# --- Cleanup Functions ---

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

    print(f"✅ Cache cleanup complete: {deleted_count} files deleted, {skipped_count} skipped.\n")

# --- Audit Functions ---

def audit_cache_files():
    print("🔍 Starting Cache Audit...")

    issues_found = False

    # Check TV Signals
    tv_path = os.path.join(CACHE_DIR, "tv_signals.json")
    if os.path.exists(tv_path):
        with open(tv_path, "r") as f:
            tv_data = json.load(f)
        old_entries = [k for k, v in tv_data.items() if "timestamp" not in v]
        if old_entries:
            print(f"⚠️ {len(old_entries)} tickers missing timestamp in tv_signals.json")
            issues_found = True
    else:
        print("⚠️ tv_signals.json missing!")
        issues_found = True

    # Check Sector ETF Prices
    sector_path = os.path.join(CACHE_DIR, "sector_etf_prices.json")
    if os.path.exists(sector_path):
        with open(sector_path, "r") as f:
            sector_data = json.load(f)
        expected_etfs = ["XLF", "XLK", "XLE", "XLV", "XLY", "XLI", "XLP", "XLU", "XLRE", "XLB", "XLC"]
        missing_etfs = [etf for etf in expected_etfs if etf not in sector_data]
        if missing_etfs:
            print(f"⚠️ Missing sector ETF prices for: {missing_etfs}")
            issues_found = True
    else:
        print("⚠️ sector_etf_prices.json missing!")
        issues_found = True

    # Check 5m Candles
    candles_path = os.path.join(CACHE_DIR, "candles_5m.json")
    if os.path.exists(candles_path):
        with open(candles_path, "r") as f:
            candle_data = json.load(f)
        empty_candles = [symbol for symbol, candles in candle_data.items() if not candles]
        if empty_candles:
            print(f"⚠️ {len(empty_candles)} tickers have no 5m candles")
            issues_found = True
    else:
        print("⚠️ candles_5m.json missing!")
        issues_found = True

    # Check Multi-Day Levels
    multi_path = os.path.join(CACHE_DIR, "multi_day_levels.json")
    if os.path.exists(multi_path):
        with open(multi_path, "r") as f:
            multi_data = json.load(f)
        missing_levels = [symbol for symbol, levels in multi_data.items() if "high" not in levels or "low" not in levels]
        if missing_levels:
            print(f"⚠️ {len(missing_levels)} tickers missing multi-day high/low levels")
            issues_found = True
    else:
        print("⚠️ multi_day_levels.json missing!")
        issues_found = True

    # Check Short Interest
    short_path = os.path.join(CACHE_DIR, "short_interest.json")
    if os.path.exists(short_path):
        with open(short_path, "r") as f:
            short_data = json.load(f)
        if len(short_data) < 50:
            print(f"⚠️ Only {len(short_data)} short interest tickers found — expected more")
            issues_found = True
    else:
        print("⚠️ short_interest.json missing!")
        issues_found = True

    if not issues_found:
        print("✅ Cache Audit Passed — All major caches healthy.\n")
    else:
        print("⚠️ Cache Audit found some problems. Check warnings above.\n")

# --- Main Execution ---

if __name__ == "__main__":
    cleanup_old_files()
    audit_cache_files()
