import os
import glob

def get_latest_universe_path(cache_dir: str = "backend/cache") -> str | None:
    pattern = os.path.join(cache_dir, "universe_enriched_*.json")
    files = glob.glob(pattern)
    if not files:
        print("❌ No universe enriched cache files found.")
        return None
    latest = max(files, key=os.path.getmtime)
    print(f"✅ Latest universe file found: {latest}")
    return latest


def get_data_path(filename: str, subdir: str = "backend/cache") -> str:
    return os.path.join(subdir, filename)
