-- scripts/broker_tables.sql
--
-- Run this in Supabase B SQL editor (the project at dbptdhnamqtfwvupscia).
--
-- Creates:
--   broker_connections   — stores encrypted API credentials per user/broker
--   Adds live_mode + broker columns to paper_trade_sessions
--
-- Safe to re-run (uses IF NOT EXISTS / ADD COLUMN IF NOT EXISTS).
-- ─────────────────────────────────────────────────────────────────────────────

-- ─── 1. broker_connections ───────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS public.broker_connections (
    id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    broker           text        NOT NULL,                          -- 'zerodha', future: 'upstox', 'angelone'
    api_key          text        NOT NULL,
    api_secret_enc   text        NOT NULL,   -- Fernet-encrypted, never returned to frontend
    access_token_enc text,                   -- Fernet-encrypted, refreshed daily via OAuth
    token_fetched_at timestamptz,
    broker_user_id   text,                   -- e.g. "ZP1234" from Zerodha login response
    status           text        NOT NULL DEFAULT 'connected'
                                 CHECK (status IN ('connected', 'token_expired', 'disconnected')),
    created_at       timestamptz NOT NULL DEFAULT now(),
    updated_at       timestamptz NOT NULL DEFAULT now(),
    UNIQUE (user_id, broker)
);

-- Row-level security: users can only see/modify their own connection
ALTER TABLE public.broker_connections ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'broker_connections' AND policyname = 'owner_select'
    ) THEN
        CREATE POLICY "owner_select" ON public.broker_connections
            FOR SELECT USING (auth.uid() = user_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'broker_connections' AND policyname = 'owner_insert'
    ) THEN
        CREATE POLICY "owner_insert" ON public.broker_connections
            FOR INSERT WITH CHECK (auth.uid() = user_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'broker_connections' AND policyname = 'owner_update'
    ) THEN
        CREATE POLICY "owner_update" ON public.broker_connections
            FOR UPDATE USING (auth.uid() = user_id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'broker_connections' AND policyname = 'owner_delete'
    ) THEN
        CREATE POLICY "owner_delete" ON public.broker_connections
            FOR DELETE USING (auth.uid() = user_id);
    END IF;
END $$;

-- Service-role bypass policy so the backend (Railway) can write tokens
-- without needing an authenticated user JWT on every cron run.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies
        WHERE tablename = 'broker_connections' AND policyname = 'service_role_all'
    ) THEN
        CREATE POLICY "service_role_all" ON public.broker_connections
            USING (auth.role() = 'service_role')
            WITH CHECK (auth.role() = 'service_role');
    END IF;
END $$;

-- ─── 2. paper_trade_sessions — add live_mode + broker ────────────────────────

ALTER TABLE public.paper_trade_sessions
    ADD COLUMN IF NOT EXISTS live_mode boolean NOT NULL DEFAULT false,
    ADD COLUMN IF NOT EXISTS broker    text;    -- 'zerodha' when live_mode = true

-- ─── Done ─────────────────────────────────────────────────────────────────────
-- Verify:
--   SELECT table_name FROM information_schema.tables
--   WHERE table_schema = 'public' AND table_name = 'broker_connections';
