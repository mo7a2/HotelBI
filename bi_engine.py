from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ["CheckInDate", "CheckOutDate", "RateAmount", "BookingStatus"]
OPTIONAL_COLUMNS = ["RoomType", "RoomNumber", "Channel", "GuestName", "GuestCountry", "RepeatGuest"]

STATUS_MAP = {
    "confirmed": "Confirmed", "complete": "Completed", "completed": "Completed",
    "checked in": "Checked In", "checked-in": "Checked In", "checkedin": "Checked In",
    "cancelled": "Cancelled", "canceled": "Cancelled", "no show": "No Show", "noshow": "No Show",
}

CHANNEL_MAP = {
    "booking": "Booking.com", "booking.com": "Booking.com", "expedia": "Expedia",
    "direct": "Direct", "website": "Direct", "walk in": "Walk-in", "walk-in": "Walk-in",
    "agoda": "Agoda", "airbnb": "Airbnb",
}

@dataclass
class CleaningResult:
    clean: pd.DataFrame
    summary: dict[str, Any]
    issues: dict[str, int]


def _norm_name(name: str) -> str:
    return "".join(ch.lower() for ch in str(name).strip() if ch.isalnum())


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    aliases = {_norm_name(c): c for c in REQUIRED_COLUMNS + OPTIONAL_COLUMNS}
    rename = {}
    for col in df.columns:
        key = _norm_name(col)
        if key in aliases:
            rename[col] = aliases[key]
    return df.rename(columns=rename)


def parse_csv_bytes(raw: bytes, filename: str = "upload.csv") -> CleaningResult:
    text = raw.decode("utf-8-sig", errors="replace")
    df = pd.read_csv(io.StringIO(text))
    return clean_bookings(df, filename)


def clean_bookings(df: pd.DataFrame, filename: str = "upload.csv") -> CleaningResult:
    df = _rename_columns(df.copy())
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    received = len(df)
    duplicate_mask = df.duplicated(keep="first")
    duplicates_removed = int(duplicate_mask.sum())
    df = df.loc[~duplicate_mask].copy()

    issues = {
        "missing_required": 0,
        "invalid_dates": 0,
        "invalid_rate": 0,
        "invalid_stay": 0,
        "duplicates_removed": duplicates_removed,
    }

    for col in OPTIONAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    raw_required_missing = df[REQUIRED_COLUMNS].isna().any(axis=1)
    issues["missing_required"] = int(raw_required_missing.sum())

    df["CheckInDate"] = pd.to_datetime(df["CheckInDate"], errors="coerce")
    df["CheckOutDate"] = pd.to_datetime(df["CheckOutDate"], errors="coerce")
    df["RateAmount"] = pd.to_numeric(df["RateAmount"], errors="coerce")

    invalid_dates = df["CheckInDate"].isna() | df["CheckOutDate"].isna()
    invalid_rate = df["RateAmount"].isna() | (df["RateAmount"] < 0)
    invalid_stay = (~invalid_dates) & (df["CheckOutDate"] <= df["CheckInDate"])

    issues["invalid_dates"] = int(invalid_dates.sum())
    issues["invalid_rate"] = int(invalid_rate.sum())
    issues["invalid_stay"] = int(invalid_stay.sum())

    valid = ~(raw_required_missing | invalid_dates | invalid_rate | invalid_stay)
    clean = df.loc[valid].copy()

    clean["BookingStatus"] = clean["BookingStatus"].astype(str).str.strip().map(
        lambda x: STATUS_MAP.get(x.lower(), x.title())
    )
    clean["Channel"] = clean["Channel"].fillna("").astype(str).str.strip().map(
        lambda x: CHANNEL_MAP.get(x.lower(), x.title() if x else "Unknown")
    )
    clean["RoomType"] = clean["RoomType"].fillna("").replace("", "Standard")
    clean["GuestCountry"] = clean["GuestCountry"].fillna("").replace("", "Unknown")
    clean["RepeatGuest"] = clean["RepeatGuest"].fillna("").astype(str).str.strip().str.lower().isin(
        ["1", "true", "yes", "y", "repeat", "returning"]
    )
    clean["Nights"] = (clean["CheckOutDate"] - clean["CheckInDate"]).dt.days
    clean["StayRevenue"] = (clean["RateAmount"] * clean["Nights"]).round(2)

    rejected = received - duplicates_removed - len(clean)
    summary = {
        "filename": filename,
        "rows_received": int(received),
        "rows_clean": int(len(clean)),
        "rows_rejected": int(max(rejected, 0)),
        "duplicates_removed": duplicates_removed,
        "data_health_score": data_health_score(received, len(clean), duplicates_removed),
    }
    return CleaningResult(clean=clean, summary=summary, issues=issues)


def data_health_score(received: int, clean_count: int, duplicates: int) -> int:
    if received <= 0:
        return 0
    usable = clean_count / received
    duplicate_penalty = min(duplicates / received, 0.25)
    return max(0, min(100, round((usable - duplicate_penalty * 0.25) * 100)))


