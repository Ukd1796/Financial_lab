# app/core/push.py
#
# Expo push notification helper. Mirrors notify.py — no state, just a function.
# Expo's Push API is free and requires no server-side SDK; plain HTTP POST suffices.
#
# Usage:
#   from app.core.push import send_push, send_push_to_session_user
#   send_push("ExponentPushToken[...]", title="Signals Ready", body="3 BUY signals today")
#   send_push_to_session_user(session_id, title="...", body="...")

import requests

_EXPO_URL = "https://exp.host/--/api/v2/push/send"


def send_push(token: str, title: str, body: str, data: dict | None = None) -> bool:
    """Send a push notification to a single Expo push token."""
    if not token or not token.startswith("ExponentPushToken"):
        print(f"  [Push] Invalid token: {token[:30] if token else 'None'}")
        return False
    payload: dict = {"to": token, "title": title, "body": body, "sound": "default"}
    if data:
        payload["data"] = data
    try:
        resp = requests.post(
            _EXPO_URL,
            json=payload,
            timeout=10,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        result = resp.json()
        status = (result.get("data") or {}).get("status", "unknown")
        if resp.status_code == 200 and status == "ok":
            print(f"  [Push] Sent → {token[:35]}...")
            return True
        details = (result.get("data") or {}).get("details", result)
        print(f"  [Push] Expo error [{status}]: {details}")
        return False
    except Exception as exc:
        print(f"  [Push] Request failed: {exc}")
        return False


def send_push_to_session_user(
    session_id: str, title: str, body: str, data: dict | None = None
) -> bool:
    """Look up the push token for the user who owns session_id and send a notification."""
    from sqlalchemy import text
    from app.core.database import SessionLocal

    db = SessionLocal()
    try:
        row = db.execute(
            text(
                "SELECT pt.token FROM push_tokens pt "
                "JOIN paper_trade_sessions pts ON pts.user_id = pt.user_id "
                "WHERE pts.session_id = :sid"
            ),
            {"sid": session_id},
        ).fetchone()
        if row is None:
            print(f"  [Push] No token for session {session_id} — skipping")
            return False
        return send_push(row.token, title, body, data)
    except Exception as exc:
        print(f"  [Push] DB lookup failed for {session_id}: {exc}")
        return False
    finally:
        db.close()
