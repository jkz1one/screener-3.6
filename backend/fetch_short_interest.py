
import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

BASE_URLS = [
    "https://www.highshortinterest.com/all/1",
    "https://www.highshortinterest.com/all/2"
]

OUTPUT_PATH = "backend/cache/short_interest.json"

def is_valid_ticker(ticker):
    return ticker.isalpha() and 1 <= len(ticker) <= 5 and ticker.isupper()

def fetch_high_short_interest():
    data = {}
    for url in BASE_URLS:
        print(f"🔍 Fetching: {url}")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"❌ Failed to fetch {url}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        if not table:
            print(f"❌ No table found at {url}")
            continue

        rows = table.find_all("tr")[1:]  # skip header
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 4:
                ticker = cols[0].text.strip().upper()
                if not is_valid_ticker(ticker):
                    continue
                try:
                    short_percent = float(cols[3].text.strip().replace("%", "")) / 100
                    data[ticker] = {
                        "shortPercentOfFloat": round(short_percent, 4)
                    }
                except ValueError:
                    continue

    sorted_data = dict(sorted(data.items()))

    Path("backend/cache").mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(sorted_data, f, indent=2)
    print(f"✅ Saved short interest data for {len(sorted_data)} valid tickers to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_high_short_interest()
