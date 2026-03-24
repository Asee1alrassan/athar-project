"""
Gig Activity Index Calculator
Range: 0 – 100
Weights:
  search_score    → Google Trends      25 %
  app_score       → App Ecosystem      20 %
  food_score      → Food Delivery      20 %
  freelance_score → Freelance Platforms 20 %
  (Benchmark 15 % is implicit in the normalisation baseline)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

from app.schemas.models import SOURCE_WEIGHTS, SCORE_SOURCE_MAP
from app.services.data_pipeline import run_pipeline

# Map pipeline column names → source weight keys
_COL_WEIGHT: Dict[str, float] = {
    "search_score":    SOURCE_WEIGHTS["Google Trends"],
    "app_score":       SOURCE_WEIGHTS["App Ecosystem"],
    "food_score":      SOURCE_WEIGHTS["Food Delivery"],
    "freelance_score": SOURCE_WEIGHTS["Freelance Platforms"],
}


def _weighted_index(row: pd.Series, cols: list, total_w: float) -> float:
    """Compute weighted average for available (non-NaN) columns."""
    val = sum(
        row[c] * _COL_WEIGHT[c]
        for c in cols
        if not pd.isna(row.get(c))
    )
    return round(val / total_w, 2) if total_w > 0 else 0.0


def calculate_gig_index() -> Dict[str, Any]:
    """
    Run the pipeline, calculate Gig Activity Index per row, and return
    a summary dict with overall stats and per-region averages.
    """
    df = run_pipeline()
    if df.empty:
        return {"error": "No processed data available. Run /process first."}

    # Only use columns that actually exist in the merged frame
    available_cols = [c for c in _COL_WEIGHT if c in df.columns]
    total_weight   = sum(_COL_WEIGHT[c] for c in available_cols)

    df["gig_activity_index"] = df.apply(
        lambda row: _weighted_index(row, available_cols, total_weight),
        axis=1,
    )

    # ── Summary ───────────────────────────────────────────────────────────────
    by_region = (
        df.groupby("region")["gig_activity_index"]
        .mean()
        .round(2)
        .to_dict()
    )

    return {
        "overall_mean":  round(float(df["gig_activity_index"].mean()), 2),
        "overall_max":   round(float(df["gig_activity_index"].max()), 2),
        "overall_min":   round(float(df["gig_activity_index"].min()), 2),
        "by_region":     by_region,
        "weights_used":  {SCORE_SOURCE_MAP[c]: _COL_WEIGHT[c] for c in available_cols},
        "records_scored": len(df),
    }
