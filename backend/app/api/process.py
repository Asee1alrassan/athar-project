from fastapi import APIRouter
from app.services.data_pipeline import run_pipeline

router = APIRouter()

@router.post("/process")
def process_data():
    result = run_pipeline()
    if result.empty:
        return {"status": "warning", "message": "No data to process — check raw data files."}
    return {
        "status":           "success",
        "processed_records": len(result),
        "columns":          list(result.columns),
        "regions":          sorted(result["region"].unique().tolist()),
        "message":          "Pipeline completed successfully",
    }
