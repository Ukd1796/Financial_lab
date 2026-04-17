# api/main.py
#
# FastAPI application entry point for Financial Lab.
#
# Run with:
#   uvicorn api.main:app --reload --port 8000
#
# CORS is configured to allow the Vite dev server (localhost:5173)
# and can be extended for the production frontend origin via the
# ALLOWED_ORIGINS environment variable (comma-separated).

import os

from dotenv import load_dotenv

# Load .env before any service/router imports so OPENAI_API_KEY and other
# variables are available when module-level code runs (e.g. OpenAI client init).
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.store import init_db
from api.routers import backtest, broker, market, paper_trade, strategies, users

app = FastAPI(
    title="Financial Lab API",
    description="Backend for QuantCanvas UI — exposes regime, strategy, backtest and paper-trade data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
_extra_origins = [
    o.strip()
    for o in os.environ.get("ALLOWED_ORIGINS", "").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"] + _extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def on_startup():
    """Initialise SQLite tables for API state on first boot."""
    init_db()


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(market.router,      prefix="/api/market",      tags=["Market"])
app.include_router(strategies.router,  prefix="/api/strategies",  tags=["Strategies"])
app.include_router(backtest.router,    prefix="/api/backtest",    tags=["Backtest"])
app.include_router(paper_trade.router, prefix="/api/paper-trade", tags=["Paper Trade"])
app.include_router(broker.router,      prefix="/api/broker",      tags=["Broker"])
app.include_router(users.router,       prefix="/api/users",       tags=["Users"])


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["Health"])
def health():
    return {"status": "ok"}
