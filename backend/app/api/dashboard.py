from fastapi import APIRouter, Query
from typing import Optional
from app.services.demo_service import get_dashboard_data

router = APIRouter()

@router.get("/dashboard-data")
def dashboard_data(
    period: Optional[str] = Query(
        default="90",
        description="Time period in days: 30 | 90 | 180 | 365",
    ),
    region: Optional[str] = Query(
        default=None,
        description="Filter by region: Riyadh | Jeddah | Dammam | Makkah | Madinah",
    ),
):
    days = int(period) if period and period.isdigit() else 90
    return get_dashboard_data(days=days, region=region or None)
