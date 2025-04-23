
import json
from backend.utils.fetch_fallback_price import fetch_yf_price

def load_tv_signals(path="backend/cache/tv_signals.json"):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return {entry["symbol"]: entry for entry in data}
    except Exception as e:
        print(f"⚠️ Failed to load tv_signals.json: {e}")
        return {}

def merge_tv_signals(universe, tv_map):
    for stock in universe:
        sym = stock.get("symbol")
        tv_data = tv_map.get(sym)

        if tv_data:
            stock["tv_price"] = tv_data.get("price")
            stock["tv_volume"] = tv_data.get("volume")
            stock["tv_changePercent"] = tv_data.get("changePercent")
            stock["premarketHigh"] = tv_data.get("premarketHigh")
            stock["premarketLow"] = tv_data.get("premarketLow")
        else:
            fallback_price = fetch_yf_price(sym)
            stock["tv_price"] = fallback_price
            stock["tv_volume"] = None
            stock["tv_changePercent"] = None
            stock["premarketHigh"] = None
            stock["premarketLow"] = None

    return universe
