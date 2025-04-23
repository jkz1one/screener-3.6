from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from backend.screenbuilder import build_screening_output, is_cache_fresh

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/autowatchlist/")
def get_watchlist():
    cache_path = "backend/cache/autowatchlist_cache.json"
    if is_cache_fresh(cache_path):
        try:
            with open(cache_path, "r") as f:
                raw = json.load(f)
            for symbol, row in raw.items():
                row["symbol"] = symbol
            return list(raw.values())
        except Exception as e:
            print(f"❌ Failed to load cache: {e}")

    # fallback to rebuild if cache missing or broken
    df = build_screening_output()
    return df.to_dict("records")

@app.get("/rebuild/")
def rebuild_watchlist():
    result = build_screening_output()
    return {"status": "rebuilt", "count": len(result)}
