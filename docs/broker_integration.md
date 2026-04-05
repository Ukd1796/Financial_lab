# Broker Integration — Zerodha & Groww

## Broker API Reality Check

| Broker | Official API | Cost | Auth Model | Notes |
|---|---|---|---|---|
| **Zerodha** | ✅ Kite Connect | ₹2,000/month | OAuth, token expires daily at midnight IST | Well-documented, widely used |
| **Groww** | ❌ No public API | — | — | No official third-party trading API exists as of 2025. Groww Pro is their platform but not API-accessible for automation. |

**Practical decision:** Start with Zerodha only. Groww cannot be integrated via a legitimate API — attempting to automate it would violate their ToS. If Groww releases an official API later, the adapter pattern in the codebase makes it trivial to add.

---

## How Zerodha Kite Connect Works

```
Day 0 (one-time):
  User creates a Kite Connect app at developers.kite.trade
  Gets: api_key + api_secret
  Stores them in their profile on tactiq.in

Every trading day (before 9:15 AM IST):
  1. User opens tactiq.in → clicks "Re-authenticate Zerodha"
  2. Redirects to → https://kite.trade/connect/login?api_key=xxx
  3. User logs in to Zerodha, approves access
  4. Zerodha redirects back → https://api.tactiq.in/api/broker/callback/zerodha?request_token=yyy
  5. Backend exchanges request_token + api_secret → access_token
  6. access_token stored in DB, valid until midnight IST
  7. run_orders.py picks it up at 9:15 AM and places real orders
```

**Key constraint:** Zerodha access tokens expire every day at midnight IST. The user must re-authenticate daily. This is Zerodha's policy and cannot be bypassed.

---

## Database Changes

### New table: `broker_connections` (Supabase B)

```sql
-- Run in Supabase B SQL editor
CREATE TABLE IF NOT EXISTS public.broker_connections (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    broker          text NOT NULL CHECK (broker IN ('zerodha')),
    api_key         text NOT NULL,
    api_secret_enc  text NOT NULL,   -- AES-encrypted, never returned to frontend
    access_token    text,            -- refreshed daily, encrypted
    token_fetched_at timestamptz,
    zerodha_user_id text,            -- e.g. "ZP1234" — returned in Zerodha login response
    status          text NOT NULL DEFAULT 'connected'
                    CHECK (status IN ('connected', 'token_expired', 'disconnected')),
    created_at      timestamptz DEFAULT now(),
    updated_at      timestamptz DEFAULT now(),
    UNIQUE (user_id, broker)
);

ALTER TABLE public.broker_connections ENABLE ROW LEVEL SECURITY;

-- Users can only see and modify their own connection
CREATE POLICY "owner_select" ON public.broker_connections
    FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "owner_insert" ON public.broker_connections
    FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "owner_update" ON public.broker_connections
    FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "owner_delete" ON public.broker_connections
    FOR DELETE USING (auth.uid() = user_id);
```

### `paper_trade_sessions` — add `live_mode` column

```sql
ALTER TABLE public.paper_trade_sessions
    ADD COLUMN IF NOT EXISTS live_mode boolean NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS broker text;   -- 'zerodha' when live_mode=true
```

---

## Backend Changes

### 1. New dependency

```
# Add to requirements.txt
kiteconnect>=5.0.1
cryptography>=42.0.0
```

### 2. Encryption helper — `app/broker/crypto.py`

Encrypts api_secret and access_token at rest using a server-side `BROKER_ENCRYPTION_KEY` env var:

```python
# app/broker/crypto.py
import os, base64
from cryptography.fernet import Fernet

def _fernet() -> Fernet:
    key = os.environ.get("BROKER_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError("BROKER_ENCRYPTION_KEY not set")
    return Fernet(key.encode())

def encrypt(plaintext: str) -> str:
    return _fernet().encrypt(plaintext.encode()).decode()

def decrypt(ciphertext: str) -> str:
    return _fernet().decrypt(ciphertext.encode()).decode()
```

Generate a key once and store it in Railway Variables:
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. KiteAdapter — `app/broker/kite_adapter.py`

