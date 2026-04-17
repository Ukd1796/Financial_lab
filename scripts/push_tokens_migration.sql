-- =============================================================================
-- Migration: Push notifications support (run in Supabase B SQL editor)
-- =============================================================================

-- 1. Add user_id to paper_trade_sessions if not already present
-- (The frontend writes sessions directly via Supabase JS; this column ties each
-- session to a Supabase auth user so we can look up their push token.)
ALTER TABLE paper_trade_sessions
    ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES auth.users(id) ON DELETE SET NULL;

-- 2. push_tokens — one row per user, upserted by the mobile app on sign-in
CREATE TABLE IF NOT EXISTS push_tokens (
    user_id    uuid REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    token      text NOT NULL,
    updated_at timestamptz DEFAULT now()
);

ALTER TABLE push_tokens ENABLE ROW LEVEL SECURITY;

-- Users can only read/write their own token
CREATE POLICY "push_tokens: own row only"
    ON push_tokens
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
