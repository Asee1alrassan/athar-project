from fastapi import APIRouter
from app.services.demo_service import load_demo_data

router = APIRouter()

@router.post("/ingest")
def ingest_data():
    data = load_demo_data()
    return {
        "status":         "success",
        "records_loaded": {k: len(v) for k, v in data.items()},
        "message":        "Data ingested from demo cache (DEMO_MODE=true)",
    }
