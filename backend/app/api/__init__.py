from fastapi import APIRouter
from app.api import health, regions, sectors, sources, ingest, process, calculate_index, dashboard

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(regions.router, tags=["Regions"])
router.include_router(sectors.router, tags=["Sectors"])
router.include_router(sources.router, tags=["Sources"])
router.include_router(ingest.router, tags=["Ingest"])
router.include_router(process.router, tags=["Process"])
router.include_router(calculate_index.router, tags=["Index"])
router.include_router(dashboard.router, tags=["Dashboard"])
