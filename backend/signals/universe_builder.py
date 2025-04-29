import os, json

def load_latest_universe():
    path = os.path.join(os.path.dirname(__file__), "cache", "universe_cache.json")
    if not os.path.exists(path):
        raise FileNotFoundError("⚠️ universe_cache.json not found.")
    with open(path, "r") as f:
        return json.load(f)