```python
# app/broker/kite_adapter.py
from kiteconnect import KiteConnect
from app.broker.base import BrokerAdapter
from app.broker.models import BrokerPosition, Order

class KiteAdapter(BrokerAdapter):
    def __init__(self, api_key: str, access_token: str):
        self.kite = KiteConnect(api_key=api_key)
        self.kite.set_access_token(access_token)

    def place_order(self, symbol, action, quantity, order_type="MARKET", notes="") -> str:
        transaction = self.kite.TRANSACTION_TYPE_BUY if action == "BUY" \
                      else self.kite.TRANSACTION_TYPE_SELL
        order_id = self.kite.place_order(
            variety=self.kite.VARIETY_REGULAR,
            exchange=self.kite.EXCHANGE_NSE,
            tradingsymbol=symbol,
            transaction_type=transaction,
            quantity=quantity,
            product=self.kite.PRODUCT_CNC,       # delivery for equity
            order_type=self.kite.ORDER_TYPE_MARKET,
        )
        return str(order_id)

    def get_order_status(self, order_id: str) -> Order:
        orders = self.kite.orders()
        row = next((o for o in orders if str(o["order_id"]) == order_id), None)
        if row is None:
            return Order(order_id=order_id, symbol="", action="", quantity=0,
                         order_type="MARKET", status="NOT_FOUND")
        status_map = {"COMPLETE": "FILLED", "REJECTED": "REJECTED",
                      "CANCELLED": "CANCELLED", "OPEN": "PLACED"}
        return Order(
            order_id=order_id, symbol=row["tradingsymbol"],
            action="BUY" if row["transaction_type"] == "BUY" else "SELL",
            quantity=row["quantity"], order_type="MARKET",
            status=status_map.get(row["status"], "PENDING"),
            fill_price=row.get("average_price"),
            fill_qty=row.get("filled_quantity"),
        )

    def get_positions(self) -> list[BrokerPosition]:
        data = self.kite.positions()
        return [
            BrokerPosition(symbol=p["tradingsymbol"], quantity=p["quantity"],
                           average_price=p["average_price"])
            for p in data.get("net", []) if p["quantity"] > 0
        ]

    def cancel_order(self, order_id: str) -> bool:
        try:
            self.kite.cancel_order(variety=self.kite.VARIETY_REGULAR, order_id=order_id)
            return True
        except Exception:
            return True   # already filled/cancelled
```

### 4. New API router — `api/routers/broker.py`

**Endpoints:**

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/broker/connect/zerodha` | Save api_key + api_secret, return login URL |
| `GET` | `/api/broker/callback/zerodha` | Handle OAuth redirect, exchange token, store |
| `GET` | `/api/broker/status` | Return connection status + token age |
| `DELETE` | `/api/broker/disconnect` | Remove connection |

**`POST /api/broker/connect/zerodha`** request body:
```json
{
  "api_key": "xxxx",
  "api_secret": "yyyy",
  "user_id": "supabase-uuid"
}
```
Response:
```json
{
  "login_url": "https://kite.trade/connect/login?api_key=xxxx&v=3"
}
```

**`GET /api/broker/callback/zerodha?request_token=zzz&user_id=uuid`**
- Exchanges `request_token` → `access_token` using stored `api_key` + decrypted `api_secret`
- Stores encrypted `access_token` in `broker_connections`
- Redirects to `https://tactiq.in/live-trading?connected=true`

**`GET /api/broker/status?user_id=uuid`** response:
```json
{
  "broker": "zerodha",
  "status": "connected",
  "zerodha_user_id": "ZP1234",
  "token_fetched_at": "2026-04-05T07:30:00",
  "token_valid": true
}
```

### 5. Update `run_paper_orders.py` for live sessions

When a session has `live_mode=true`, swap PaperAdapter → KiteAdapter:

```python
def _get_broker(sess: dict):
    if not sess.get("live_mode"):
        return PaperAdapter()
    # Load broker connection for session owner
    row = db.execute(text(
        "SELECT api_key, api_secret_enc, access_token "
        "FROM broker_connections WHERE user_id = :uid AND broker = 'zerodha'"
    ), {"uid": sess["user_id"]}).fetchone()
    if row is None or not row.access_token:
        print(f"  [SKIP] {sess['session_id']} — no active Zerodha token")
        return None
    from app.broker.crypto import decrypt
    from app.broker.kite_adapter import KiteAdapter
    return KiteAdapter(api_key=row.api_key, access_token=decrypt(row.access_token))
```

