import subprocess

print("🔁 [1/4] Building base universe...")
subprocess.run(["python3", "backend/enrich_universe.py"], check=True)

print("📊 [2/4] Scraping sector ETF prices...")
subprocess.run(["python3", "scrape_sector_prices.py"], check=True)

print("🧠 [3/4] Merging signals and injecting sector data...")
subprocess.run(["python3", "backend/merge_signals_to_universe.py"], check=True)

print("⚙️ [4/4] Scoring and saving autowatchlist output...")
subprocess.run(["python3", "-m", "backend.screenbuilder"], check=True)

print("✅ Pipeline complete. Watchlist and cache updated.")
