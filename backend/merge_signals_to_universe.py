import os
import json
from datetime import datetime
from pytz import timezone

RAW_UNIVERSE = "backend/cache/universe_cache.json"
TV_SIGNALS = "backend/cache/tv_signals.json"

def merge_signals():
    if not os.path.exists(RAW_UNIVERSE):
        raise FileNotFoundError("Missing universe_cache.json")
    if not os.path.exists(TV_SIGNALS):
        raise FileNotFoundError("Missing tv_signals.json")

    with open(RAW_UNIVERSE, "r") as f:
        base_universe = json.load(f)

    with open(TV_SIGNALS, "r") as f:
        tv_raw = json.load(f)

    if isinstance(tv_raw, list):
        tv_data = {entry["symbol"]: entry for entry in tv_raw if "symbol" in entry}
    else:
        tv_data = tv_raw

    et = timezone("US/Eastern")
    now_et = datetime.now(et)
    after_935 = now_et.hour > 9 or (now_et.hour == 9 and now_et.minute >= 35)

    merged = {}
    for symbol, row in base_universe.items():
        try:
            if not row.get("sector"):
                try:
                    import yfinance as yf
                    info = yf.Ticker(symbol).info
                    sector = info.get("sector", None)
                    if sector:
                        row["sector"] = sector
                        print(f"✅ Pulled sector for {symbol}: {sector}")
                    else:
                        print(f"⚠️ No sector found for {symbol}")
                except Exception as e:
                    print(f"❌ Failed to fetch sector for {symbol}: {e}")

            data = tv_data.get(symbol, {})
            signals = {}

            tv_price = data.get("tv_price")
            prev_close = row.get("prevClose") or data.get("prevClose")

            if tv_price and prev_close and prev_close > 0:
                tv_change = ((tv_price - prev_close) / prev_close) * 100
                signals["gapPercent"] = round(tv_change, 2)

            row["signals"] = signals
            row["tv_price"] = tv_price
            row["tv_volume"] = data.get("tv_volume")
            row["tv_changePercent"] = data.get("tv_changePercent")

            merged[symbol] = row

        except Exception as e:
            print(f"❌ Merge failed for {symbol}: {e}")

    # Save enriched universe
    out_path = f"backend/cache/universe_enriched_{datetime.now().date()}.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(merged, f, indent=2)
    print(f"📦 Enriched universe saved to {out_path}")

    # Save updated universe (with sectors) back to cache
    with open(RAW_UNIVERSE, "w") as f:
        json.dump(base_universe, f, indent=2)
    print(f"📝 Base universe updated with sectors: {RAW_UNIVERSE}")

if __name__ == "__main__":
    merge_signals()
