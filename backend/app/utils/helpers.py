import re
from datetime import datetime


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def iso_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))
