import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    demo = os.getenv("DEMO_MODE", "true").lower() == "true"
    return {
        "status":    "healthy",
        "demo_mode": demo,
        "version":   "1.0.0",
        "system":    "ATHAR",
    }
