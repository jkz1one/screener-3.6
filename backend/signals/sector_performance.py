import json
import os

# Static map of sector ETFs to their names
SECTOR_ETFS = {
    "XLF": "Financials",
    "XLK": "Technology",
    "XLE": "Energy",
    "XLV": "Healthcare",
    "XLY": "Consumer Discretionary",
    "XLI": "Industrials",
    "XLP": "Consumer Staples",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
    "XLB": "Materials",
    "XLCD": "Communication Services"
}

SECTOR_PRICES_PATH = "backend/cache/sector_etf_prices.json"

def get_sector_rotation_rankings():
    if not os.path.exists(SECTOR_PRICES_PATH):
        print("❌ No sector ETF price data found.")
        return set(), set()

    with open(SECTOR_PRICES_PATH, "r") as f:
        sector_prices = json.load(f)

    sector_changes = {}
    for etf, sector in SECTOR_ETFS.items():
        data = sector_prices.get(etf)
        if not data:
            continue
        price = data.get("tv_price")
        prev = data.get("prevClose")
        if price and prev and prev > 0:
            change = ((price - prev) / prev) * 100
            sector_changes[sector] = round(change, 2)

    ranked = sorted(sector_changes.items(), key=lambda x: x[1], reverse=True)
    top2 = set([s for s, _ in ranked[:2]])
    bottom2 = set([s for s, _ in ranked[-2:]])
    return top2, bottom2
