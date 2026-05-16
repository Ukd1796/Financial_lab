# api/routers/broker.py
#
# Broker connection management — generic OAuth + credential storage.
# Currently supports Zerodha (Kite Connect). Extend _BROKER_HANDLERS for new brokers.
#
# Platform model: ONE Kite Connect app owned by the platform operator.
# api_key and api_secret are stored in Railway env vars (KITE_API_KEY, KITE_API_SECRET).
# Each end-user just needs a Zerodha trading account — they never enter API credentials.
#
# Endpoints:
#   POST   /api/broker/connect/{broker}     — create row + return OAuth login URL
#   GET    /api/broker/callback/{broker}    — OAuth callback, exchange token, store, redirect
#   GET    /api/broker/status               — connection status for a user
#   DELETE /api/broker/disconnect           — remove connection

import os
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import text

from app.broker.crypto import encrypt, decrypt
from app.core.database import SessionLocal

router = APIRouter()

# ---------------------------------------------------------------------------
# IST timezone helper
# ---------------------------------------------------------------------------
_IST = timezone(timedelta(hours=5, minutes=30))


def _ist_now() -> datetime:
    return datetime.now(_IST)


def _token_is_valid(fetched_at: Optional[datetime]) -> bool:
    """
    A Zerodha access_token is valid until midnight IST on the day it was issued.
    Returns True if token_fetched_at is today in IST and current IST time < midnight.
    """
    if fetched_at is None:
        return False
    now_ist = _ist_now()
    if fetched_at.tzinfo is None:
        fetched_at = fetched_at.replace(tzinfo=timezone.utc)
    fetched_ist = fetched_at.astimezone(_IST)
    return fetched_ist.date() == now_ist.date()


# ---------------------------------------------------------------------------
# Platform credentials — loaded from env vars, never from user input
# ---------------------------------------------------------------------------

def _get_platform_credentials(broker: str) -> tuple[str, str]:
    """
    Returns (api_key, api_secret) for the given broker from environment variables.
    Raises RuntimeError if not configured.
    """
    if broker == "zerodha":
        api_key = os.environ.get("KITE_API_KEY")
        api_secret = os.environ.get("KITE_API_SECRET")
        if not api_key or not api_secret:
            raise RuntimeError(
                "KITE_API_KEY and KITE_API_SECRET must be set in Railway Variables."
            )
        return api_key, api_secret
    raise RuntimeError(f"No platform credentials configured for broker: {broker}")


# ---------------------------------------------------------------------------
# Broker-specific OAuth handlers — add new brokers here
# ---------------------------------------------------------------------------

def _zerodha_login_url(api_key: str) -> str:
    return f"https://kite.trade/connect/login?api_key={api_key}&v=3"


def _zerodha_exchange_token(api_key: str, api_secret: str, request_token: str) -> dict:
    from kiteconnect import KiteConnect
    kite = KiteConnect(api_key=api_key)
    session_data = kite.generate_session(request_token, api_secret=api_secret)
    return {
        "access_token":   session_data["access_token"],
        "broker_user_id": session_data.get("user_id", ""),
    }


_BROKER_HANDLERS = {
    "zerodha": (_zerodha_login_url, _zerodha_exchange_token),
}

_SUPPORTED_BROKERS = list(_BROKER_HANDLERS.keys())


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class ConnectRequest(BaseModel):
    user_id: str   # Supabase user UUID — the only thing the frontend sends


# ---------------------------------------------------------------------------
# POST /api/broker/connect/{broker}
# ---------------------------------------------------------------------------