---

## Frontend Changes

### 1. Replace `LiveTradingPage.tsx` waitlist with real UI

The page needs three states:

**State A — Not connected:**
```
[ Connect Zerodha ]  ← opens a form to enter api_key + api_secret
                        then calls POST /api/broker/connect/zerodha
                        then redirects to the Zerodha login URL returned
```

**State B — Connected, token valid:**
```
✅ Zerodha connected (ZP1234)
   Token valid until midnight IST
   [ Enable Live Trading for my session ]
   [ Re-authenticate ] [ Disconnect ]
```

**State C — Connected, token expired (every morning):**
```
⚠️  Token expired — re-authenticate to trade today
   [ Re-authenticate Zerodha ]  ← same OAuth flow
```

### 2. New frontend API hooks — `src/api/broker.ts`

```typescript
// POST /api/broker/connect/zerodha → returns { login_url }
export function useConnectZerodha() { ... }

// GET /api/broker/status
export function useBrokerStatus(userId: string) { ... }

// DELETE /api/broker/disconnect
export function useDisconnectBroker() { ... }
```

### 3. OAuth callback handling

After Zerodha redirects to `https://api.tactiq.in/api/broker/callback/zerodha`, the backend redirects to:
```
https://tactiq.in/live-trading?connected=true
```

`LiveTradingPage.tsx` reads the `?connected=true` query param and shows a success toast.

---

## Environment Variables to Add

| Variable | Where | Value |
|---|---|---|
| `BROKER_ENCRYPTION_KEY` | Railway | Generated Fernet key (see above) |
| `KITE_REDIRECT_URL` | Railway | `https://api.tactiq.in/api/broker/callback/zerodha` |
| `FRONTEND_URL` | Railway | `https://tactiq.in` |

> `FRONTEND_URL` is used by the callback endpoint to redirect the user after OAuth completes.
> The Zerodha callback URL (`/api/broker/callback/zerodha?user_id=...`) must also be registered
> under **Redirect URL** in your Kite Connect app at developers.kite.trade.

The `KITE_REDIRECT_URL` must also be registered in your Kite Connect app settings at developers.kite.trade under "Redirect URL".

---

## Daily Re-auth UX (Important)

Zerodha's daily token expiry is a real friction point. Mitigate it:

1. **Email reminder at 8:30 AM IST** — if a user has `live_mode=true` and their token is from yesterday, send an email: _"Re-authenticate Zerodha before 9:15 AM to enable today's trades"_
2. **Dashboard banner** — if token expired, show a persistent warning on the paper-trade dashboard
3. **Fallback** — if `live_mode=true` but no valid token at order time, fall back to logging signals as PENDING (don't skip them silently) and email the user

---

## Implementation Order

| Step | What | Effort |
|---|---|---|
| 1 | Create `broker_connections` table in Supabase B | 10 min |
| 2 | Add `BROKER_ENCRYPTION_KEY` to Railway + `.env` | 5 min |
| 3 | Write `app/broker/crypto.py` | 15 min |
| 4 | Write `app/broker/kite_adapter.py` | 1 hr |
| 5 | Write `api/routers/broker.py` (4 endpoints) | 1.5 hr |
| 6 | Register broker router in `api/main.py` | 5 min |
| 7 | Update `run_paper_orders.py` to swap broker by session | 30 min |
| 8 | Replace `LiveTradingPage.tsx` with real connection UI | 2 hr |
| 9 | Add `src/api/broker.ts` hooks | 30 min |
| 10 | Add `live_mode` + `broker` columns to `paper_trade_sessions` | 10 min |
| 11 | Add 8:30 AM IST Railway cron for re-auth email reminders | 20 min |

**Total: ~6–7 hours of focused work.**

One Kite Connect app (₹2,000/month) covers all users on tactiq.in — you don't need one app per user.
