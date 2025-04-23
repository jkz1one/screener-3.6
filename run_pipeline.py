import subprocess

print("🔁 [1/3] Building base universe...")
subprocess.run(["python3", "backend/enrich_universe.py"], check=True)

print("📊 [2/3] Scraping sector ETF prices...")
subprocess.run(["python3", "scrape_sector_prices.py"], check=True)

print("⚙️ [3/3] Scoring and saving autowatchlist output...")
subprocess.run(["python3", "-m", "backend.screenbuilder"], check=True)

print("✅ Pipeline complete. Watchlist and cache updated.")
