"""
Pydantic models, constants, and configuration for ATHAR.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

# ── Constants ─────────────────────────────────────────────────────────────────

REGIONS: List[str] = ["Riyadh", "Jeddah", "Dammam", "Makkah", "Madinah"]

SECTORS: List[str] = [
    "Ride-hailing",
    "Food Delivery",
    "Freelance Digital Work",
    "Gig Services",
]

SOURCES: List[str] = [
    "Google Trends",
    "App Ecosystem",
    "Food Delivery",
    "Freelance Platforms",
    "Benchmark Dataset",
]

# Geographic coordinates for Saudi cities
REGION_COORDS: dict = {
    "Riyadh":  {"lat": 24.7136, "lng": 46.6753},
    "Jeddah":  {"lat": 21.4858, "lng": 39.1925},
    "Dammam":  {"lat": 26.4207, "lng": 50.0888},
    "Makkah":  {"lat": 21.3891, "lng": 39.8579},
    "Madinah": {"lat": 24.5247, "lng": 39.5692},
}

# Composite index weights (must sum to 1.0)
SOURCE_WEIGHTS: dict = {
    "Google Trends":       0.25,
    "App Ecosystem":       0.20,
    "Food Delivery":       0.20,
    "Freelance Platforms": 0.20,
    "Benchmark Dataset":   0.15,
}

# Pipeline score column → source key mapping
SCORE_SOURCE_MAP: dict = {
    "search_score":    "Google Trends",
    "app_score":       "App Ecosystem",
    "food_score":      "Food Delivery",
    "freelance_score": "Freelance Platforms",
}

# ── Enums ─────────────────────────────────────────────────────────────────────

class SourceType(str, Enum):
    real      = "real"
    estimated = "estimated"
    synthetic = "synthetic"

class TimePeriod(str, Enum):
    days_30  = "30"
    days_90  = "90"
    days_180 = "180"
    days_365 = "365"

# ── Raw Record Schemas ────────────────────────────────────────────────────────

class SearchTrendRecord(BaseModel):
    date:              str
    region:            str
    keyword:           str
    interest:          float = Field(ge=0, le=100)
    source_name:       str = "Google Trends"
    source_type:       SourceType = SourceType.real
    reliability_score: float = Field(default=0.9, ge=0, le=1)


class AppEcosystemRecord(BaseModel):
    date:              str
    app_name:          str
    region:            str
    rating:            float = Field(ge=0, le=5)
    review_count:      int   = Field(ge=0)
    installs:          str   = "Unknown"
    source_name:       str = "App Ecosystem"
    source_type:       SourceType = SourceType.estimated
    reliability_score: float = Field(default=0.75, ge=0, le=1)


class FreelanceRecord(BaseModel):
    date:              str
    platform:          str
    region:            str
    listings_count:    int  = Field(ge=0)
    category:          str
    source_name:       str = "Freelance Platforms"
    source_type:       SourceType = SourceType.estimated
    reliability_score: float = Field(default=0.70, ge=0, le=1)


class FoodDeliveryRecord(BaseModel):
    date:              str
    platform:          str
    region:            str
    activity_index:    float = Field(ge=0, le=100)
    source_name:       str = "Food Delivery"
    source_type:       SourceType = SourceType.estimated
    reliability_score: float = Field(default=0.75, ge=0, le=1)

# ── Dashboard Response Schemas ────────────────────────────────────────────────

class KPIMetrics(BaseModel):
    gig_activity_index: float
    growth_rate:        float
    data_reliability:   float
    active_signals:     int


class SourceContribution(BaseModel):
    source:            str
    weight:            int           # percentage, e.g. 25
    value:             float
    source_type:       str
    reliability_score: float


class RegionalComparison(BaseModel):
    region: str
    index:  float
    growth: float


class MapPoint(BaseModel):
    region: str
    lat:    float
    lng:    float
    index:  float
    growth: float


class DataQuality(BaseModel):
    overall_reliability:   float
    real_percentage:       int
    estimated_percentage:  int
    synthetic_percentage:  int
    active_signals:        int
    total_records:         int


class DashboardMeta(BaseModel):
    period_days:    int
    region_filter:  Optional[str]
    demo_mode:      bool
    generated_at:   str


class DashboardResponse(BaseModel):
    kpis:                 KPIMetrics
    time_series:          List[dict]
    source_contributions: List[SourceContribution]
    regional_comparison:  List[RegionalComparison]
    map_data:             List[MapPoint]
    data_quality:         DataQuality
    meta:                 DashboardMeta
