
# Stock Screener v3.6 – Project Goals (as of 2025-04-25)

## ✅ COMPLETED GOALS

### Tier Logic
- [x] Tier 1: Gap Up / Gap Down
- [x] Tier 1: Break Above/Below 9:30–9:40 Range
- [x] Tier 1: High Relative Volume (`rel_vol > 1.5`)
- [x] Tier 2: Early % Move (9:30–9:35)
- [x] Tier 3: High Volume
- [x] Tier 3: Top 5 Volume Gainers

### Risk Filters
- [x] Low Liquidity
- [x] Wide Spread

### Data Sources & Enrichment
- [x] `tv_signals.json` with yfinance proxy
- [x] `sector_etf_prices.json` scrape
- [x] `candles_5m.json` for range break logic
- [x] `short_interest.json` loaded
- [x] Universe cache with L1/L2/L3 logic
- [x] `universe_enriched.json` merge complete
- [x] `universe_scored.json` output

### Backend Architecture
- [x] Central scoring dictionaries (TIER_1/2/3, risk flags)
- [x] `apply_signal_flags()` logic
- [x] `score()` function
- [x] Risk filter injection
- [x] Use `get_latest_file()` logic
- [x] Progress loader in TV scraper (`tqdm`)
- [x] Modular flow (scrape → enrich → score)

## ⚒️ IN PROGRESS / PARTIALLY COMPLETE

### Tier Logic (Partial)
- [~] Tier 2: Squeeze Watch (needs `volatility` logic)
- [~] Tier 3: High Volume, No Breakout (missing breakout logic)

### Enrichment & Signal Engine
- [~] Sector ETF scraped — scoring logic not wired
- [~] Short interest used — volatility component missing

## ❌ NOT YET STARTED

### Tier Logic
- [ ] Tier 1: Momentum Confluence (PM + prev day)
- [ ] Tier 2: Sector Rotation logic
- [ ] Tier 3: Near Multi-Day High

### Risk Filters
- [ ] No Reliable Price / Ghost Print logic

### Backend Features
- [ ] Add debug logs for scoring breakdown
- [ ] Include `reasons[]` in output
- [ ] Add timestamps to all cache files
- [ ] Build `runner.py` for full pipeline
- [ ] Fallback logic if yfinance fails mid-run

### Timed Automation
- [ ] Add `APScheduler` or `cron` support for scheduled pulls
- [ ] Skip scraping if cache is fresh

### TradingView Scraper Upgrade
- [ ] Add stealth features (user-agent, delay randomization)
- [ ] Handle rate limiting and fallback logging
- [ ] Consider Playwright-based option

### Frontend Goals
- [ ] Frontend UI config (e.g. rel_vol threshold)
- [ ] Toggle tier visibility
- [ ] Show triggered signals per ticker
- [ ] Add Sector Rotation tab
- [ ] Show score + tier tags in UI
- [ ] “Top 3 Only” / Blocked ticker views
- [ ] UI indicators for data freshness

### Long-Term / Advanced
- [ ] Relative Volume Percentiles
- [ ] Options-based GEX / vanna / charm integration
- [ ] Sentiment overlays (e.g. SPY + VIX)
- [ ] Screener builder or custom logic mode
- [ ] Backtest / replay past signals
- [ ] Export or alert system