@router.post("/connect/{broker}")
def connect_broker(broker: str, body: ConnectRequest):
    """
    Create (or reset) a broker connection row for the user and return the OAuth login URL.
    Platform api_key/secret come from env vars — users never provide them.
    """
    if broker not in _BROKER_HANDLERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported broker: {broker}. Supported: {_SUPPORTED_BROKERS}",
        )

    try:
        api_key, _ = _get_platform_credentials(broker)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    login_url_fn, _ = _BROKER_HANDLERS[broker]
    login_url = login_url_fn(api_key)

    db = SessionLocal()
    try:
        existing = db.execute(
            text("SELECT id FROM broker_connections WHERE user_id = :uid AND broker = :broker"),
            {"uid": body.user_id, "broker": broker},
        ).fetchone()

        now = datetime.utcnow()

        if existing:
            # Clear the old token — access_token_enc = NULL signals "OAuth in progress"
            db.execute(
                text("""
                    UPDATE broker_connections
                    SET access_token_enc = NULL,
                        token_fetched_at = NULL,
                        status           = 'connected',
                        updated_at       = :now
                    WHERE user_id = :uid AND broker = :broker
                """),
                {"now": now, "uid": body.user_id, "broker": broker},
            )
        else:
            # api_key stored for reference; api_secret_enc stores placeholder
            # (actual secret is always read from env at callback time)
            db.execute(
                text("""
                    INSERT INTO broker_connections
                        (id, user_id, broker, api_key, api_secret_enc, status, created_at, updated_at)
                    VALUES
                        (gen_random_uuid(), :uid, :broker, :api_key, 'platform_managed', 'connected', :now, :now)
                """),
                {
                    "uid":     body.user_id,
                    "broker":  broker,
                    "api_key": api_key,
                    "now":     now,
                },
            )
        db.commit()
    finally:
        db.close()

    return {"broker": broker, "login_url": login_url}


# ---------------------------------------------------------------------------
# GET /api/broker/callback/{broker}
# ---------------------------------------------------------------------------

@router.get("/callback/{broker}")
def broker_callback(
    broker: str,
    request_token: str = Query(...),
    user_id: Optional[str] = Query(None),
):
    """
    OAuth callback handler. Zerodha redirects here with ?request_token=xxx.
    user_id is NOT sent by Zerodha — we resolve the user from the most recently
    initiated row (access_token_enc IS NULL = OAuth in progress, timing-based).
    """
    if broker not in _BROKER_HANDLERS:
        return _html_error("Unsupported broker.")

    try:
        api_key, api_secret = _get_platform_credentials(broker)
    except RuntimeError as exc:
        return _html_error(str(exc))

    _, exchange_fn = _BROKER_HANDLERS[broker]

    try:
        result = exchange_fn(api_key, api_secret, request_token)
    except Exception as exc:
        return _html_error(f"Token exchange failed: {exc}")

    broker_user_id = result.get("broker_user_id", "")
    now = datetime.utcnow()
    # Connections initiated in the last 15 minutes are considered pending
    cutoff = now - timedelta(minutes=15)

    db = SessionLocal()
    try:
        if user_id:
            # Explicit user_id provided (e.g., future deep-link flow)
            row = db.execute(
                text("SELECT user_id FROM broker_connections WHERE user_id = :uid AND broker = :broker"),
                {"uid": user_id, "broker": broker},
            ).fetchone()
            resolved_uid = user_id if row else None
        else:
            # Resolve by timing: find the most recently initiated row where
            # access_token_enc IS NULL (token not yet received = OAuth in progress).
            # First try matching broker_user_id (re-auth case), then any recent row.
            row = db.execute(
                text("""
                    SELECT user_id FROM broker_connections
                    WHERE broker = :broker
                      AND access_token_enc IS NULL
                      AND updated_at > :cutoff
                      AND (:buid = '' OR broker_user_id IS NULL OR broker_user_id = :buid)
                    ORDER BY updated_at DESC
                    LIMIT 1
                """),
                {"broker": broker, "cutoff": cutoff, "buid": broker_user_id},
            ).fetchone()
            resolved_uid = str(row.user_id) if row else None

        if resolved_uid is None:
            return _html_error("No pending connection found. Please initiate connect again from the app.")

        db.execute(
            text("""
                UPDATE broker_connections
                SET access_token_enc = :token_enc,
                    token_fetched_at = :fetched_at,
                    broker_user_id   = :broker_user_id,
                    status           = 'connected',
                    updated_at       = :now
                WHERE user_id = :uid AND broker = :broker
            """),
            {
                "token_enc":      encrypt(result["access_token"]),
                "fetched_at":     now,
                "broker_user_id": broker_user_id,
                "now":            now,
                "uid":            resolved_uid,
                "broker":         broker,
            },
        )
        db.commit()
    finally:
        db.close()

    return _html_success(broker)


