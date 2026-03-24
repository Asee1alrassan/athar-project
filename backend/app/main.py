"""
ATHAR — Digital Observatory for Gig Economy Activity
FastAPI Backend Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.api import router as api_router

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ATHAR API",
    description=(
        "Digital Observatory for Gig Economy Activity in Saudi Arabia.\n\n"
        "Estimates platform-economy activity using hybrid digital signals: "
        "search trends, app ecosystem, food delivery, and freelance platforms."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(api_router)


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "system": "ATHAR",
        "description": "Digital Observatory for Gig Economy Activity",
        "version": "1.0.0",
        "demo_mode": os.getenv("DEMO_MODE", "true").lower() == "true",
        "docs": "/docs",
    }
