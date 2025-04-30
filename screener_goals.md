# ✅ Stock Screener v3.6 – Final Goals Before v3.7

> **Status:** Stable daily-use build  
> **Next phase:** Universe Builder + Automation + Risk Logic Fixes  
> **Tag:** `v3.6-final`

---

## ✅ COMPLETED

### Tier Logic
- Tier 1: Gap Up / Gap Down  
- Tier 1: Break Above/Below 9:30–9:40 Range  
- Tier 1: High Relative Volume  
- Tier 2: Early % Move  
- Tier 2: Squeeze Watch  
- Tier 2: Sector Rotation  
- Tier 3: High Volume  
- Tier 3: Top 5 Volume Gainers  
- Tier 3: Near Multi-Day High / Low  
- Tier 3: High Volume, No Breakout  

### Risk Filters
- Low Liquidity  
- Wide Spread  

### Data & Enrichment
- TradingView + yfinance merged (`tv_signals.json`)  
- Sector ETF scraper (`sector_etf_prices.json`)  
- 5-min candle scraper for 9:30–9:40 range  
- Short Interest loader  
- Multi-day high/low logic  
- Full scored universe (`universe_scored_*.json`)  
- AutoWatchlist builder working and displayed in frontend  

### Backend Architecture
- Scoring dictionaries for Tiers and Risk  
- `apply_signal_flags()` and `score()`  
- `run_pipeline.py` as orchestration layer  
- Modular flow with caching  
- Stable FastAPI backend endpoints  

### Frontend UI
- `/tracker` view shows: Tiers, Score, Tags, Risk flags  
- Toggle for: T1–T3, Risk filter, Tag filters, Sort  
- Responsive and styled per design spec  

---

## 🔄 IN PROGRESS / PARTIAL

- [~] Tier 1: Momentum Confluence (needs TradingView premarket levels)  
- [~] Scheduler system for auto-refresh (cron or APScheduler)  
- [~] Daily refresh runs manually for now  

---

## 🛠️ UPCOMING (v3.7)

### Backend Enhancements
- [ ] Fix AutoWatchlist risk toggle logic (UI not honoring blocked stocks correctly)  
- [ ] Universe Builder (dynamic L1–L3 tagging, CSV-driven)  
- [ ] Fallback logic for failed yfinance pulls  
- [ ] Timestamp injection into all cache files  
- [ ] Risk “No Reliable Price” logic  

### Automation
- [ ] `daily_refresh.py` timed run (before 9:00AM)  
- [ ] Modular runner script (`runner.py`)  
- [ ] Skip scraper if cache is fresh (timestamp check)  

### Scraper System
- [ ] Wrap scrapers as functions not raw scripts  
- [ ] Prepare for source swapping (TV as primary)  
- [ ] Add stealth options to TradingView scraper  

### Frontend Goals
- [ ] Sector Rotation tab  
- [ ] Add frontend config (e.g. `rel_vol` threshold)  
- [ ] UI badge for cache timestamp freshness  
- [ ] Add “Top 3 Only” or “Show Blocked” toggles  

### Long-Term / Advanced
- [ ] Options data (GEX, Vanna, Charm)  
- [ ] Sentiment overlays (SPY, VIX)  
- [ ] Screener builder or rule editor  
- [ ] Export / Alerts for top picks  
- [ ] Replay engine for backtesting signals  