def _html_success(broker: str) -> HTMLResponse:
    return HTMLResponse(f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Connected</title>
<style>body{{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#fff;
display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}}
.card{{padding:40px 32px;max-width:360px}}
.icon{{font-size:48px;margin-bottom:16px}}
h1{{font-size:22px;margin:0 0 8px}}
p{{color:#888;font-size:14px;line-height:1.5;margin:0}}
</style></head>
<body><div class="card">
<div class="icon">✓</div>
<h1>Zerodha Connected</h1>
<p>You can close this window and return to TacTiq.<br>Your live trading session is ready.</p>
</div></body></html>""")


def _html_error(message: str) -> HTMLResponse:
    return HTMLResponse(f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Error</title>
<style>body{{font-family:-apple-system,sans-serif;background:#0a0a0a;color:#fff;
display:flex;align-items:center;justify-content:center;height:100vh;margin:0;text-align:center}}
.card{{padding:40px 32px;max-width:360px}}
.icon{{font-size:48px;margin-bottom:16px}}
h1{{font-size:22px;margin:0 0 8px}}
p{{color:#888;font-size:14px;line-height:1.5;margin:0}}
</style></head>
<body><div class="card">
<div class="icon">✗</div>
<h1>Connection Failed</h1>
<p>{message}<br><br>Please return to TacTiq and try again.</p>
</div></body></html>""", status_code=400)


# ---------------------------------------------------------------------------
# GET /api/broker/status
# ---------------------------------------------------------------------------

@router.get("/status")
def broker_status(user_id: str = Query(...), broker: str = Query("zerodha")):
    """Returns the current connection status and token validity for a user + broker."""
    if broker not in _BROKER_HANDLERS:
        raise HTTPException(status_code=400, detail=f"Unsupported broker: {broker}")

    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT broker, status, broker_user_id, token_fetched_at, access_token_enc
                FROM broker_connections
                WHERE user_id = :uid AND broker = :broker
            """),
            {"uid": user_id, "broker": broker},
        ).fetchone()
    finally:
        db.close()

    if row is None or row.access_token_enc is None:
        return {"connected": False, "broker": broker}

    token_valid = _token_is_valid(row.token_fetched_at) and bool(row.access_token_enc)

    if not token_valid and row.status == "connected" and row.access_token_enc:
        _mark_token_expired(user_id, broker)

    return {
        "connected":        True,
        "broker":           row.broker,
        "status":           "connected" if token_valid else "token_expired",
        "broker_user_id":   row.broker_user_id,
        "token_fetched_at": row.token_fetched_at.isoformat() if row.token_fetched_at else None,
        "token_valid":      token_valid,
    }


# ---------------------------------------------------------------------------
# DELETE /api/broker/disconnect
# ---------------------------------------------------------------------------

@router.delete("/disconnect")
def disconnect_broker(user_id: str = Query(...), broker: str = Query("zerodha")):
    """Remove a broker connection entirely."""
    if broker not in _BROKER_HANDLERS:
        raise HTTPException(status_code=400, detail=f"Unsupported broker: {broker}")

    db = SessionLocal()
    try:
        db.execute(
            text("DELETE FROM broker_connections WHERE user_id = :uid AND broker = :broker"),
            {"uid": user_id, "broker": broker},
        )
        db.commit()
    finally:
        db.close()

    return {"disconnected": True, "broker": broker}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _mark_token_expired(user_id: str, broker: str) -> None:
    db = SessionLocal()
    try:
        db.execute(
            text("""
                UPDATE broker_connections
                SET status = 'token_expired', updated_at = :now
                WHERE user_id = :uid AND broker = :broker
            """),
            {"now": datetime.utcnow(), "uid": user_id, "broker": broker},
        )
        db.commit()
    finally:
        db.close()


def get_active_access_token(user_id: str, broker: str) -> Optional[str]:
    """
    Returns the decrypted access_token if valid, None otherwise.
    Called by run_paper_orders.py when live_mode=True.
    """
    db = SessionLocal()
    try:
        row = db.execute(
            text("""
                SELECT access_token_enc, token_fetched_at
                FROM broker_connections
                WHERE user_id = :uid AND broker = :broker
            """),
            {"uid": user_id, "broker": broker},
        ).fetchone()
    finally:
        db.close()

    if row is None or not row.access_token_enc:
        return None
    if not _token_is_valid(row.token_fetched_at):
        return None
    return decrypt(row.access_token_enc)
