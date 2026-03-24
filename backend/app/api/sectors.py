from fastapi import APIRouter
from app.schemas.models import SECTORS

router = APIRouter()

@router.get("/sectors")
def get_sectors():
    return {"sectors": SECTORS}
