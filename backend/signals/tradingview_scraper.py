
import asyncio
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_PATH = Path("backend/cache/tv_signals.json")

def parse_volume(volume_str):
    volume_str = volume_str.replace("\u202f", "").replace(",", "").strip()
    multiplier = 1
    if "K" in volume_str:
        multiplier = 1_000
        volume_str = volume_str.replace("K", "")
    elif "M" in volume_str:
        multiplier = 1_000_000
        volume_str = volume_str.replace("M", "")
    elif "B" in volume_str:
        multiplier = 1_000_000_000
        volume_str = volume_str.replace("B", "")
    try:
        return int(float(volume_str) * multiplier)
    except ValueError:
        return None

async def scrape_tradingview():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.tradingview.com/markets/stocks-usa/market-movers-active/")
        await page.wait_for_selector('table tr')

        rows = await page.query_selector_all("table tr")
        results = []

        for row in rows[1:]:
            try:
                cells = await row.query_selector_all("td")
                if len(cells) < 6:
                    continue

                raw_symbol = await cells[0].inner_text()
                clean_symbol = raw_symbol.strip().split("\n")[0]

                price = await cells[2].inner_text()
                change = await cells[3].inner_text()
                volume = await cells[4].inner_text()

                results.append({
                    "symbol": clean_symbol,
                    "price": float(price.replace(",", "").replace("USD", "").strip()),
                    "changePercent": float(change.replace("%", "").replace("+", "").replace("−", "-").strip()),
                    "volume": parse_volume(volume)
                })
            except Exception as e:
                print(f"⚠️ Error parsing row: {e}")

        await browser.close()

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with OUTPUT_PATH.open("w") as f:
            json.dump(results, f, indent=2)

        print(f"✅ Scraped and cleaned {len(results)} tickers to {OUTPUT_PATH}")

if __name__ == "__main__":
    asyncio.run(scrape_tradingview())
