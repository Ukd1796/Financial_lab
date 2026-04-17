# api/routers/users.py
#
# User-facing endpoints that don't belong to a specific feature domain.
#
#   POST /api/users/push-token — upsert Expo push token for a user

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import text

from app.core.database import SessionLocal

router = APIRouter()


class PushTokenBody(BaseModel):
    user_id: str
    token: str


@router.post("/push-token", status_code=200)
def upsert_push_token(body: PushTokenBody):
    """Register or refresh the Expo push token for a user. Called by the mobile app on sign-in."""
    if not body.token.startswith("ExponentPushToken"):
        raise HTTPException(status_code=400, detail="token must be an ExponentPushToken")
    db = SessionLocal()
    try:
        db.execute(
            text("""
                INSERT INTO push_tokens (user_id, token, updated_at)
                VALUES (:uid, :token, now())
                ON CONFLICT (user_id)
                DO UPDATE SET token = EXCLUDED.token, updated_at = now()
            """),
            {"uid": body.user_id, "token": body.token},
        )
        db.commit()
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        db.close()