def active_bookings(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    return df.loc[~df["BookingStatus"].str.lower().isin(["cancelled", "canceled", "no show"])].copy()


def daily_metrics(df: pd.DataFrame, total_rooms: int = 550, days: int = 30, end_date: date | None = None) -> list[dict[str, Any]]:
    total_rooms = max(int(total_rooms or 1), 1)
    if end_date is None:
        if len(df):
            end_date = max(df["CheckOutDate"].max().date(), df["CheckInDate"].max().date())
        else:
            end_date = date.today()
    start_date = end_date - timedelta(days=max(days, 1) - 1)
    valid = active_bookings(df)
    out = []
    for offset in range(days):
        d = start_date + timedelta(days=offset)
        ts = pd.Timestamp(d)
        occupied = valid[(valid["CheckInDate"] <= ts) & (valid["CheckOutDate"] > ts)]
        rooms_sold = int(len(occupied))
        revenue = float(occupied["RateAmount"].sum()) if rooms_sold else 0.0
        occupancy = rooms_sold / total_rooms * 100
        adr = revenue / rooms_sold if rooms_sold else 0.0
        revpar = revenue / total_rooms
        out.append({
            "date": d.isoformat(), "label": d.strftime("%b %d"), "rooms_sold": rooms_sold,
            "occupancy": round(occupancy, 2), "adr": round(adr, 2), "revpar": round(revpar, 2),
            "revenue": round(revenue, 2),
        })
    return out


def dashboard_summary(daily: list[dict[str, Any]]) -> dict[str, float]:
    if not daily:
        return {"average_occupancy": 0, "average_adr": 0, "average_revpar": 0, "total_revenue": 0}
    return {
        "average_occupancy": round(float(np.mean([x["occupancy"] for x in daily])), 2),
        "average_adr": round(float(np.mean([x["adr"] for x in daily])), 2),
        "average_revpar": round(float(np.mean([x["revpar"] for x in daily])), 2),
        "total_revenue": round(float(np.sum([x["revenue"] for x in daily])), 2),
    }


def guest_insights(df: pd.DataFrame) -> dict[str, Any]:
    total = int(len(df))
    if not total:
        return {"total_bookings": 0, "repeat_rate": 0, "cancellation_rate": 0, "average_stay": 0, "channels": [], "countries": [], "room_types": []}
    cancelled = df["BookingStatus"].str.lower().isin(["cancelled", "canceled", "no show"])
    channels = df["Channel"].value_counts().head(10)
    countries = df["GuestCountry"].value_counts().head(10)
    room_types = df["RoomType"].value_counts().head(10)
    return {
        "total_bookings": total,
        "repeat_rate": round(float(df["RepeatGuest"].mean() * 100), 2),
        "cancellation_rate": round(float(cancelled.mean() * 100), 2),
        "average_stay": round(float(df["Nights"].mean()), 2),
        "channels": [{"name": str(k), "count": int(v)} for k, v in channels.items()],
        "countries": [{"name": str(k), "count": int(v)} for k, v in countries.items()],
        "room_types": [{"name": str(k), "count": int(v)} for k, v in room_types.items()],
    }


def forecast_from_daily(daily: list[dict[str, Any]], horizon: int = 10) -> list[dict[str, Any]]:
    if not daily:
        return []
    y = np.array([float(x["occupancy"]) for x in daily], dtype=float)
    x = np.arange(len(y), dtype=float)
    if len(y) >= 2:
        slope, intercept = np.polyfit(x, y, 1)
        fitted = intercept + slope * x
        sigma = float(np.std(y - fitted))
    else:
        slope, intercept, sigma = 0.0, y[0], 0.0
    last_date = datetime.fromisoformat(daily[-1]["date"]).date()
    result = []
    for i in range(1, horizon + 1):
        pred = float(intercept + slope * (len(y) - 1 + i))
        pred = max(0.0, min(100.0, pred))
        lower = max(0.0, pred - 1.96 * sigma)
        upper = min(100.0, pred + 1.96 * sigma)
        d = last_date + timedelta(days=i)
        result.append({"date": d.isoformat(), "label": d.strftime("%b %d"), "occupancy": round(pred, 2), "lower": round(lower, 2), "upper": round(upper, 2)})
    return result


def build_alerts(summary: dict[str, float], guests: dict[str, Any], thresholds: dict[str, float] | None = None) -> list[dict[str, Any]]:
    t = {"low_occupancy": 45.0, "high_cancellation": 18.0, "low_revpar": 45.0}
    if thresholds:
        t.update({k: float(v) for k, v in thresholds.items() if k in t})
    alerts = []
    if summary.get("average_occupancy", 0) < t["low_occupancy"]:
        alerts.append({"type": "Low Occupancy", "severity": "warning", "message": f"Average occupancy is {summary.get('average_occupancy', 0):.1f}%, below the {t['low_occupancy']:.0f}% threshold."})
    if guests.get("cancellation_rate", 0) > t["high_cancellation"]:
        alerts.append({"type": "Cancellation Spike", "severity": "danger", "message": f"Cancellation rate is {guests.get('cancellation_rate', 0):.1f}%, above the {t['high_cancellation']:.0f}% threshold."})
    if summary.get("average_revpar", 0) < t["low_revpar"]:
        alerts.append({"type": "Low RevPAR", "severity": "info", "message": f"Average RevPAR is ${summary.get('average_revpar', 0):.2f}, below the ${t['low_revpar']:.0f} threshold."})
    return alerts


def serializable_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []
    out = df.copy()
    for c in ["CheckInDate", "CheckOutDate"]:
        out[c] = out[c].dt.strftime("%Y-%m-%d")
    out["RepeatGuest"] = out["RepeatGuest"].astype(bool)
    return out.replace({np.nan: None}).to_dict(orient="records")
