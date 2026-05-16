-- Migration 003: broker_connections table + live_mode on paper_trade_sessions
--
-- Run against Supabase B using port 5432 (DDL port):
--   psql "${DATABASE_URL_DDL}" -f migrations/003_broker_connections.sql
--
-- Or paste into the Supabase SQL Editor for project dbptdhnamqtfwvupscia.

-- ─── broker_connections ───────────────────────────────────────────────────────
-- One row per user per broker. Stores encrypted access tokens for live trading.

CREATE TABLE IF NOT EXISTS broker_connections (
  id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID        NOT NULL,
  broker           TEXT        NOT NULL DEFAULT 'zerodha',
  api_key          TEXT        NOT NULL,
  api_secret_enc   TEXT        NOT NULL,        -- 'platform_managed' (secret lives in Railway env)
  access_token_enc TEXT,                        -- Fernet-encrypted daily access token
  token_fetched_at TIMESTAMPTZ,
  broker_user_id   TEXT,                        -- Zerodha user ID (e.g. "ZP1234")
  status           TEXT        NOT NULL DEFAULT 'connecting', -- connecting | connected | token_expired
  created_at       TIMESTAMPTZ DEFAULT NOW(),
  updated_at       TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (user_id, broker)
);

-- ─── paper_trade_sessions — live_mode columns ─────────────────────────────────
-- live_mode=true rows use KiteAdapter instead of PaperAdapter for order execution.
-- Paper and live sessions are always independent (never upgrade paper → live).

ALTER TABLE paper_trade_sessions
  ADD COLUMN IF NOT EXISTS live_mode BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS broker    TEXT;
