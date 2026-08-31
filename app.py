from __future__ import annotations

import io
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "hotelbi.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "change-this-in-production")
CORS(app, supports_credentials=True)

DEMO_USERS = {
    "manager": {"email": "manager@hotel.com", "password": "managermanager", "role": "manager"},
    "admin": {"email": "admin@admin.com", "password": "adminadmin", "role": "admin"},
}

REQUIRED_COLUMNS = {
    "date", "room_type", "rooms_available", "rooms_sold", "room_revenue"
}


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    with db() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                uploaded_at TEXT NOT NULL,
                rows_received INTEGER NOT NULL,
                rows_clean INTEGER NOT NULL,
                rows_rejected INTEGER NOT NULL,
                duplicates_removed INTEGER NOT NULL,
                status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS profiles (
                role TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )


init_db()


@app.get("/")
def index():
    # This is the original uploaded production React bundle, served unchanged.
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "HotelBI Flask API"})


@app.post("/api/login")
def login():
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))
    requested_role = str(payload.get("role", "")).strip().lower()

    candidates = [DEMO_USERS[requested_role]] if requested_role in DEMO_USERS else DEMO_USERS.values()
    for user in candidates:
        if email == user["email"] and password == user["password"]:
            session["role"] = user["role"]
            return jsonify({"ok": True, "role": user["role"], "email": user["email"]})
    return jsonify({"ok": False, "error": "Wrong email or password."}), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("-", "_")
        for c in df.columns
    ]
    return df


def process_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    received = len(df)
    df = normalize_columns(df)

    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    before_dupes = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = before_dupes - len(df)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for col in ["rooms_available", "rooms_sold", "room_revenue"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    valid = (
        df["date"].notna()
        & df["room_type"].notna()
        & (df["rooms_available"] > 0)
        & (df["rooms_sold"] >= 0)
        & (df["rooms_sold"] <= df["rooms_available"])
        & (df["room_revenue"] >= 0)
    )
    clean = df.loc[valid].copy()
    rejected = len(df) - len(clean)

    clean["occupancy"] = (clean["rooms_sold"] / clean["rooms_available"] * 100).round(2)
    clean["adr"] = (clean["room_revenue"] / clean["rooms_sold"].replace(0, pd.NA)).fillna(0).round(2)
    clean["revpar"] = (clean["room_revenue"] / clean["rooms_available"]).round(2)

    summary = {
        "rows_received": int(received),
        "rows_clean": int(len(clean)),
        "rows_rejected": int(rejected),
        "duplicates_removed": int(duplicates_removed),
        "average_occupancy": round(float(clean["occupancy"].mean()), 2) if len(clean) else 0,
        "average_adr": round(float(clean["adr"].mean()), 2) if len(clean) else 0,
        "average_revpar": round(float(clean["revpar"].mean()), 2) if len(clean) else 0,
    }
    return clean, summary


@app.post("/api/process-csv")
def process_csv():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "CSV file is required."}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"ok": False, "error": "CSV file is required."}), 400

    try:
        raw = file.read()
        df = pd.read_csv(io.BytesIO(raw))
        clean, summary = process_dataframe(df)
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400

    now = datetime.now(timezone.utc).isoformat()
    with db() as con:
        con.execute(
            """INSERT INTO uploads
               (filename, uploaded_at, rows_received, rows_clean, rows_rejected, duplicates_removed, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                file.filename,
                now,
                summary["rows_received"],
                summary["rows_clean"],
                summary["rows_rejected"],
                summary["duplicates_removed"],
                "Processed" if summary["rows_clean"] else "No valid rows",
            ),
        )

    daily = (
        clean.groupby(clean["date"].dt.date, as_index=False)
        .agg(rooms_available=("rooms_available", "sum"), rooms_sold=("rooms_sold", "sum"), room_revenue=("room_revenue", "sum"))
    ) if len(clean) else pd.DataFrame(columns=["date", "rooms_available", "rooms_sold", "room_revenue"])

    if len(daily):
        daily["occupancy"] = (daily["rooms_sold"] / daily["rooms_available"] * 100).round(2)
        daily["adr"] = (daily["room_revenue"] / daily["rooms_sold"].replace(0, pd.NA)).fillna(0).round(2)
        daily["revpar"] = (daily["room_revenue"] / daily["rooms_available"]).round(2)
        daily["date"] = daily["date"].astype(str)

    return jsonify({
        "ok": True,
        "filename": file.filename,
        "summary": summary,
        "daily": daily.to_dict(orient="records"),
        "rows": clean.fillna("").astype(object).where(pd.notnull(clean), None).to_dict(orient="records"),
    })


@app.get("/api/uploads")
def uploads():
    with db() as con:
        rows = con.execute("SELECT * FROM uploads ORDER BY id DESC LIMIT 100").fetchall()
    return jsonify({"ok": True, "uploads": [dict(r) for r in rows]})


@app.route("/api/profile/<role>", methods=["GET", "PUT"])
def profile(role: str):
    if role not in {"manager", "admin"}:
        return jsonify({"ok": False, "error": "Invalid role."}), 404

    if request.method == "GET":
        with db() as con:
            row = con.execute("SELECT payload, updated_at FROM profiles WHERE role = ?", (role,)).fetchone()
        if not row:
            return jsonify({"ok": True, "profile": {}, "updated_at": None})
        return jsonify({"ok": True, "profile": json.loads(row["payload"]), "updated_at": row["updated_at"]})

    payload = request.get_json(silent=True) or {}
    now = datetime.now(timezone.utc).isoformat()
    with db() as con:
        con.execute(
            """INSERT INTO profiles(role, payload, updated_at) VALUES (?, ?, ?)
               ON CONFLICT(role) DO UPDATE SET payload=excluded.payload, updated_at=excluded.updated_at""",
            (role, json.dumps(payload), now),
        )
    return jsonify({"ok": True, "profile": payload, "updated_at": now})


@app.route("/api/settings/<key>", methods=["GET", "PUT"])
def settings(key: str):
    if request.method == "GET":
        with db() as con:
            row = con.execute("SELECT payload, updated_at FROM settings WHERE key = ?", (key,)).fetchone()
        if not row:
            return jsonify({"ok": True, "value": None, "updated_at": None})
        return jsonify({"ok": True, "value": json.loads(row["payload"]), "updated_at": row["updated_at"]})

    payload = request.get_json(silent=True)
    now = datetime.now(timezone.utc).isoformat()
    with db() as con:
        con.execute(
            """INSERT INTO settings(key, payload, updated_at) VALUES (?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET payload=excluded.payload, updated_at=excluded.updated_at""",
            (key, json.dumps(payload), now),
        )
    return jsonify({"ok": True, "value": payload, "updated_at": now})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
