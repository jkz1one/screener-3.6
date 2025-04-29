from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = "backend/cache"

def load_json_file(path: str, label: str):
    if not os.path.exists(path):
        return JSONResponse(
            {"error": f"{label} not found at path: {path}"},
            status_code=404
        )
    with open(path, "r") as f:
        return JSONResponse(content=json.load(f))

@app.get("/api/universe")
async def get_universe():
    path = os.path.join(CACHE_DIR, "universe_scored.json")
    return load_json_file(path, "Scored universe")

@app.get("/api/sector")
async def get_sector_rotation():
    path = os.path.join(CACHE_DIR, "sector_etf_prices.json")
    return load_json_file(path, "Sector ETF data")

@app.get("/api/raw")
async def get_universe_raw():
    path = os.path.join(CACHE_DIR, "universe_cache.json")
    return load_json_file(path, "Raw universe")

@app.get("/api/cache-timestamps")
async def get_cache_timestamps():
    """Returns last modified timestamps and freshness status for key cache files."""
    files = [
        "tv_signals.json",
        "sector_etf_prices.json",
        "candles_5m.json",
        "multi_day_levels.json",
        "short_interest.json",
        "universe_enriched.json",
        "universe_scored.json"
    ]

    now = datetime.now()
    freshness_minutes = 15
    output = {}

    for fname in files:
        full_path = os.path.join(CACHE_DIR, fname)
        if os.path.exists(full_path):
            modified_ts = os.path.getmtime(full_path)
            modified_dt = datetime.fromtimestamp(modified_ts)
            is_fresh = (now - modified_dt).total_seconds() < freshness_minutes * 60
            output[fname] = {
                "last_modified": modified_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "is_fresh": is_fresh
            }
        else:
            output[fname] = {
                "last_modified": "Missing",
                "is_fresh": False
            }

    return JSONResponse(content=output)

