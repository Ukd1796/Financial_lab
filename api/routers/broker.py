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
from fastapi.responses import RedirectResponse
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
    user_id: str = Query(...),
):
    """
    OAuth callback handler. Zerodha redirects here with ?request_token=xxx&user_id=yyy.
    Exchanges request_token → access_token using platform env var credentials.
    """
    if broker not in _BROKER_HANDLERS:
        raise HTTPException(status_code=400, detail=f"Unsupported broker: {broker}")

    try:
        api_key, api_secret = _get_platform_credentials(broker)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    _, exchange_fn = _BROKER_HANDLERS[broker]

    # Verify a connection row exists for this user
    db = SessionLocal()
    try:
        existing = db.execute(
            text("SELECT id FROM broker_connections WHERE user_id = :uid AND broker = :broker"),
            {"uid": user_id, "broker": broker},
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=404,
                detail="No broker connection row found. Initiate connect first.",
            )

        try:
            result = exchange_fn(api_key, api_secret, request_token)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=f"Token exchange failed: {exc}")

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
                "fetched_at":     datetime.utcnow(),
                "broker_user_id": result.get("broker_user_id", ""),
                "now":            datetime.utcnow(),
                "uid":            user_id,
                "broker":         broker,
            },
        )
        db.commit()
    finally:
        db.close()

    frontend_url = os.environ.get("FRONTEND_URL", "https://tactiq.in")
    return RedirectResponse(url=f"{frontend_url}/live-trading?connected=true&broker={broker}")


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

    if row is None:
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
