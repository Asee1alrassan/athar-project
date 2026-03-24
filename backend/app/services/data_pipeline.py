"""
ATHAR Data Pipeline
Steps:
  1. Load raw JSON datasets
  2. Validate schema (add missing columns)
  3. Remove duplicates
  4. Normalize region names
  5. Convert dates to ISO format
  6. Handle missing values (median fill)
  7. Detect & remove outliers using IQR
  8. Normalize metrics to 0-100 scale
  9. Merge datasets by region and date
 10. Save processed analytics table
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Optional

from app.schemas.models import REGIONS

# ── Paths ─────────────────────────────────────────────────────────────────────
_BASE      = os.path.dirname(__file__)
RAW_DIR    = os.path.join(_BASE, "..", "data", "raw")
PROC_DIR   = os.path.join(_BASE, "..", "data", "processed")

# ── Region alias map (handles Arabic + case variants) ─────────────────────────
REGION_ALIASES: dict = {
    "riyadh":      "Riyadh",
    "الرياض":      "Riyadh",
    "jeddah":      "Jeddah",
    "jedda":       "Jeddah",
    "جدة":         "Jeddah",
    "dammam":      "Dammam",
    "الدمام":      "Dammam",
    "makkah":      "Makkah",
    "mecca":       "Makkah",
    "مكة":         "Makkah",
    "madinah":     "Madinah",
    "medina":      "Madinah",
    "المدينة":     "Madinah",
}

# ── Internal helpers ──────────────────────────────────────────────────────────

def _load_json(filename: str) -> list:
    fpath = os.path.join(RAW_DIR, filename)
    if not os.path.exists(fpath):
        return []
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f)


def _ensure_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """Step 2 — Add any missing required columns as NaN."""
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
    return df


def _normalize_regions(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4 — Standardise region names; drop unrecognised rows."""
    if "region" not in df.columns:
        return df
    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
        .map(lambda x: REGION_ALIASES.get(x.lower(), x))
    )
    return df[df["region"].isin(REGIONS)].copy()


def _normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Step 5 — Convert date column to ISO 8601 YYYY-MM-DD strings."""
    if "date" not in df.columns:
        return df
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df.dropna(subset=["date"]).copy()


def _fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Step 6 — Fill numeric NaNs with per-column median."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    return df


def _remove_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Step 7 — Drop rows where col falls outside 1.5 × IQR fence."""
    if col not in df.columns or df[col].isna().all():
        return df
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr     = q3 - q1
    return df[(df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)].copy()


def _normalize_0_100(series: pd.Series) -> pd.Series:
    """Step 8 — Min-max normalise a series to [0, 100]."""
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series(50.0, index=series.index)
    return (series - mn) / (mx - mn) * 100.0


# ── Source-specific processors ────────────────────────────────────────────────

def _process_search(raw: list) -> Optional[pd.DataFrame]:
    if not raw:
        return None
    df = pd.DataFrame(raw)
    df = _ensure_columns(df, ["date", "region", "keyword", "interest"])
    df = df.drop_duplicates()
    df = _normalize_regions(df)
    df = _normalize_dates(df)
    df = _fill_missing(df)
    df = _remove_outliers_iqr(df, "interest")
    df["interest_norm"] = _normalize_0_100(df["interest"])
    agg = df.groupby(["date", "region"])["interest_norm"].mean().reset_index()
    agg.rename(columns={"interest_norm": "search_score"}, inplace=True)
    return agg


def _process_app(raw: list) -> Optional[pd.DataFrame]:
    if not raw:
        return None
    df = pd.DataFrame(raw)
    df = _ensure_columns(df, ["date", "region", "app_name", "rating", "review_count"])
    df = df.drop_duplicates()
    df = _normalize_regions(df)
    df = _normalize_dates(df)
    df = _fill_missing(df)
    # Composite app signal: rating × log(review_count + 1)
    df["_raw_app"] = df["rating"] * np.log1p(df["review_count"])
    df["app_score"] = _normalize_0_100(df["_raw_app"])
    agg = df.groupby(["date", "region"])["app_score"].mean().reset_index()
    return agg


def _process_freelance(raw: list) -> Optional[pd.DataFrame]:
    if not raw:
        return None
    df = pd.DataFrame(raw)
    df = _ensure_columns(df, ["date", "region", "platform", "listings_count"])
    df = df.drop_duplicates()
    df = _normalize_regions(df)
    df = _normalize_dates(df)
    df = _fill_missing(df)
    df = _remove_outliers_iqr(df, "listings_count")
    df["freelance_score"] = _normalize_0_100(df["listings_count"])
    agg = df.groupby(["date", "region"])["freelance_score"].mean().reset_index()
    return agg


def _process_food(raw: list) -> Optional[pd.DataFrame]:
    if not raw:
        return None
    df = pd.DataFrame(raw)
    df = _ensure_columns(df, ["date", "region", "platform", "activity_index"])
    df = df.drop_duplicates()
    df = _normalize_regions(df)
    df = _normalize_dates(df)
    df = _fill_missing(df)
    df["food_score"] = _normalize_0_100(df["activity_index"])
    agg = df.groupby(["date", "region"])["food_score"].mean().reset_index()
    return agg


# ── Public pipeline entry point ───────────────────────────────────────────────

def run_pipeline() -> pd.DataFrame:
    """
    Execute the full 10-step pipeline and return the merged analytics DataFrame.
    Also persists the result to data/processed/analytics_table.csv.
    """

    # ── Step 1: Load ─────────────────────────────────────────────────────────
    search_raw   = _load_json("search_trends.json")
    app_raw      = _load_json("app_ecosystem.json")
    freelance_raw= _load_json("freelance.json")
    food_raw     = _load_json("food_delivery.json")

    # ── Steps 2-8: Source-specific processing ────────────────────────────────
    frames = {
        "search":    _process_search(search_raw),
        "app":       _process_app(app_raw),
        "freelance": _process_freelance(freelance_raw),
        "food":      _process_food(food_raw),
    }
    frames = {k: v for k, v in frames.items() if v is not None}

    if not frames:
        return pd.DataFrame(columns=["date", "region"])

    # ── Step 9: Merge on date × region ───────────────────────────────────────
    merged: pd.DataFrame = None  # type: ignore
    for df in frames.values():
        if merged is None:
            merged = df
        else:
            merged = pd.merge(merged, df, on=["date", "region"], how="outer")

    merged = merged.sort_values(["region", "date"]).reset_index(drop=True)

    # ── Step 10: Persist ─────────────────────────────────────────────────────
    os.makedirs(PROC_DIR, exist_ok=True)
    out_path = os.path.join(PROC_DIR, "analytics_table.csv")
    merged.to_csv(out_path, index=False, encoding="utf-8")

    return merged
