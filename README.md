# 📊 Stock Screener 3.6 – Momentum & Risk-Aware Watchlist Builder

A real-time stock scanning tool that builds a tiered watchlist using premarket signals, sector rotation, volume, and risk filters. Built with FastAPI + Next.js.

---
![image](https://github.com/user-attachments/assets/d5ee4dfc-0336-4804-939b-82a089c4a1f4)

## 🔧 How It Works

### 📦 Daily Refresh
- `daily_refresh.py`: Must be run once per day to fetch and cache fresh data. **9:40AM EST is optimal run time** 
  - [ Scrape TV Signals ] → `tv_signals.json`
  - [ Scrape Sector ETFs ] → `sector_etf_prices.json`
  - [ Scrape Multi-Day High/Lows ] → `multi_day_levels.json`
  - [ Scrape Short Interest ] → `short_interest.json`
  - [ YFinance Enrichment ] → `universe_enriched_*.json`

### ⚙️ Backend Pipeline
- `run_pipeline.py`: Runs the full enrichment + scoring + watchlist build
- `enrich_universe.py`: Pulls in live volume/price signals from TradingView and Yahoo
- `screenbuilder.py`: Scores each stock based on Tier 1–3 logic and risk flags
- `watchlist_builder.py`: Builds the final filtered and tagged watchlist (used by frontend)

### 🖥️ Frontend

- Located at `/tracker`
- Displays:
  - Score
  - Tier hits (T1, T2, T3)
  - Risk flags (e.g. "Low Liquidity", "Wide Spread")
  - Tags like **Strong Setup**, **Squeeze Watch**, **Early Watch**
- UI filters for:
  - T1/T2/T3 visibility
  - Risk toggle (show/hide risk-blocked tickers)
  - Tag filtering and sort

---

## ▶️ How to Run

```bash
# 1. Refresh daily signals before scoring (once per day)
python3 backend/daily_refresh.py

# 2. Run the full pipeline (enrich + score + build watchlist)
python3 run_pipeline.py

# 3. Start backend server (FastAPI)
uvicorn backend.main:app --reload --port 8000

# 4. Start frontend (Next.js)
npm run dev
```
---

## 📡 API Endpoints

| Endpoint                | Description                           |
|------------------------|---------------------------------------|
| `/api/autowatchlist`   | Returns the final filtered watchlist  |
| `/api/universe`        | Returns the scored universe JSON      |
| `/api/raw`             | Returns the raw, enriched universe    |
| `/api/sector`          | Returns sector ETF data               |
| `/api/cache-timestamps`| Returns freshness metadata for cache  |

---

## 🧩 Goals / To-Do

- [ ] ✅ Finalize Tier 1–3 scoring logic (mostly done)
- [ ] 🛠 Fix `risk: off` toggle to correctly include low-score, high-risk names
- [ ] ⏰ Auto Pull for Daily Refresh
- [ ] 📊 Add UI breakdown of scoring logic and tier definitions
- [ ] 🔁 Add caching freshness indicators to frontend
- [ ] 🧼 Cleanup and document universe builder sources

