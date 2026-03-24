from fastapi import APIRouter
from app.services.index_calculator import calculate_gig_index

router = APIRouter()

@router.post("/calculate-index")
def calculate_index():
    result = calculate_gig_index()
    return {
        "status":           "success",
        "index_calculated": True,
        "summary":          result,
    }
