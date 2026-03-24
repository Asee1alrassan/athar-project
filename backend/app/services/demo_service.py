"""
Demo Service — generates stable mock data for hackathon demo mode.
All randomness is seeded so responses are consistent across requests.
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from app.schemas.models import REGIONS, REGION_COORDS

# ── Seed for stable reproducibility ──────────────────────────────────────────
_RNG = random.Random(42)

# Base activity indices per region (Riyadh highest, Madinah lowest)
REGION_BASE: Dict[str, float] = {
    "Riyadh":  78.0,
    "Jeddah":  71.0,
    "Dammam":  64.0,
    "Makkah":  58.0,
    "Madinah": 53.0,
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _date_range(days: int) -> List[str]:
    """Return list of ISO date strings from (today - days) to today."""
    end   = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=days - 1)
    result, current = [], start
    while current <= end:
        result.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    return result


def _trend(base: float, idx: int, total: int, growth: float = 0.06) -> float:
    """Value that slowly trends upward with Gaussian noise."""
    progress = idx / max(total - 1, 1)
    val = base * (1 + growth * progress) + _RNG.gauss(0, 4.5)
    return round(max(0.0, min(100.0, val)), 2)


# ── Raw data loader ───────────────────────────────────────────────────────────

def load_demo_data() -> Dict[str, List[dict]]:
    """Load raw JSON datasets from the data/raw directory."""
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    result: Dict[str, List[dict]] = {}
    for fname in ("search_trends.json", "app_ecosystem.json",
                  "freelance.json", "food_delivery.json"):
        fpath = os.path.join(raw_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                key = fname.replace(".json", "")
                result[key] = json.load(f)
    return result


# ── Time-series generator ─────────────────────────────────────────────────────

def _build_time_series(
    days: int, region: Optional[str]
) -> List[Dict[str, Any]]:
    """Build a list of {date, Region1, Region2, ...} objects."""
    rng = random.Random(42)          # local seed for determinism
    dates = _date_range(days)
    regions = [region] if region else REGIONS

    # Pre-generate per-region value sequences
    series: Dict[str, List[float]] = {}
    for reg in regions:
        base = REGION_BASE[reg]
        vals: List[float] = []
        for i in range(len(dates)):
            progress = i / max(len(dates) - 1, 1)
            v = base * (1 + 0.06 * progress) + rng.gauss(0, 4.5)
            vals.append(round(max(0.0, min(100.0, v)), 2))
        series[reg] = vals

    # Merge into single list
    merged: List[Dict[str, Any]] = []
    for i, d in enumerate(dates):
        point: Dict[str, Any] = {"date": d}
        for reg in regions:
            point[reg] = series[reg][i]
        merged.append(point)
    return merged


# ── Main dashboard builder ────────────────────────────────────────────────────

def get_dashboard_data(
    days: int = 90, region: Optional[str] = None
) -> Dict[str, Any]:
    """Return the complete dashboard payload."""

    rng = random.Random(42)

    time_series = _build_time_series(days, region)

    focus = region or "Riyadh"
    vals  = [p[focus] for p in time_series]
    current_idx  = round(vals[-1], 1)
    prev_idx     = round(vals[max(0, len(vals) - 31)], 1)
    growth_rate  = round((current_idx - prev_idx) / max(prev_idx, 1) * 100, 2)

    # Source contributions
    source_contributions = [
        {
            "source":            "Google Trends",
            "weight":            25,
            "value":             round(74 + rng.gauss(0, 3), 1),
            "source_type":       "real",
            "reliability_score": 0.90,
        },
        {
            "source":            "App Ecosystem",
            "weight":            20,
            "value":             round(68 + rng.gauss(0, 3), 1),
            "source_type":       "estimated",
            "reliability_score": 0.75,
        },
        {
            "source":            "Food Delivery",
            "weight":            20,
            "value":             round(71 + rng.gauss(0, 3), 1),
            "source_type":       "estimated",
            "reliability_score": 0.75,
        },
        {
            "source":            "Freelance Platforms",
            "weight":            20,
            "value":             round(65 + rng.gauss(0, 3), 1),
            "source_type":       "estimated",
            "reliability_score": 0.70,
        },
        {
            "source":            "Benchmark Dataset",
            "weight":            15,
            "value":             round(60 + rng.gauss(0, 3), 1),
            "source_type":       "synthetic",
            "reliability_score": 0.60,
        },
    ]

    # Regional comparison (average over the period)
    regional_comparison = []
    for reg in REGIONS:
        reg_vals = [p[reg] for p in time_series if reg in p]
        avg = round(sum(reg_vals) / len(reg_vals), 1) if reg_vals else REGION_BASE[reg]
        regional_comparison.append({
            "region": reg,
            "index":  avg,
            "growth": round(rng.uniform(2.0, 8.5), 2),
        })

    # Map data
    map_data = []
    for item in regional_comparison:
        reg = item["region"]
        map_data.append({
            "region": reg,
            "lat":    REGION_COORDS[reg]["lat"],
            "lng":    REGION_COORDS[reg]["lng"],
            "index":  item["index"],
            "growth": item["growth"],
        })

    # Data quality metrics
    data_quality = {
        "overall_reliability":  0.77,
        "real_percentage":      25,
        "estimated_percentage": 55,
        "synthetic_percentage": 20,
        "active_signals":       42,
        "total_records":        max(1250, 1250 * (days // 30)),
    }

    return {
        "kpis": {
            "gig_activity_index": current_idx,
            "growth_rate":        growth_rate,
            "data_reliability":   round(data_quality["overall_reliability"] * 100, 1),
            "active_signals":     data_quality["active_signals"],
        },
        "time_series":          time_series,
        "source_contributions": source_contributions,
        "regional_comparison":  regional_comparison,
        "map_data":             map_data,
        "data_quality":         data_quality,
        "meta": {
            "period_days":   days,
            "region_filter": region,
            "demo_mode":     True,
            "generated_at":  datetime.now().isoformat(),
        },
    }
