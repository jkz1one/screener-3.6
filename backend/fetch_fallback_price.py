import yfinance as yf

def fetch_yf_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info.get("last_price") or ticker.history(period="1d")["Close"].iloc[-1]
        return round(price, 2)
    except Exception as e:
        print(f"⚠️ yfinance fallback failed for {symbol}: {e}")
        return None


def fetch_fallback_price(row):
    return fetch_yf_price(row["symbol"])
