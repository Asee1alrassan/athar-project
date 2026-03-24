from fastapi import APIRouter
from app.schemas.models import SOURCES, SOURCE_WEIGHTS

router = APIRouter()

@router.get("/sources")
def get_sources():
    return {
        "sources": SOURCES,
        "weights": SOURCE_WEIGHTS,
    }
