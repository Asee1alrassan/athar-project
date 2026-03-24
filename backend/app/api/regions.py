from fastapi import APIRouter
from app.schemas.models import REGIONS, REGION_COORDS

router = APIRouter()

@router.get("/regions")
def get_regions():
    return {
        "regions": REGIONS,
        "coordinates": REGION_COORDS,
    }
