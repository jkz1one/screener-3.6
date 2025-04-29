# Stock Screener v3.6 – Project Goals (as of 2025-04-28)

# 🚀 Current Phase: **Late Phase 1 / Early Phase 2**
> (Tier Logic almost locked → Moving into Time Automation and Full Pipeline orchestration.)

## ✅ COMPLETED GOALS

### Tier Logic
- [x] Tier 1: Gap Up / Gap Down
- [x] Tier 1: Break Above/Below 9:30–9:40 Range
- [x] Tier 1: High Relative Volume (`rel_vol > 1.5`)
- [x] Tier 2: Early % Move (9:30–9:35)
- [x] Tier 2: Squeeze Watch (Short % + RelVol + Move)
- [x] Tier 2: Sector Rotation logic
- [x] Tier 3: High Volume
- [x] Tier 3: Top 5 Volume Gainers
- [x] Tier 3: Near Multi-Day High / Low
- [x] Tier 3: High Volume, No Breakout

### Risk Filters
- [x] Low Liquidity
- [x] Wide Spread

### Data Sources & Enrichment
- [x] `tv_signals.json` (TradingView + yfinance merged)
- [x] `sector_etf_prices.json` scrape
- [x] `candles_5m.json` for range break logic
- [x] `short_interest.json` loaded
- [x] `multi_day_levels.json` added (high/low)
- [x] Universe cache with L1/L2/L3 logic
- [x] `universe_enriched.json` merge complete
- [x] `universe_scored.json` output

### Backend Architecture
- [x] Central scoring dictionaries (TIER_1/2/3, risk flags)
- [x] `apply_signal_flags()` logic
- [x] `score()` function
- [x] Risk filter injection
- [x] Use `get_latest_file()` logic
- [x] Progress loader in scrapers (`tqdm`)
- [x] Modular flow (scrape → enrich → score)
- [x] Delete obsolete `yfinance_enrichment.py` after merger

---

## 🧹 Tiny Cosmetic Improvements
- [x] Collapse all data saves into clean `backend/cache/`
- [x] Uniform JSON file formats across scrapers
- [x] Smarter loading and error checking across scraper scripts

---

## ⚒️ IN PROGRESS / PARTIALLY COMPLETE
- [~] Tier 1: Momentum Confluence (PM high/low + prev day high/low)
- [~] Build lightweight scheduler script (timed scraper runner)
- [~] Time-align scraper tasks (4AM premarket jobs, 9:30AM open jobs, 9:40AM candle jobs)

---

## 🔥 New Goals Just Added
- [~] Build lightweight daily scheduler
- [~] Organize scraper times (4AM, 9:30AM, 9:40AM) 

---

## ❌ NOT YET STARTED

### Tier Logic
- [ ] Finalize Tier 1: Momentum Confluence logic

### Risk Filters
- [ ] No Reliable Price / Ghost Print logic

### Backend Features
- [ ] Build scraper module wrapper (functions not just raw scripts)
- [ ] Add batch loading support in scrapers (candles, TV signals, sector ETFs)
- [ ] Prepare scrapers for easy source swapping (e.g., TradingView full primary ready)
- [ ] Add debug logs for scoring breakdown
- [ ] Include `reasons[]` array in output
- [ ] Add timestamps inside all cache files
- [ ] Build `runner.py` for full pipeline automation
- [ ] Fallback logic if yfinance fails mid-run
- [ ] Build scoring anomaly validator script (for audit/debugging)

### Timed Automation
- [ ] Add `APScheduler` or `cron` support for timed scrapes
- [ ] Skip scraping if latest cache is still fresh (timestamp check)

### TradingView Scraper Upgrade
- [ ] Add stealth features (rotate user-agent, random delays)
- [ ] Handle rate limiting / fallback retries
- [ ] Consider Playwright-based scraping option
- [ ] Make TradingView scraping the **primary** source (replace yfinance dependency)

### Frontend Goals
- [ ] Frontend UI config (e.g., set relative volume threshold)
- [ ] Toggle tier visibility in UI
- [ ] Show triggered signals per ticker in UI
- [ ] Add Sector Rotation tab
- [ ] Show score + tier tags visually
- [ ] "Top 3 Only" / Blocked ticker toggle view
- [ ] UI indicators for cache freshness (timestamp display)

### Long-Term / Advanced
- [ ] Relative Volume Percentiles (dynamic scaling)
- [ ] Options-based GEX, Vanna, Charm signal integration
- [ ] Sentiment overlays (SPY + VIX confluence, sector strength overlays)
- [ ] Screener builder or custom logic editor (Management Panel front end)
- [ ] Backtest / replay engine (past signals validation)
- [ ] Export or alert system for daily top signals
- [ ] Expand universe with more tickers (e.g., mid-caps for squeeze watch)
- [ ] Fix or rebuild the Watchlist Puller logic
