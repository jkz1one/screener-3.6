import json
import os
import yfinance as yf

# Sector ETF symbols mapped to sector names
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
    "XLC": "Communication Services"
}

CACHE_PATH = "backend/cache/sector_etf_prices.json"

def fetch_sector_prices():
    data = {}
    for symbol in SECTOR_ETFS:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("regularMarketPrice")
            prev_close = info.get("previousClose")

            if price and prev_close:
                data[symbol] = {
                    "tv_price": round(price, 2),
                    "prevClose": round(prev_close, 2)
                }
                print(f"✅ {symbol}: {data[symbol]}")
            else:
                print(f"⚠️ Missing price or prevClose for {symbol}")
        except Exception as e:
            print(f"❌ Failed to fetch {symbol}: {e}")

    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"📦 Sector ETF data saved to {CACHE_PATH}")

if __name__ == "__main__":
    fetch_sector_prices()
