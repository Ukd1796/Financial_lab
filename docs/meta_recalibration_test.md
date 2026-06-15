

---

## Meta Recalibration Test — 2026-05-30 20:23

**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  
**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + `_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  
**Costs:** 0.10% commission + 0.05% slippage per side  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=1`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2017-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Full  2018–2024   (2018-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2018-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2018-01-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2018-01-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2018-01-16 → Breakout WR 20.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] 2018-01-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2018-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-02-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-02-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-02-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-02-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-03-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2018-03-11 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-03-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-03-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2018-04-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-04-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-04-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-04-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-04-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2018-05-06 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2018-05-13 [BULL_MEDVOL/MEDIUM] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2018-05-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-05-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-06-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-06-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2018-06-17 [MIXED/LOW] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2018-06-24 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2018-07-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-07-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-07-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-07-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-07-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2018-08-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-08-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-08-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-08-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-09-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-09-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-09-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2018-09-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2018-09-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-10-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-10-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2018-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2018-10-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-11-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2018-11-11 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2018-11-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2018-11-25 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-12-02 [MIXED/LOW] → DualMA=0.45  Breakout=0.30  QuietBrk=0.25  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2018-12-09 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2018-12-16 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2018-12-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2018-12-30 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-05-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-06-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-06-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-03-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-05-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-05-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-01-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.10
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.10
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-02-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-02-26 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-05 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-03-12 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      1.14    98.34%   24.09%    1.41  44.5%     4711
                         (LLM calls: 337)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         2901       +60221     40.7%        +21    66.1%
  QuietBrk          546       +15001     35.2%        +27    16.5%
  RSI-MR            795        +8894     56.9%        +11     9.8%
  TrendPB           405        +3992     58.0%        +10     4.4%
  DualMA             64        +2948     53.1%        +46     3.2%
  TOTAL            4711       +91056
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          31201    5925      25249         27       64       18.8%
  Breakout        46651   38047       1965       6639     1958       77.4%
  QuietBrk        14007    4101       9518        388      470       25.9%
  TrendPB         37334    5675      15016      16643      287       14.4%
  RSI-MR          26310    2697      15582       8031      670        7.7%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter               1814         9       1.15
  MeanReversionUniverseFilter          6747        20       4.27
  DualMAUniverseFilter                 3430        16       2.17

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Full  2018–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 4711  (2095 winners / 2616 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.3%   (price continued post-exit)
    False breakout rate  :   34.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.216      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.07%    +0.40%    +0.74%
    Losers       -0.09%    +0.04%    +0.22%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (1581 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.0%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.004  (>0 = stable universe → better trades)
    Turnover vs success  : +0.003  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              269    50.6%     0.79%
    HIGH_VOL_UPTREND              2038    44.9%     1.17%
    LOW_VOL_SIDEWAYS               277    51.6%     2.26%
    LOW_VOL_UPTREND                835    41.0%     0.43%
    MID_VOL_SIDEWAYS               251    48.2%     0.39%
    MID_VOL_UPTREND               1041    42.1%     1.07%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2019-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2019-01-21 → Breakout WR 21.4% < 40% over last 14 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2019-05-12 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2019-05-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-26 [MIXED/LOW] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  Adaptive  (5-strat)     -0.11    -1.26%    6.87%    0.91  42.9%      854
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            265        +3728     58.5%        +14  -136.5%
  TrendPB            56          +78     46.4%         +1    -2.8%
  DualMA             17         -735     23.5%        -43    26.9%
  QuietBrk           86        -2363     23.3%        -27    86.5%
  Breakout          430        -3440     37.4%         -8   125.9%
  TOTAL             854        -2732
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5432    1687       3741          4       17       30.7%
  Breakout         7106    4771        907       1428      214       64.1%
  QuietBrk         2039     667       1307         65       54       30.1%
  TrendPB          5733    1108       2392       2233       26       18.9%
  RSI-MR           5011     815       3040       1156      113       14.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 854  (366 winners / 488 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.7%   (price continued post-exit)
    False breakout rate  :   35.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.225      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.16%    -0.00%    +0.23%
    Losers       -0.03%    -0.11%    -0.10%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.020  (>0 = stable universe → better trades)
    Turnover vs success  : +0.085  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               44    50.0%     1.49%
    HIGH_VOL_UPTREND               238    48.7%     0.79%
    LOW_VOL_SIDEWAYS               103    53.4%     0.60%
    LOW_VOL_UPTREND                192    34.9%    -0.68%
    MID_VOL_SIDEWAYS                59    45.8%    -0.15%
    MID_VOL_UPTREND                218    36.2%    -0.62%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2020-02-23 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2020-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      2.35    31.48%    6.87%    1.92  48.8%      925
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          518       +21985     42.9%        +42    75.8%
  QuietBrk           96        +4079     41.7%        +42    14.1%
  RSI-MR            197        +1637     62.9%         +8     5.6%
  TrendPB           106        +1260     57.5%        +12     4.3%
  DualMA              8          +44     50.0%         +5     0.2%
  TOTAL             925       +29004
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7148    1034       6106          8       12       14.3%
  Breakout         8460    6919        231       1310      279       78.5%
  QuietBrk         2646     716       1853         77       52       25.1%
  TrendPB          7029    1222       2141       3666       70       16.4%
  RSI-MR           6317     568       3839       1910       63        8.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 925  (451 winners / 474 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.4%   (price continued post-exit)
    False breakout rate  :   37.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.132      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.04%    +0.91%    +1.36%
    Losers       -0.02%    +0.64%    +0.98%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.041  (>0 = stable universe → better trades)
    Turnover vs success  : +0.052  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               29    58.6%    -0.02%
    HIGH_VOL_UPTREND               319    42.9%     1.28%
    LOW_VOL_SIDEWAYS                85    67.1%     4.97%
    LOW_VOL_UPTREND                224    47.3%     1.47%
    MID_VOL_SIDEWAYS                40    72.5%     3.28%
    MID_VOL_UPTREND                228    46.1%     1.99%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [RCAQualityGate] 2020-06-10 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-03-29 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-04-04 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-05-02 [MIXED/LOW] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-05-09 [MIXED/LOW] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.20
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  Adaptive  (5-strat)      3.07    80.28%    7.38%    2.13  50.9%     1977
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1082       +57040     46.0%        +53    71.4%
  QuietBrk          188       +13570     44.7%        +72    17.0%
  RSI-MR            473        +5417     59.8%        +11     6.8%
  DualMA             17        +1908     64.7%       +112     2.4%
  TrendPB           217        +1898     60.4%         +9     2.4%
  TOTAL            1977       +79833
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16386    2828      13535         23       19       17.1%
  Breakout        17215   13442       1037       2736      421       75.6%
  QuietBrk         5164    1342       3645        177       99       24.1%
  TrendPB         14292    2430       4648       7214      105       16.3%
  RSI-MR          14684    1394       8861       4429      196        8.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1977  (1007 winners / 970 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.7%   (price continued post-exit)
    False breakout rate  :   34.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.108      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.10%    +0.70%    +1.14%
    Losers       -0.07%    +0.36%    +0.77%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.005  (>0 = stable universe → better trades)
    Turnover vs success  : -0.017  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              124    58.1%     1.17%
    HIGH_VOL_UPTREND               904    48.6%     1.88%
    LOW_VOL_SIDEWAYS               102    64.7%     4.94%
    LOW_VOL_UPTREND                285    49.8%     1.81%
    MID_VOL_SIDEWAYS               112    61.6%     2.73%
    MID_VOL_UPTREND                450    48.7%     2.00%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      0.24     1.75%   10.56%    1.07  38.4%      526
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          347        +3564     38.3%        +10   202.5%
  DualMA              9          +27     55.6%         +3     1.6%
  RSI-MR             62         -417     48.4%         -7   -23.7%
  TrendPB            43         -567     34.9%        -13   -32.2%
  QuietBrk           65         -848     29.2%        -13   -48.2%
  TOTAL             526        +1760
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           2193     530       1663          0        8       23.8%
  Breakout         5606    4619        212        775      460       74.2%
  QuietBrk         1551     542        952         57      105       28.2%
  TrendPB          4358     730       1747       1881       66       15.2%
  RSI-MR           1594     230        967        397       65       10.4%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 526  (202 winners / 324 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   44.9%   (price continued post-exit)
    False breakout rate  :   38.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.320      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.10%    +0.20%    -0.04%
    Losers       -0.12%    -0.35%    -0.50%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.118  (>0 = stable universe → better trades)
    Turnover vs success  : -0.047  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               14    21.4%    -2.44%
    HIGH_VOL_UPTREND               126    30.2%    -0.82%
    LOW_VOL_SIDEWAYS                63    50.8%     1.63%
    LOW_VOL_UPTREND                160    40.6%    -0.29%
    MID_VOL_SIDEWAYS                34    50.0%     0.39%
    MID_VOL_UPTREND                129    36.4%     0.03%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.35  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-03-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.28  QuietBrk=0.28  TrendPB=0.15  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      1.25    30.34%   10.56%    1.38  45.4%     1718
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1036       +19430     41.6%        +19    74.9%
  QuietBrk          215        +5328     39.5%        +25    20.5%
  TrendPB           115         +738     51.3%         +6     2.8%
  RSI-MR            330         +588     58.8%         +2     2.3%
  DualMA             22         -127     50.0%         -6    -0.5%
  TOTAL            1718       +25957
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          12823    1857      10959          7       29       14.3%
  Breakout        17039   14489        318       2232     1046       78.9%
  QuietBrk         5362    1591       3633        138      264       24.7%
  TrendPB         13431    1853       5918       5660       99       13.1%
  RSI-MR          10860    1172       6353       3335      328        7.8%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1718  (780 winners / 938 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.6%   (price continued post-exit)
    False breakout rate  :   32.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.209      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.04%    +0.40%    +0.74%
    Losers       +0.01%    +0.09%    +0.37%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.062  (>0 = stable universe → better trades)
    Turnover vs success  : -0.030  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               96    47.9%     0.05%
    HIGH_VOL_UPTREND               750    44.5%     0.52%
    LOW_VOL_SIDEWAYS                99    51.5%     1.74%
    LOW_VOL_UPTREND                340    43.5%     0.37%
    MID_VOL_SIDEWAYS                79    55.7%     0.53%
    MID_VOL_UPTREND                354    44.4%     1.08%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [RCAQualityGate] 2025-04-03 → Breakout WR 8.3% < 40% over last 12 trades — CB relaxation disabled
  [AdaptiveSelector] 2025-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-04-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-09-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BEAR_CONFIRMED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2025-12-21 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-12-28 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-04 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-11 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] 2026-01-18 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.21  QuietBrk=0.21  TrendPB=0.21  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-26 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-15 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-02-22 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  Adaptive  (5-strat)     -0.04    -0.49%    4.20%    0.98  36.8%      625
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           92        +1554     30.4%        +17  -316.5%
  RSI-MR            120         +377     50.8%         +3   -76.7%
  TrendPB            16         -201     43.8%        -13    40.8%
  DualMA             12         -668      8.3%        -56   136.0%
  Breakout          385        -1553     34.5%         -4   316.4%
  TOTAL             625         -491
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           4774    1416       3357          1       26       29.1%
  Breakout         5873    4281        869        723      453       65.2%
  QuietBrk         2082     627       1413         42      118       24.4%
  TrendPB          4475     714       2123       1638       31       15.3%
  RSI-MR           4045     592       2309       1144      270        8.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 625  (230 winners / 395 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.0%   (price continued post-exit)
    False breakout rate  :   27.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.324      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.05%    -0.00%    +0.23%
    Losers       +0.29%    +0.32%    +0.84%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.110  (>0 = stable universe → better trades)
    Turnover vs success  : +0.032  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               20    45.0%     0.11%
    HIGH_VOL_UPTREND               138    37.7%    -0.46%
    LOW_VOL_SIDEWAYS                79    34.2%    -0.04%
    LOW_VOL_UPTREND                193    35.8%    -0.38%
    MID_VOL_SIDEWAYS                30    30.0%    -1.52%
    MID_VOL_UPTREND                165    38.8%     0.07%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```


---

## Meta Recalibration Test — 2026-05-30 20:36

**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  
**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + `_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  
**Costs:** 0.10% commission + 0.05% slippage per side  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=1`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2019-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2019-01-21 → Breakout WR 21.4% < 40% over last 14 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2019-05-12 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2019-05-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-26 [MIXED/LOW] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-07-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  Adaptive  (5-strat)     -0.12    -1.31%    6.89%    0.91  42.7%      854
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            265        +3740     58.5%        +14  -135.3%
  TrendPB            55          -16     45.5%         -0     0.6%
  DualMA             17         -735     23.5%        -43    26.6%
  QuietBrk           86        -2376     23.3%        -28    86.0%
  Breakout          431        -3376     37.4%         -8   122.2%
  TOTAL             854        -2763
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5427    1683       3740          4       17       30.7%
  Breakout         7100    4773        902       1425      213       64.2%
  QuietBrk         2040     667       1308         65       54       30.0%
  TrendPB          5726    1104       2388       2234       27       18.8%
  RSI-MR           5006     815       3040       1151      113       14.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 854  (365 winners / 489 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.7%   (price continued post-exit)
    False breakout rate  :   35.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.228      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.17%    -0.00%    +0.23%
    Losers       -0.03%    -0.11%    -0.10%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.018  (>0 = stable universe → better trades)
    Turnover vs success  : +0.084  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               44    50.0%     1.49%
    HIGH_VOL_UPTREND               237    48.5%     0.76%
    LOW_VOL_SIDEWAYS               103    53.4%     0.60%
    LOW_VOL_UPTREND                192    34.9%    -0.68%
    MID_VOL_SIDEWAYS                59    45.8%    -0.15%
    MID_VOL_UPTREND                219    36.1%    -0.63%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2020-02-23 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2020-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      2.35    31.48%    6.87%    1.92  48.8%      925
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          518       +21985     42.9%        +42    75.8%
  QuietBrk           96        +4079     41.7%        +42    14.1%
  RSI-MR            197        +1637     62.9%         +8     5.6%
  TrendPB           106        +1260     57.5%        +12     4.3%
  DualMA              8          +44     50.0%         +5     0.2%
  TOTAL             925       +29004
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7148    1034       6106          8       12       14.3%
  Breakout         8460    6919        231       1310      279       78.5%
  QuietBrk         2646     716       1853         77       52       25.1%
  TrendPB          7029    1222       2141       3666       70       16.4%
  RSI-MR           6317     568       3839       1910       63        8.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 925  (451 winners / 474 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.4%   (price continued post-exit)
    False breakout rate  :   37.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.132      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.04%    +0.91%    +1.36%
    Losers       -0.02%    +0.64%    +0.98%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.041  (>0 = stable universe → better trades)
    Turnover vs success  : +0.052  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               29    58.6%    -0.02%
    HIGH_VOL_UPTREND               319    42.9%     1.28%
    LOW_VOL_SIDEWAYS                85    67.1%     4.97%
    LOW_VOL_UPTREND                224    47.3%     1.47%
    MID_VOL_SIDEWAYS                40    72.5%     3.28%
    MID_VOL_UPTREND                228    46.1%     1.99%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [RCAQualityGate] 2020-06-10 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-03-29 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-04-04 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2021-05-02 [MIXED/LOW] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-05-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.20
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  Adaptive  (5-strat)      3.10    81.35%    7.42%    2.14  50.8%     1975
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1080       +57895     46.0%        +54    71.6%
  QuietBrk          189       +13766     44.4%        +73    17.0%
  RSI-MR            472        +5386     59.3%        +11     6.7%
  DualMA             17        +1946     64.7%       +114     2.4%
  TrendPB           217        +1907     60.4%         +9     2.4%
  TOTAL            1975       +80899
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16386    2827      13536         23       19       17.1%
  Breakout        17220   13446       1028       2746      424       75.6%
  QuietBrk         5179    1343       3659        177       98       24.0%
  TrendPB         14298    2432       4648       7218      105       16.3%
  RSI-MR          14541    1390       8770       4381      195        8.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1975  (1003 winners / 972 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.8%   (price continued post-exit)
    False breakout rate  :   34.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.109      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.10%    +0.70%    +1.13%
    Losers       -0.08%    +0.37%    +0.77%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.011  (>0 = stable universe → better trades)
    Turnover vs success  : -0.015  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              122    58.2%     1.22%
    HIGH_VOL_UPTREND               906    48.2%     1.84%
    LOW_VOL_SIDEWAYS               103    65.0%     5.17%
    LOW_VOL_UPTREND                285    49.8%     1.81%
    MID_VOL_SIDEWAYS               111    62.2%     2.78%
    MID_VOL_UPTREND                448    48.4%     1.99%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      0.24     1.75%   10.56%    1.07  38.4%      526
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          347        +3564     38.3%        +10   202.5%
  DualMA              9          +27     55.6%         +3     1.6%
  RSI-MR             62         -417     48.4%         -7   -23.7%
  TrendPB            43         -567     34.9%        -13   -32.2%
  QuietBrk           65         -848     29.2%        -13   -48.2%
  TOTAL             526        +1760
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           2193     530       1663          0        8       23.8%
  Breakout         5606    4619        212        775      460       74.2%
  QuietBrk         1551     542        952         57      105       28.2%
  TrendPB          4358     730       1747       1881       66       15.2%
  RSI-MR           1594     230        967        397       65       10.4%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 526  (202 winners / 324 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   44.9%   (price continued post-exit)
    False breakout rate  :   38.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.320      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.10%    +0.20%    -0.04%
    Losers       -0.12%    -0.35%    -0.50%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.118  (>0 = stable universe → better trades)
    Turnover vs success  : -0.047  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               14    21.4%    -2.44%
    HIGH_VOL_UPTREND               126    30.2%    -0.82%
    LOW_VOL_SIDEWAYS                63    50.8%     1.63%
    LOW_VOL_UPTREND                160    40.6%    -0.29%
    MID_VOL_SIDEWAYS                34    50.0%     0.39%
    MID_VOL_UPTREND                129    36.4%     0.03%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.35  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.05  Breakout=0.45  QuietBrk=0.35  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-02-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-03-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.30  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.10  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.30  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.10
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  Adaptive  (5-strat)      1.26    30.76%   10.56%    1.39  45.4%     1713
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1034       +18837     41.4%        +18    71.3%
  QuietBrk          217        +6494     40.1%        +30    24.6%
  TrendPB           114         +659     50.9%         +6     2.5%
  RSI-MR            326         +572     59.2%         +2     2.2%
  DualMA             22         -127     50.0%         -6    -0.5%
  TOTAL            1713       +26435
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          12844    1850      10987          7       29       14.2%
  Breakout        17049   14504        316       2229     1047       78.9%
  QuietBrk         5442    1614       3690        138      262       24.8%
  TrendPB         13451    1852       5933       5666       99       13.0%
  RSI-MR          10883    1170       6359       3354      334        7.7%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1713  (777 winners / 936 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.4%   (price continued post-exit)
    False breakout rate  :   32.2%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.210      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.05%    +0.36%    +0.70%
    Losers       +0.01%    +0.10%    +0.37%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.064  (>0 = stable universe → better trades)
    Turnover vs success  : -0.036  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               96    47.9%     0.05%
    HIGH_VOL_UPTREND               746    44.5%     0.55%
    LOW_VOL_SIDEWAYS               100    51.0%     1.67%
    LOW_VOL_UPTREND                340    43.5%     0.37%
    MID_VOL_SIDEWAYS                79    55.7%     0.56%
    MID_VOL_UPTREND                352    44.3%     1.06%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [ADAPTIVE_ONLY=1 — skipping solo strategies and EqualWeight]
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [RCAQualityGate] 2025-04-03 → Breakout WR 8.3% < 40% over last 12 trades — CB relaxation disabled
  [AdaptiveSelector] 2025-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-04-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-09-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-21 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-09-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BEAR_CONFIRMED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.15  Breakout=0.25  QuietBrk=0.25  TrendPB=0.20  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2025-12-21 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-12-28 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-04 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-11 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] 2026-01-18 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-01-26 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.20  RSI-MR=0.20
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-15 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-02-22 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2026-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.20  Breakout=0.20  QuietBrk=0.20  TrendPB=0.25  RSI-MR=0.15
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00  [NO-CLAMP]
  [AdaptiveSelector raw_llm] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  Adaptive  (5-strat)     -0.05    -0.55%    4.20%    0.97  36.7%      624
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           92        +1523     30.4%        +17  -275.2%
  RSI-MR            120         +390     50.8%         +3   -70.4%
  TrendPB            16         -201     43.8%        -13    36.2%
  DualMA             12         -668      8.3%        -56   120.7%
  Breakout          384        -1598     34.4%         -4   288.7%
  TOTAL             624         -554
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           4764    1414       3349          1       26       29.1%
  Breakout         5861    4272        866        723      455       65.1%
  QuietBrk         2078     627       1409         42      120       24.4%
  TrendPB          4463     714       2116       1633       31       15.3%
  RSI-MR           4033     592       2303       1138      270        8.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 624  (229 winners / 395 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.1%   (price continued post-exit)
    False breakout rate  :   27.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.327      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.06%    +0.00%    +0.24%
    Losers       +0.29%    +0.32%    +0.84%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.110  (>0 = stable universe → better trades)
    Turnover vs success  : +0.031  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               20    45.0%     0.11%
    HIGH_VOL_UPTREND               138    37.7%    -0.46%
    LOW_VOL_SIDEWAYS                79    34.2%    -0.04%
    LOW_VOL_UPTREND                191    35.6%    -0.38%
    MID_VOL_SIDEWAYS                30    30.0%    -1.52%
    MID_VOL_UPTREND                166    38.6%     0.05%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```


---

## Meta Recalibration Test — 2026-05-31 01:22

**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  
**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + `_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  
**Costs:** 0.10% commission + 0.05% slippage per side  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=0`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.10    -1.46%    8.43%    0.62  27.4%       84
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.27     2.77%   11.03%    1.03  39.8%      387
  QuietBrk 20d             0.47     5.34%   10.96%    0.95  35.8%      243
  TrendPB v2 pct=3%        0.39     2.79%    4.94%    1.14  54.5%      253
  TrendPB v2 pct=5%        0.90     4.51%    2.85%    1.43  57.3%      124
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.08    -1.18%   10.86%    0.98  54.8%      416
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.56    -3.69%    7.85%    0.83  41.7%      933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            315         +308     52.4%         +1    -6.8%
  TrendPB            55          +17     43.6%         +0    -0.4%
  DualMA             25        -1262     20.0%        -50    27.7%
  QuietBrk           88        -1717     25.0%        -20    37.7%
  Breakout          450        -1904     38.4%         -4    41.8%
  TOTAL             933        -4558
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6765    5405       1356          4       18       79.6%
  Breakout         7118    2058       3645       1415      187       26.3%
  QuietBrk         2052     412       1570         70       51       17.6%
  TrendPB          5897     541       2996       2360       32        8.6%
  RSI-MR           6588    1002       3917       1669      149       12.9%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             62   6.6%    43.5%       -2.3        -141
  strategy            871  93.4%    41.6%       -5.1       -4417

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.7%   95.3%    71.4%      36.8%    +43.6       -6.6
  DualMA        92.0%    8.0%    21.7%       0.0%    -49.4      -63.1
  QuietBrk      20.5%   79.5%    38.9%      21.4%     +4.4      -25.7
  RSI-MR         0.0%  100.0%     0.0%      52.4%     +0.0       +1.0
  TrendPB        0.0%  100.0%     0.0%      43.6%     +0.0       +0.3
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2019-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2019-01-21 → Breakout WR 18.8% < 40% over last 16 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-03 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-10 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2019-05-12 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-26 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-06-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-06-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2019-07-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  Adaptive  (5-strat)     -0.16    -2.04%    7.51%    0.87  41.2%      684
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            130         +542     55.4%         +4   -13.0%
  TrendPB            53         +173     50.9%         +3    -4.2%
  DualMA             11         -219     27.3%        -20     5.3%
  QuietBrk           76        -1221     28.9%        -16    29.3%
  Breakout          414        -3442     38.2%         -8    82.6%
  TOTAL             684        -4167
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3750    1151       2597          2        6       30.5%
  Breakout         6408    5025        358       1025      255       74.4%
  QuietBrk         1857     596       1219         42       70       28.3%
  TrendPB          5147     627       2380       2140       35       11.5%
  RSI-MR           3193     532       1967        694      175       11.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2019-01-21 → Breakout WR 18.8% < 40% over last 16 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.20     1.53%    7.18%    1.00  41.0%      744
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          421        +1922     37.8%         +5 11228.4%
  RSI-MR            168        +1271     56.0%         +8  7426.8%
  TrendPB            55         +416     47.3%         +8  2428.9%
  DualMA             22        -1384     22.7%        -63 -8081.6%
  QuietBrk           78        -2209     26.9%        -28 -12902.5%
  TOTAL             744          +17
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5859    4547       1309          3       15       77.4%
  Breakout         6398    2270       3076       1052      235       31.8%
  QuietBrk         1826     383       1402         41       56       17.9%
  TrendPB          5058     476       2492       2090       31        8.8%
  RSI-MR           4969     711       2944       1314      257        9.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  RCA delta              + 0.36  +   3.56%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2361  (976 winners / 1385 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.4%   (price continued post-exit)
    False breakout rate  :   36.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.250      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.05%    +0.06%    +0.13%
    Losers       -0.11%    -0.16%    -0.13%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.004  (>0 = stable universe → better trades)
    Turnover vs success  : +0.069  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              102    43.1%     1.00%
    HIGH_VOL_UPTREND               638    49.4%     0.82%
    LOW_VOL_SIDEWAYS               274    47.4%     0.03%
    LOW_VOL_UPTREND                592    33.4%    -0.89%
    MID_VOL_SIDEWAYS               142    51.4%    -0.74%
    MID_VOL_UPTREND                613    35.2%    -0.75%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.67    23.80%    9.00%    2.27  49.5%       93
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.72    29.08%    7.25%    1.49  41.3%      426
  QuietBrk 20d             1.95    31.64%   12.71%    1.70  39.0%      287
  TrendPB v2 pct=3%        1.62    19.51%    5.84%    1.53  60.9%      425
  TrendPB v2 pct=5%        1.83    16.68%    5.42%    1.78  62.8%      253
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.05    13.63%   10.08%    1.31  61.6%      435
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.53    27.91%    5.21%    1.98  50.1%      991

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17301     43.3%        +33    68.4%
  QuietBrk           99        +3216     40.4%        +32    12.7%
  RSI-MR            246        +2976     65.4%        +12    11.8%
  TrendPB           106        +1679     59.4%        +16     6.6%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             991       +25299
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8346    6692       1644         10       22       79.9%
  Breakout         8558    2359       4812       1387      261       24.5%
  QuietBrk         2698     501       2119         78       47       16.8%
  TrendPB          7116     579       2849       3688       72        7.1%
  RSI-MR           7514     728       4525       2261       98        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             97   9.8%    69.1%     +139.5      +13535
  strategy            894  90.2%    48.0%      +13.2      +11764

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       9.6%   90.4%    82.0%      39.1%   +181.8      +17.5
  DualMA        90.0%   10.0%    38.9%       0.0%    +18.4     -101.9
  QuietBrk      29.3%   70.7%    65.5%      30.0%   +141.9      -12.9
  RSI-MR         0.0%  100.0%     0.0%      65.4%     +0.0      +12.1
  TrendPB        0.0%  100.0%     0.0%      59.4%     +0.0      +15.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2020-02-23 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2020-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      2.33    33.17%    6.79%    1.88  45.8%      823
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          506       +24976     41.9%        +49    82.3%
  QuietBrk           96        +3973     36.5%        +41    13.1%
  TrendPB            98        +1301     59.2%        +13     4.3%
  RSI-MR            114         +105     60.5%         +1     0.3%
  DualMA              9           -5     33.3%         -1    -0.0%
  TOTAL             823       +30351
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7031    1401       5622          8       14       19.7%
  Breakout         7879    6800         82        997      342       82.0%
  QuietBrk         2505     651       1793         61       57       23.7%
  TrendPB          6433     575       2321       3537       83        7.6%
  RSI-MR           5764     470       3467       1827      171        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.46    32.33%    6.17%    1.96  47.1%      870
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          516       +24590     43.4%        +48    81.9%
  QuietBrk          100        +2939     39.0%        +29     9.8%
  TrendPB           111        +2292     59.5%        +21     7.6%
  DualMA             21         +222     38.1%        +11     0.7%
  RSI-MR            122          -31     59.8%         -0    -0.1%
  TOTAL             870       +30013
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7749    5085       2656          8        9       65.5%
  Breakout         8230    3670       3442       1118      267       41.3%
  QuietBrk         2651     502       2090         59       51       17.0%
  TrendPB          6759     567       2525       3667       46        7.7%
  RSI-MR           6440     488       3902       2050      173        4.9%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  RCA delta              + 0.13    -0.84%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2684  (1283 winners / 1401 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.4%   (price continued post-exit)
    False breakout rate  :   37.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.147      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.11%    +0.87%    +1.26%
    Losers       -0.03%    +0.57%    +0.86%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.048  (>0 = stable universe → better trades)
    Turnover vs success  : +0.060  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               74    54.1%    -0.47%
    HIGH_VOL_UPTREND               932    43.6%     1.34%
    LOW_VOL_SIDEWAYS               241    65.6%     4.74%
    LOW_VOL_UPTREND                663    47.4%     1.51%
    MID_VOL_SIDEWAYS               112    71.4%     3.21%
    MID_VOL_UPTREND                662    43.1%     1.75%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.87    51.22%    9.01%    2.40  52.7%      169
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.62   105.97%   11.72%    1.79  44.6%      822
  QuietBrk 20d             2.42    92.87%   14.52%    1.91  43.6%      546
  TrendPB v2 pct=3%        1.24    29.13%    9.93%    1.36  60.2%      782
  TrendPB v2 pct=5%        1.30    23.55%    6.96%    1.49  60.9%      460
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.31    32.35%    7.52%    1.34  58.8%      873
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    3.00    68.25%    6.28%    2.12  51.3%     1985

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1036       +44120     46.3%        +43    65.0%
  QuietBrk          192       +11193     44.8%        +58    16.5%
  RSI-MR            503        +6718     60.6%        +13     9.9%
  DualMA             41        +3873     53.7%        +94     5.7%
  TrendPB           213        +1966     59.2%         +9     2.9%
  TOTAL            1985       +67869
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16452   13264       3164         24       29       80.4%
  Breakout        17177    4707       9629       2841      439       24.8%
  QuietBrk         5273     945       4150        178       99       16.0%
  TrendPB         14309    1152       6003       7154      113        7.3%
  RSI-MR          15042    1436       9119       4487      176        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            186   9.4%    74.2%     +216.7      +40306
  strategy           1799  90.6%    49.0%      +15.3      +27564

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       8.9%   91.1%    81.5%      42.9%   +268.5      +20.6
  DualMA        90.2%    9.8%    56.8%      25.0%   +110.7      -56.1
  QuietBrk      29.7%   70.3%    73.7%      32.6%   +201.9       -2.3
  RSI-MR         0.0%  100.0%     0.0%      60.6%     +0.0      +13.4
  TrendPB        0.0%  100.0%     0.0%      59.2%     +0.0       +9.2
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [RCAQualityGate] 2020-06-10 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-05-02 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-05-09 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  Adaptive  (5-strat)      2.81    85.60%    8.94%    2.02  49.3%     1711
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1050       +72349     46.7%        +69    85.3%
  QuietBrk          175        +8911     38.9%        +51    10.5%
  TrendPB           203        +1585     59.1%         +8     1.9%
  DualMA             19        +1226     42.1%        +65     1.4%
  RSI-MR            264         +774     59.5%         +3     0.9%
  TOTAL            1711       +84845
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15465    3222      12228         15       20       20.7%
  Breakout        15737   13426        323       1988      537       81.9%
  QuietBrk         4730    1235       3354        141      131       23.3%
  TrendPB         12778     941       4944       6893      119        6.4%
  RSI-MR          13308    1150       7959       4199      483        5.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-06-10 → Breakout WR 16.7% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   3.02    85.05%    6.94%    2.16  49.7%     1788
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1069       +65666     46.2%        +61    77.7%
  QuietBrk          185       +10735     42.7%        +58    12.7%
  DualMA             43        +5103     53.5%       +119     6.0%
  TrendPB           232        +2130     59.5%         +9     2.5%
  RSI-MR            259         +909     59.5%         +4     1.1%
  TOTAL            1788       +84544
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16273   10820       5433         20       23       66.3%
  Breakout        16719    7062       7432       2225      396       39.9%
  QuietBrk         5128     926       4055        147      103       16.0%
  TrendPB         13816    1008       5557       7251       84        6.7%
  RSI-MR          14413    1120       8672       4621      469        4.5%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  RCA delta              + 0.21    -0.54%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5484  (2750 winners / 2734 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.4%   (price continued post-exit)
    False breakout rate  :   35.0%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.122      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.08%    +0.74%    +1.17%
    Losers       -0.11%    +0.34%    +0.71%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.000  (>0 = stable universe → better trades)
    Turnover vs success  : -0.020  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              300    53.0%     0.58%
    HIGH_VOL_UPTREND              2553    48.4%     1.87%
    LOW_VOL_SIDEWAYS               264    65.2%     5.51%
    LOW_VOL_UPTREND                810    49.8%     1.86%
    MID_VOL_SIDEWAYS               297    61.6%     2.95%
    MID_VOL_UPTREND               1260    47.5%     2.14%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.20    -2.29%   10.37%    0.88  38.3%       81
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.26     2.42%   11.98%    1.06  41.7%      343
  QuietBrk 20d            -0.22    -3.81%   16.98%    0.90  37.3%      220
  TrendPB v2 pct=3%       -1.09   -10.64%   12.14%    0.71  52.3%      241
  TrendPB v2 pct=5%       -0.40    -2.48%    5.86%    0.87  50.0%      116
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.97   -12.12%   15.78%    0.72  48.5%      344
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    0.05     0.07%    7.67%    1.00  40.7%      703

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +2360     38.8%         +6  4016.7%
  DualMA             28         +177     50.0%         +6   301.3%
  TrendPB            50          -89     46.0%         -2  -151.7%
  QuietBrk           72         -895     26.4%        -12 -1523.4%
  RSI-MR            177        -1494     47.5%         -8 -2543.0%
  TOTAL             703          +59
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5822    4523       1297          2       27       77.2%
  Breakout         6042    2093       2989        960      396       28.1%
  QuietBrk         1664     379       1214         71       79       18.0%
  TrendPB          4774     396       2371       2007       63        7.0%
  RSI-MR           5304     741       3075       1488      244        9.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             64   9.1%    56.2%      +59.4       +3804
  strategy            639  90.9%    39.1%       -5.9       -3745

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.3%   95.7%    81.2%      36.9%   +174.6       -1.2
  DualMA        96.4%    3.6%    48.1%     100.0%     +6.1      +13.1
  QuietBrk      29.2%   70.8%    47.6%      17.6%    +40.3      -34.1
  RSI-MR         0.0%  100.0%     0.0%      47.5%     +0.0       -8.4
  TrendPB        0.0%  100.0%     0.0%      46.0%     +0.0       -1.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      0.22     1.53%    9.89%    1.06  38.4%      529
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +3291     38.3%         +9   210.7%
  RSI-MR             37         +273     56.8%         +7    17.5%
  TrendPB            44          -97     43.2%         -2    -6.2%
  DualMA              9         -154     44.4%        -17    -9.8%
  QuietBrk           63        -1752     23.8%        -28  -112.2%
  TOTAL             529        +1562
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           2882     808       2073          1       14       27.6%
  Breakout         5494    4740        212        542      430       78.4%
  QuietBrk         1481     493        940         48      101       26.5%
  TrendPB          4052     433       1694       1925       69        9.0%
  RSI-MR           1872     254       1133        485      156        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.14     0.94%   14.84%    1.03  38.1%      509
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          361        +6671     38.8%        +18   694.4%
  TrendPB            42         +278     47.6%         +7    28.9%
  DualMA             11         -291     45.5%        -26   -30.3%
  QuietBrk           49         -659     26.5%        -13   -68.6%
  RSI-MR             46        -5039     34.8%       -110  -524.5%
  TOTAL             509         +961
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3967    1535       2431          1       12       38.4%
  Breakout         5260    3980        716        564      452       67.1%
  QuietBrk         1232     315        882         35      101       17.4%
  TrendPB          3518     387       1389       1742       44        9.7%
  RSI-MR           1465     287        843        335      103       12.6%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              -0.07    -0.59%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1741  (683 winners / 1058 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   46.9%   (price continued post-exit)
    False breakout rate  :   37.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.297      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.11%    +0.23%    +0.30%
    Losers       -0.15%    -0.20%    -0.50%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.121  (>0 = stable universe → better trades)
    Turnover vs success  : -0.009  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               50    34.0%    -1.83%
    HIGH_VOL_UPTREND               398    36.2%    -0.27%
    LOW_VOL_SIDEWAYS               215    51.2%     1.69%
    LOW_VOL_UPTREND                511    38.0%    -0.27%
    MID_VOL_SIDEWAYS               130    43.1%    -0.39%
    MID_VOL_UPTREND                437    37.1%    -0.04%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.49    10.25%   11.79%    1.16  40.5%      205
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.80    26.11%   13.00%    1.19  41.1%      894
  QuietBrk 20d             0.65    20.36%   18.27%    1.18  40.7%      573
  TrendPB v2 pct=3%        0.33     6.01%   15.19%    1.11  57.4%      563
  TrendPB v2 pct=5%        0.87    11.19%    7.31%    1.40  59.8%      266
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.28    -9.19%   18.38%    0.91  52.9%      908
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.13    22.42%    7.67%    1.35  45.5%     1933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1049       +15242     41.8%        +15    77.0%
  QuietBrk          229        +1888     33.2%         +8     9.5%
  TrendPB           117        +1233     56.4%        +11     6.2%
  DualMA             61        +1069     52.5%        +18     5.4%
  RSI-MR            477         +359     55.8%         +1     1.8%
  TOTAL            1933       +19792
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17391   13788       3595          8       67       78.9%
  Breakout        17847    5426       9817       2604      963       25.0%
  QuietBrk         5465    1171       4139        155      235       17.1%
  TrendPB         14233     882       7647       5704      101        5.5%
  RSI-MR          15500    1793       9008       4699      539        8.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            190   9.8%    63.7%      +95.0      +18058
  strategy           1743  90.2%    43.5%       +1.0       +1734

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       6.9%   93.1%    73.6%      39.5%   +154.5       +4.2
  DualMA        86.9%   13.1%    54.7%      37.5%    +22.4      -14.9
  QuietBrk      28.4%   71.6%    60.0%      22.6%    +88.4      -23.5
  RSI-MR         0.0%  100.0%     0.0%      55.8%     +0.0       +0.8
  TrendPB        0.0%  100.0%     0.0%      56.4%     +0.0      +10.5
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-01-22 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-01-29 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-02-19 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-02-26 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-03-12 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      1.54    41.78%    9.89%    1.48  45.0%     1540
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1020       +27377     41.9%        +27    76.7%
  QuietBrk          212        +6108     37.7%        +29    17.1%
  TrendPB           112        +1255     56.2%        +11     3.5%
  RSI-MR            172         +674     65.1%         +4     1.9%
  DualMA             24         +274     45.8%        +11     0.8%
  TOTAL            1540       +35689
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          13411    2706      10698          7       42       19.9%
  Breakout        16233   14320        314       1599     1074       81.6%
  QuietBrk         5362    1602       3665         95      273       24.8%
  TrendPB         12474     783       5964       5727      109        5.4%
  RSI-MR          10351    1029       5985       3337      602        4.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.13    28.22%   14.84%    1.34  43.5%     1569
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1049       +22171     40.5%        +21    93.2%
  QuietBrk          198        +4969     36.9%        +25    20.9%
  TrendPB           109        +1964     58.7%        +18     8.3%
  DualMA             41         -632     43.9%        -15    -2.7%
  RSI-MR            172        -4694     59.3%        -27   -19.7%
  TOTAL            1569       +23777
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15143    9879       5256          8       45       64.9%
  Breakout        16432    7931       6817       1684     1018       42.1%
  QuietBrk         5052    1087       3876         89      258       16.4%
  TrendPB         12276     749       5988       5539       81        5.4%
  RSI-MR          10292    1036       5944       3312      543        4.8%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.41   -13.56%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5042  (2254 winners / 2788 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.6%   (price continued post-exit)
    False breakout rate  :   32.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.216      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.01%    +0.41%    +0.83%
    Losers       -0.05%    +0.07%    +0.24%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.061  (>0 = stable universe → better trades)
    Turnover vs success  : -0.015  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              234    50.0%     0.28%
    HIGH_VOL_UPTREND              2126    45.0%     0.69%
    LOW_VOL_SIDEWAYS               338    48.8%     1.42%
    LOW_VOL_UPTREND               1027    42.4%     0.56%
    MID_VOL_SIDEWAYS               250    50.4%     0.24%
    MID_VOL_UPTREND               1067    42.5%     1.02%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.00    -0.55%    7.80%    0.98  33.7%      104
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.69   -10.61%   12.90%    0.80  37.4%      409
  QuietBrk 20d             0.05    -0.27%    8.43%    0.99  38.8%      263
  TrendPB v2 pct=3%        0.23     1.50%    3.84%    1.09  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.36     3.82%    5.86%    1.10  53.6%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.62    -3.56%    4.31%    0.81  37.1%      647

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           87         +365     31.0%         +4   -10.3%
  TrendPB            18          -37     50.0%         -2     1.0%
  RSI-MR            164         -329     50.6%         -2     9.2%
  DualMA             14         -751     14.3%        -54    21.1%
  Breakout          364        -2809     32.7%         -8    78.9%
  TOTAL             647        -3561
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5807    4437       1368          2       41       75.7%
  Breakout         5694    1949       2960        785      484       25.7%
  QuietBrk         1996     474       1473         49      134       17.0%
  TrendPB          4297     237       2582       1478       30        4.8%
  RSI-MR           4908     758       2820       1330      302        9.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             39   6.0%    51.3%      +25.5        +995
  strategy            608  94.0%    36.2%       -7.5       -4556

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       3.3%   96.7%    58.3%      31.8%    +35.8       -9.2
  DualMA        85.7%   14.3%    16.7%       0.0%    -54.2      -50.2
  QuietBrk      17.2%   82.8%    73.3%      22.2%    +81.1      -11.8
  RSI-MR         0.0%  100.0%     0.0%      50.6%     +0.0       -2.0
  TrendPB        0.0%  100.0%     0.0%      50.0%     +0.0       -2.0
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2025-03-31 [BULL_MEDVOL/MEDIUM] → DualMA=0.05  Breakout=0.45  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [RCAQualityGate] 2025-04-01 → Breakout WR 9.1% < 40% over last 11 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-06 [BULL_MEDVOL/MEDIUM] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-14 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.20  Breakout=0.45  QuietBrk=0.20  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  Adaptive  (5-strat)     -0.45    -4.04%    6.33%    0.85  33.9%      528
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           95        +1251     30.5%        +13   -31.7%
  RSI-MR             42           -5     40.5%         -0     0.1%
  TrendPB            15           -8     46.7%         -1     0.2%
  DualMA              4          -44     25.0%        -11     1.1%
  Breakout          372        -5133     33.6%        -14   130.3%
  TOTAL             528        -3940
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3649     728       2921          0       20       19.4%
  Breakout         5534    4984         17        533      490       81.2%
  QuietBrk         2066     692       1342         32      129       27.3%
  TrendPB          3992     185       2240       1567       33        3.8%
  RSI-MR           2424     345       1437        642      232        4.7%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2025-04-01 → Breakout WR 8.3% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.38    -3.27%    5.94%    0.87  35.5%      563
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           82        +1207     35.4%        +15   -36.9%
  RSI-MR             58         +670     51.7%        +12   -20.5%
  TrendPB            17          -75     47.1%         -4     2.3%
  DualMA             13         -488     30.8%        -38    14.9%
  Breakout          393        -4590     32.8%        -12   140.2%
  TOTAL             563        -3274
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5365    3098       2266          1       24       57.3%
  Breakout         5686    3197       1914        575      450       48.3%
  QuietBrk         1902     441       1427         34      125       16.6%
  TrendPB          4010     254       2231       1525       23        5.8%
  RSI-MR           3142     399       1830        913      250        4.7%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              + 0.07  +   0.77%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1738  (619 winners / 1119 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.1%   (price continued post-exit)
    False breakout rate  :   28.5%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.345      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.04%    +0.02%    +0.21%
    Losers       +0.29%    +0.27%    +0.74%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.113  (>0 = stable universe → better trades)
    Turnover vs success  : -0.008  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               44    40.9%    -0.06%
    HIGH_VOL_UPTREND               378    39.4%    -0.23%
    LOW_VOL_SIDEWAYS               198    30.3%    -0.25%
    LOW_VOL_UPTREND                556    34.2%    -0.47%
    MID_VOL_SIDEWAYS                91    33.0%    -1.58%
    MID_VOL_UPTREND                471    36.5%    -0.08%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```


---

## Meta Recalibration Test — 2026-06-02 09:46

**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  
**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + `_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  
**Costs:** 0.10% commission + 0.05% slippage per side  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=0`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.10    -1.46%    8.43%    0.62  27.4%       84
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.27     2.77%   11.03%    1.03  39.8%      387
  QuietBrk 20d             0.47     5.34%   10.96%    0.95  35.8%      243
  TrendPB v2 pct=3%        0.39     2.79%    4.94%    1.14  54.5%      253
  TrendPB v2 pct=5%        0.90     4.51%    2.85%    1.43  57.3%      124
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.08    -1.18%   10.86%    0.98  54.8%      416
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.56    -3.69%    7.85%    0.83  41.7%      933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            315         +308     52.4%         +1    -6.8%
  TrendPB            55          +17     43.6%         +0    -0.4%
  DualMA             25        -1262     20.0%        -50    27.7%
  QuietBrk           88        -1717     25.0%        -20    37.7%
  Breakout          450        -1904     38.4%         -4    41.8%
  TOTAL             933        -4558
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6765    5405       1356          4       18       79.6%
  Breakout         7118    2058       3645       1415      187       26.3%
  QuietBrk         2052     412       1570         70       51       17.6%
  TrendPB          5897     541       2996       2360       32        8.6%
  RSI-MR           6588    1002       3917       1669      149       12.9%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             62   6.6%    43.5%       -2.3        -141
  strategy            871  93.4%    41.6%       -5.1       -4417

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.7%   95.3%    71.4%      36.8%    +43.6       -6.6
  DualMA        92.0%    8.0%    21.7%       0.0%    -49.4      -63.1
  QuietBrk      20.5%   79.5%    38.9%      21.4%     +4.4      -25.7
  RSI-MR         0.0%  100.0%     0.0%      52.4%     +0.0       +1.0
  TrendPB        0.0%  100.0%     0.0%      43.6%     +0.0       +0.3
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2019-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2019-01-21 → Breakout WR 18.8% < 40% over last 16 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-03 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-10 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2019-05-12 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-26 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-06-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-06-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2019-07-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  Adaptive  (5-strat)     -0.16    -2.04%    7.51%    0.87  41.2%      684
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            130         +542     55.4%         +4   -13.0%
  TrendPB            53         +173     50.9%         +3    -4.2%
  DualMA             11         -219     27.3%        -20     5.3%
  QuietBrk           76        -1221     28.9%        -16    29.3%
  Breakout          414        -3442     38.2%         -8    82.6%
  TOTAL             684        -4167
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3750    1151       2597          2        6       30.5%
  Breakout         6408    5025        358       1025      255       74.4%
  QuietBrk         1857     596       1219         42       70       28.3%
  TrendPB          5147     627       2380       2140       35       11.5%
  RSI-MR           3193     532       1967        694      175       11.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2019-01-21 → Breakout WR 21.4% < 40% over last 14 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.41    -2.87%    7.85%    0.86  41.9%      943
                         (LLM calls: 0)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            315         +290     52.4%         +1    -7.8%
  TrendPB            55          +25     43.6%         +0    -0.7%
  DualMA             26         -977     23.1%        -38    26.1%
  QuietBrk           91        -1403     26.4%        -15    37.5%
  Breakout          456        -1674     38.6%         -4    44.8%
  TOTAL             943        -3738
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6861    5506       1351          4       17       80.0%
  Breakout         7258    2089       3740       1429      171       26.4%
  QuietBrk         2140     427       1642         71       47       17.8%
  TrendPB          6040     541       3060       2439       32        8.4%
  RSI-MR           6731    1002       3996       1733      148       12.7%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  RCA delta              -0.25    -0.83%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2560  (1066 winners / 1494 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   48.5%   (price continued post-exit)
    False breakout rate  :   36.9%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.243      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.02%    +0.11%    +0.23%
    Losers       -0.11%    -0.12%    -0.04%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.017  (>0 = stable universe → better trades)
    Turnover vs success  : +0.055  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              126    45.2%     0.99%
    HIGH_VOL_UPTREND               700    49.3%     0.76%
    LOW_VOL_SIDEWAYS               307    46.6%    -0.22%
    LOW_VOL_UPTREND                623    34.2%    -0.82%
    MID_VOL_SIDEWAYS               161    52.2%    -0.74%
    MID_VOL_UPTREND                643    34.8%    -0.72%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.67    23.80%    9.00%    2.27  49.5%       93
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.72    29.08%    7.25%    1.49  41.3%      426
  QuietBrk 20d             1.95    31.64%   12.71%    1.70  39.0%      287
  TrendPB v2 pct=3%        1.62    19.51%    5.84%    1.53  60.9%      425
  TrendPB v2 pct=5%        1.83    16.68%    5.42%    1.78  62.8%      253
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.05    13.63%   10.08%    1.31  61.6%      435
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.53    27.91%    5.21%    1.98  50.1%      991

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17301     43.3%        +33    68.4%
  QuietBrk           99        +3216     40.4%        +32    12.7%
  RSI-MR            246        +2976     65.4%        +12    11.8%
  TrendPB           106        +1679     59.4%        +16     6.6%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             991       +25299
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8346    6692       1644         10       22       79.9%
  Breakout         8558    2359       4812       1387      261       24.5%
  QuietBrk         2698     501       2119         78       47       16.8%
  TrendPB          7116     579       2849       3688       72        7.1%
  RSI-MR           7514     728       4525       2261       98        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             97   9.8%    69.1%     +139.5      +13535
  strategy            894  90.2%    48.0%      +13.2      +11764

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       9.6%   90.4%    82.0%      39.1%   +181.8      +17.5
  DualMA        90.0%   10.0%    38.9%       0.0%    +18.4     -101.9
  QuietBrk      29.3%   70.7%    65.5%      30.0%   +141.9      -12.9
  RSI-MR         0.0%  100.0%     0.0%      65.4%     +0.0      +12.1
  TrendPB        0.0%  100.0%     0.0%      59.4%     +0.0      +15.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2020-02-23 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2020-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      2.33    33.17%    6.79%    1.88  45.8%      823
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          506       +24976     41.9%        +49    82.3%
  QuietBrk           96        +3973     36.5%        +41    13.1%
  TrendPB            98        +1301     59.2%        +13     4.3%
  RSI-MR            114         +105     60.5%         +1     0.3%
  DualMA              9           -5     33.3%         -1    -0.0%
  TOTAL             823       +30351
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7031    1401       5622          8       14       19.7%
  Breakout         7879    6800         82        997      342       82.0%
  QuietBrk         2505     651       1793         61       57       23.7%
  TrendPB          6433     575       2321       3537       83        7.6%
  RSI-MR           5764     470       3467       1827      171        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.53    27.91%    5.21%    1.98  50.1%      991
                         (LLM calls: 0)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17301     43.3%        +33    68.4%
  QuietBrk           99        +3216     40.4%        +32    12.7%
  RSI-MR            246        +2976     65.4%        +12    11.8%
  TrendPB           106        +1679     59.4%        +16     6.6%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             991       +25299
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8346    6692       1644         10       22       79.9%
  Breakout         8558    2359       4812       1387      261       24.5%
  QuietBrk         2698     501       2119         78       47       16.8%
  TrendPB          7116     579       2849       3688       72        7.1%
  RSI-MR           7514     728       4525       2261       98        8.4%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  RCA delta              + 0.21    -5.26%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2805  (1369 winners / 1436 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.4%   (price continued post-exit)
    False breakout rate  :   37.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.134      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.13%    +0.90%    +1.28%
    Losers       -0.03%    +0.56%    +0.87%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.048  (>0 = stable universe → better trades)
    Turnover vs success  : +0.061  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               93    58.1%     0.25%
    HIGH_VOL_UPTREND               958    44.7%     1.39%
    LOW_VOL_SIDEWAYS               257    65.0%     4.63%
    LOW_VOL_UPTREND                687    47.6%     1.48%
    MID_VOL_SIDEWAYS               128    71.1%     2.89%
    MID_VOL_UPTREND                682    44.3%     1.69%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.87    51.22%    9.01%    2.40  52.7%      169
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.62   105.97%   11.72%    1.79  44.6%      822
  QuietBrk 20d             2.42    92.87%   14.52%    1.91  43.6%      546
  TrendPB v2 pct=3%        1.24    29.13%    9.93%    1.36  60.2%      782
  TrendPB v2 pct=5%        1.30    23.55%    6.96%    1.49  60.9%      460
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.31    32.35%    7.52%    1.34  58.8%      873
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    3.00    68.25%    6.28%    2.12  51.3%     1985

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1036       +44120     46.3%        +43    65.0%
  QuietBrk          192       +11193     44.8%        +58    16.5%
  RSI-MR            503        +6718     60.6%        +13     9.9%
  DualMA             41        +3873     53.7%        +94     5.7%
  TrendPB           213        +1966     59.2%         +9     2.9%
  TOTAL            1985       +67869
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16452   13264       3164         24       29       80.4%
  Breakout        17177    4707       9629       2841      439       24.8%
  QuietBrk         5273     945       4150        178       99       16.0%
  TrendPB         14309    1152       6003       7154      113        7.3%
  RSI-MR          15042    1436       9119       4487      176        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            186   9.4%    74.2%     +216.7      +40306
  strategy           1799  90.6%    49.0%      +15.3      +27564

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       8.9%   91.1%    81.5%      42.9%   +268.5      +20.6
  DualMA        90.2%    9.8%    56.8%      25.0%   +110.7      -56.1
  QuietBrk      29.7%   70.3%    73.7%      32.6%   +201.9       -2.3
  RSI-MR         0.0%  100.0%     0.0%      60.6%     +0.0      +13.4
  TrendPB        0.0%  100.0%     0.0%      59.2%     +0.0       +9.2
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [RCAQualityGate] 2020-06-10 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-05-02 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-05-09 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  Adaptive  (5-strat)      2.81    85.60%    8.94%    2.02  49.3%     1711
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1050       +72349     46.7%        +69    85.3%
  QuietBrk          175        +8911     38.9%        +51    10.5%
  TrendPB           203        +1585     59.1%         +8     1.9%
  DualMA             19        +1226     42.1%        +65     1.4%
  RSI-MR            264         +774     59.5%         +3     0.9%
  TOTAL            1711       +84845
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15465    3222      12228         15       20       20.7%
  Breakout        15737   13426        323       1988      537       81.9%
  QuietBrk         4730    1235       3354        141      131       23.3%
  TrendPB         12778     941       4944       6893      119        6.4%
  RSI-MR          13308    1150       7959       4199      483        5.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-06-10 → Breakout WR 16.7% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.87    89.03%    8.84%    2.04  49.2%     1713
                         (LLM calls: 15)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1047       +76606     46.4%        +73    86.8%
  QuietBrk          174        +8792     40.2%        +51    10.0%
  TrendPB           202        +1458     59.4%         +7     1.7%
  RSI-MR            272         +803     58.5%         +3     0.9%
  DualMA             18         +569     44.4%        +32     0.6%
  TOTAL            1713       +88229
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15523    3081      12427         15       22       19.7%
  Breakout        15806   13626        162       2018      528       82.9%
  QuietBrk         4768    1234       3396        138      126       23.2%
  TrendPB         12855     935       5009       6911      121        6.3%
  RSI-MR          13508    1170       8057       4281      484        5.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  RCA delta              + 0.06  +   3.43%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5409  (2705 winners / 2704 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.3%   (price continued post-exit)
    False breakout rate  :   35.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.123      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.07%    +0.75%    +1.16%
    Losers       -0.11%    +0.34%    +0.71%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.003  (>0 = stable universe → better trades)
    Turnover vs success  : -0.023  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              297    53.2%     0.59%
    HIGH_VOL_UPTREND              2522    48.3%     1.87%
    LOW_VOL_SIDEWAYS               252    65.9%     5.60%
    LOW_VOL_UPTREND                791    50.2%     1.87%
    MID_VOL_SIDEWAYS               295    61.0%     2.93%
    MID_VOL_UPTREND               1252    46.8%     1.93%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.20    -2.29%   10.37%    0.88  38.3%       81
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.26     2.42%   11.98%    1.06  41.7%      343
  QuietBrk 20d            -0.22    -3.81%   16.98%    0.90  37.3%      220
  TrendPB v2 pct=3%       -1.09   -10.64%   12.14%    0.71  52.3%      241
  TrendPB v2 pct=5%       -0.40    -2.48%    5.86%    0.87  50.0%      116
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.97   -12.12%   15.78%    0.72  48.5%      344
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    0.05     0.07%    7.67%    1.00  40.7%      703

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +2360     38.8%         +6  4016.7%
  DualMA             28         +177     50.0%         +6   301.3%
  TrendPB            50          -89     46.0%         -2  -151.7%
  QuietBrk           72         -895     26.4%        -12 -1523.4%
  RSI-MR            177        -1494     47.5%         -8 -2543.0%
  TOTAL             703          +59
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5822    4523       1297          2       27       77.2%
  Breakout         6042    2093       2989        960      396       28.1%
  QuietBrk         1664     379       1214         71       79       18.0%
  TrendPB          4774     396       2371       2007       63        7.0%
  RSI-MR           5304     741       3075       1488      244        9.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             64   9.1%    56.2%      +59.4       +3804
  strategy            639  90.9%    39.1%       -5.9       -3745

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.3%   95.7%    81.2%      36.9%   +174.6       -1.2
  DualMA        96.4%    3.6%    48.1%     100.0%     +6.1      +13.1
  QuietBrk      29.2%   70.8%    47.6%      17.6%    +40.3      -34.1
  RSI-MR         0.0%  100.0%     0.0%      47.5%     +0.0       -8.4
  TrendPB        0.0%  100.0%     0.0%      46.0%     +0.0       -1.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      0.22     1.53%    9.89%    1.06  38.4%      529
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +3291     38.3%         +9   210.7%
  RSI-MR             37         +273     56.8%         +7    17.5%
  TrendPB            44          -97     43.2%         -2    -6.2%
  DualMA              9         -154     44.4%        -17    -9.8%
  QuietBrk           63        -1752     23.8%        -28  -112.2%
  TOTAL             529        +1562
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           2882     808       2073          1       14       27.6%
  Breakout         5494    4740        212        542      430       78.4%
  QuietBrk         1481     493        940         48      101       26.5%
  TrendPB          4052     433       1694       1925       69        9.0%
  RSI-MR           1872     254       1133        485      156        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.26     1.59%    7.50%    1.08  40.4%      654
                         (LLM calls: 2)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          380        +2980     38.9%         +8   186.3%
  TrendPB            52          +61     46.2%         +1     3.8%
  DualMA             25          +32     52.0%         +1     2.0%
  RSI-MR            123         -317     48.0%         -3   -19.8%
  QuietBrk           74        -1156     27.0%        -16   -72.3%
  TOTAL             654        +1599
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5725    4453       1270          2       29       77.3%
  Breakout         5927    2107       2993        827      383       29.1%
  QuietBrk         1703     390       1253         60       77       18.4%
  TrendPB          4662     358       2259       2045       56        6.5%
  RSI-MR           5037     641       2933       1463      302        6.7%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              + 0.04  +   0.06%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1886  (753 winners / 1133 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.0%   (price continued post-exit)
    False breakout rate  :   37.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.285      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.04%    +0.15%    +0.28%
    Losers       -0.18%    -0.20%    -0.48%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.085  (>0 = stable universe → better trades)
    Turnover vs success  : -0.003  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               55    34.5%    -1.87%
    HIGH_VOL_UPTREND               416    37.5%    -0.16%
    LOW_VOL_SIDEWAYS               250    52.0%     1.55%
    LOW_VOL_UPTREND                563    37.8%    -0.32%
    MID_VOL_SIDEWAYS               147    41.5%    -0.44%
    MID_VOL_UPTREND                455    38.2%     0.16%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.49    10.25%   11.79%    1.16  40.5%      205
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.80    26.11%   13.00%    1.19  41.1%      894
  QuietBrk 20d             0.65    20.36%   18.27%    1.18  40.7%      573
  TrendPB v2 pct=3%        0.33     6.01%   15.19%    1.11  57.4%      563
  TrendPB v2 pct=5%        0.87    11.19%    7.31%    1.40  59.8%      266
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.28    -9.19%   18.38%    0.91  52.9%      908
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.13    22.42%    7.67%    1.35  45.5%     1933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1049       +15242     41.8%        +15    77.0%
  QuietBrk          229        +1888     33.2%         +8     9.5%
  TrendPB           117        +1233     56.4%        +11     6.2%
  DualMA             61        +1069     52.5%        +18     5.4%
  RSI-MR            477         +359     55.8%         +1     1.8%
  TOTAL            1933       +19792
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17391   13788       3595          8       67       78.9%
  Breakout        17847    5426       9817       2604      963       25.0%
  QuietBrk         5465    1171       4139        155      235       17.1%
  TrendPB         14233     882       7647       5704      101        5.5%
  RSI-MR          15500    1793       9008       4699      539        8.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            190   9.8%    63.7%      +95.0      +18058
  strategy           1743  90.2%    43.5%       +1.0       +1734

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       6.9%   93.1%    73.6%      39.5%   +154.5       +4.2
  DualMA        86.9%   13.1%    54.7%      37.5%    +22.4      -14.9
  QuietBrk      28.4%   71.6%    60.0%      22.6%    +88.4      -23.5
  RSI-MR         0.0%  100.0%     0.0%      55.8%     +0.0       +0.8
  TrendPB        0.0%  100.0%     0.0%      56.4%     +0.0      +10.5
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-01-22 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-01-29 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-02-19 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-02-26 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-03-12 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      1.54    41.78%    9.89%    1.48  45.0%     1540
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1020       +27377     41.9%        +27    76.7%
  QuietBrk          212        +6108     37.7%        +29    17.1%
  TrendPB           112        +1255     56.2%        +11     3.5%
  RSI-MR            172         +674     65.1%         +4     1.9%
  DualMA             24         +274     45.8%        +11     0.8%
  TOTAL            1540       +35689
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          13411    2706      10698          7       42       19.9%
  Breakout        16233   14320        314       1599     1074       81.6%
  QuietBrk         5362    1602       3665         95      273       24.8%
  TrendPB         12474     783       5964       5727      109        5.4%
  RSI-MR          10351    1029       5985       3337      602        4.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.33    27.91%    7.50%    1.42  44.9%     1806
                         (LLM calls: 2)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1076       +17250     40.9%        +16    71.7%
  QuietBrk          229        +3230     35.4%        +14    13.4%
  TrendPB           119        +1740     56.3%        +15     7.2%
  DualMA             56        +1218     55.4%        +22     5.1%
  RSI-MR            326         +613     58.6%         +2     2.5%
  TOTAL            1806       +24051
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17267   13722       3536          9       71       79.1%
  Breakout        17611    5486       9911       2214      923       25.9%
  QuietBrk         5551    1171       4252        128      221       17.1%
  TrendPB         13973     745       7394       5834       93        4.7%
  RSI-MR          15032    1567       8726       4739      729        5.6%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.21   -13.87%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5279  (2382 winners / 2897 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.7%   (price continued post-exit)
    False breakout rate  :   32.4%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.208      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.02%    +0.39%    +0.83%
    Losers       -0.05%    +0.08%    +0.25%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.044  (>0 = stable universe → better trades)
    Turnover vs success  : -0.014  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              256    50.4%     0.16%
    HIGH_VOL_UPTREND              2182    45.7%     0.70%
    LOW_VOL_SIDEWAYS               375    49.3%     1.25%
    LOW_VOL_UPTREND               1097    42.2%     0.54%
    MID_VOL_SIDEWAYS               279    49.8%     0.18%
    MID_VOL_UPTREND               1090    43.0%     1.12%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.00    -0.55%    7.80%    0.98  33.7%      104
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.69   -10.61%   12.90%    0.80  37.4%      409
  QuietBrk 20d             0.05    -0.27%    8.43%    0.99  38.8%      263
  TrendPB v2 pct=3%        0.23     1.50%    3.84%    1.09  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.36     3.82%    5.86%    1.10  53.6%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.62    -3.56%    4.31%    0.81  37.1%      647

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           87         +365     31.0%         +4   -10.3%
  TrendPB            18          -37     50.0%         -2     1.0%
  RSI-MR            164         -329     50.6%         -2     9.2%
  DualMA             14         -751     14.3%        -54    21.1%
  Breakout          364        -2809     32.7%         -8    78.9%
  TOTAL             647        -3561
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5807    4437       1368          2       41       75.7%
  Breakout         5694    1949       2960        785      484       25.7%
  QuietBrk         1996     474       1473         49      134       17.0%
  TrendPB          4297     237       2582       1478       30        4.8%
  RSI-MR           4908     758       2820       1330      302        9.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             39   6.0%    51.3%      +25.5        +995
  strategy            608  94.0%    36.2%       -7.5       -4556

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       3.3%   96.7%    58.3%      31.8%    +35.8       -9.2
  DualMA        85.7%   14.3%    16.7%       0.0%    -54.2      -50.2
  QuietBrk      17.2%   82.8%    73.3%      22.2%    +81.1      -11.8
  RSI-MR         0.0%  100.0%     0.0%      50.6%     +0.0       -2.0
  TrendPB        0.0%  100.0%     0.0%      50.0%     +0.0       -2.0
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2025-03-31 [BULL_MEDVOL/MEDIUM] → DualMA=0.05  Breakout=0.45  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [RCAQualityGate] 2025-04-01 → Breakout WR 9.1% < 40% over last 11 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-06 [BULL_MEDVOL/MEDIUM] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-14 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.20  Breakout=0.45  QuietBrk=0.20  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  Adaptive  (5-strat)     -0.45    -4.04%    6.33%    0.85  33.9%      528
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           95        +1251     30.5%        +13   -31.7%
  RSI-MR             42           -5     40.5%         -0     0.1%
  TrendPB            15           -8     46.7%         -1     0.2%
  DualMA              4          -44     25.0%        -11     1.1%
  Breakout          372        -5133     33.6%        -14   130.3%
  TOTAL             528        -3940
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3649     728       2921          0       20       19.4%
  Breakout         5534    4984         17        533      490       81.2%
  QuietBrk         2066     692       1342         32      129       27.3%
  TrendPB          3992     185       2240       1567       33        3.8%
  RSI-MR           2424     345       1437        642      232        4.7%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2025-04-01 → Breakout WR 8.3% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.13    -1.12%    6.64%    0.95  35.9%      440
                         (LLM calls: 56)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk          105        +1079     29.5%        +10  -100.9%
  TrendPB            23         +446     56.5%        +19   -41.7%
  DualMA              5         -154     20.0%        -31    14.4%
  RSI-MR             53         -168     54.7%         -3    15.7%
  Breakout          254        -2273     33.1%         -9   212.5%
  TOTAL             440        -1069
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3453     799       2654          0       20       22.6%
  Breakout         3774    2815        481        478      393       64.2%
  QuietBrk         2128     844       1248         36      133       33.4%
  TrendPB          3607    1412        963       1232       20       38.6%
  RSI-MR           2922     428       1735        759      226        6.9%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              + 0.32  +   2.92%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1615  (577 winners / 1038 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   53.3%   (price continued post-exit)
    False breakout rate  :   29.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.344      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.03%    +0.04%    +0.27%
    Losers       +0.31%    +0.28%    +0.80%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.095  (>0 = stable universe → better trades)
    Turnover vs success  : +0.022  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               43    44.2%    -0.10%
    HIGH_VOL_UPTREND               357    37.3%    -0.25%
    LOW_VOL_SIDEWAYS               180    32.2%    -0.11%
    LOW_VOL_UPTREND                517    34.0%    -0.55%
    MID_VOL_SIDEWAYS                79    35.4%    -1.40%
    MID_VOL_UPTREND                439    37.1%    -0.09%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```


---

## Meta Recalibration Test — 2026-06-03 00:34

**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  
**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + `_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  
**Costs:** 0.10% commission + 0.05% slippage per side  
**Env:** `PYTHONHASHSEED=0`, `LLM_CACHE_ENABLED=1`, `ADAPTIVE_ONLY=0`

```

  [Cache] Loading 150 symbols from LOCAL SQLite (2014-01-01 → 2026-12-31)...
  [Cache] Local hit: 401,564 records for 150 symbols (no Supabase calls).

[DynamicUniverseAgent] Bulk fetching 150 symbols from 2018-06-15 to 2020-02-01 ...
[DynamicUniverseAgent] Loaded 146 symbols. Skipped 4: TMCV(no data), ETERNAL(no data), SBICARD(no data), MAXHEALTH(no data)

======================================================================
  Period: Bull  2019–2020   (2019-01-01 → 2020-02-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.10    -1.46%    8.43%    0.62  27.4%       84
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.27     2.77%   11.03%    1.03  39.8%      387
  QuietBrk 20d             0.47     5.34%   10.96%    0.95  35.8%      243
  TrendPB v2 pct=3%        0.39     2.79%    4.94%    1.14  54.5%      253
  TrendPB v2 pct=5%        0.90     4.51%    2.85%    1.43  57.3%      124
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.08    -1.18%   10.86%    0.98  54.8%      416
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.56    -3.69%    7.85%    0.83  41.7%      933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            315         +308     52.4%         +1    -6.8%
  TrendPB            55          +17     43.6%         +0    -0.4%
  DualMA             25        -1262     20.0%        -50    27.7%
  QuietBrk           88        -1717     25.0%        -20    37.7%
  Breakout          450        -1904     38.4%         -4    41.8%
  TOTAL             933        -4558
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6765    5405       1356          4       18       79.6%
  Breakout         7118    2058       3645       1415      187       26.3%
  QuietBrk         2052     412       1570         70       51       17.6%
  TrendPB          5897     541       2996       2360       32        8.6%
  RSI-MR           6588    1002       3917       1669      149       12.9%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             62   6.6%    43.5%       -2.3        -141
  strategy            871  93.4%    41.6%       -5.1       -4417

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.7%   95.3%    71.4%      36.8%    +43.6       -6.6
  DualMA        92.0%    8.0%    21.7%       0.0%    -49.4      -63.1
  QuietBrk      20.5%   79.5%    38.9%      21.4%     +4.4      -25.7
  RSI-MR         0.0%  100.0%     0.0%      52.4%     +0.0       +1.0
  TrendPB        0.0%  100.0%     0.0%      43.6%     +0.0       +0.3
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2019-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-01-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2019-01-21 → Breakout WR 18.8% < 40% over last 16 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-01-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-03 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-02-10 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-02-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-02-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-03-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-04-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2019-05-12 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-19 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2019-05-26 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-06-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-06-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-06-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2019-06-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-06-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2019-07-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-07-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-04 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-18 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2019-08-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-09-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-09-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2019-10-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2019-10-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-11-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2019-12-08 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2019-12-15 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2019-12-29 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-05 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  Adaptive  (5-strat)     -0.16    -2.04%    7.51%    0.87  41.2%      684
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  RSI-MR            130         +542     55.4%         +4   -13.0%
  TrendPB            53         +173     50.9%         +3    -4.2%
  DualMA             11         -219     27.3%        -20     5.3%
  QuietBrk           76        -1221     28.9%        -16    29.3%
  Breakout          414        -3442     38.2%         -8    82.6%
  TOTAL             684        -4167
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3750    1151       2597          2        6       30.5%
  Breakout         6408    5025        358       1025      255       74.4%
  QuietBrk         1857     596       1219         42       70       28.3%
  TrendPB          5147     627       2380       2140       35       11.5%
  RSI-MR           3193     532       1967        694      175       11.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2019-01-21 → Breakout WR 21.4% < 40% over last 14 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.43     3.39%    5.51%    1.09  42.4%      859
                         (LLM calls: 58)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          419        +3448     37.7%         +8   138.7%
  RSI-MR            278        +3087     55.4%        +11   124.2%
  TrendPB            57         +477     50.9%         +8    19.2%
  DualMA             28        -1503     25.0%        -54   -60.5%
  QuietBrk           77        -3024     20.8%        -39  -121.7%
  TOTAL             859        +2486
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           6316    2508       3803          5       18       39.4%
  Breakout         6837    1595       3887       1355      228       20.0%
  QuietBrk         1820    1062        686         72       62       54.9%
  TrendPB          5621    2452        969       2200       28       43.1%
  RSI-MR           5694    1422       2842       1430      162       22.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                291         8       1.10
  MeanReversionUniverseFilter          1099        16       4.15
  DualMAUniverseFilter                  556        12       2.10
  RCA delta              + 0.59  +   5.42%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bull  2019–2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2476  (1035 winners / 1441 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.8%   (price continued post-exit)
    False breakout rate  :   36.8%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.240      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.08%    +0.08%    +0.13%
    Losers       -0.10%    -0.19%    -0.10%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (265 days):
    Avg stability score  : 0.331  (0=fully churning, 1=static)
    Avg daily turnover   : 54.3%
    Avg leader half-life : 1.9 days
    Stability vs PnL corr: +0.016  (>0 = stable universe → better trades)
    Turnover vs success  : +0.068  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              115    46.1%     1.22%
    HIGH_VOL_UPTREND               678    49.7%     0.77%
    LOW_VOL_SIDEWAYS               295    48.5%     0.09%
    LOW_VOL_UPTREND                605    33.9%    -0.88%
    MID_VOL_SIDEWAYS               153    51.6%    -0.64%
    MID_VOL_UPTREND                630    34.6%    -0.77%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-06-15 to 2020-12-31 ...
[DynamicUniverseAgent] Loaded 148 symbols. Skipped 2: TMCV(no data), ETERNAL(no data)

======================================================================
  Period: Crash 2020        (2020-01-01 → 2020-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.67    23.80%    9.00%    2.27  49.5%       93
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             1.72    29.08%    7.25%    1.49  41.3%      426
  QuietBrk 20d             1.95    31.64%   12.71%    1.70  39.0%      287
  TrendPB v2 pct=3%        1.62    19.51%    5.84%    1.53  60.9%      425
  TrendPB v2 pct=5%        1.83    16.68%    5.42%    1.78  62.8%      253
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.05    13.63%   10.08%    1.31  61.6%      435
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    2.53    27.91%    5.21%    1.98  50.1%      991

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          520       +17301     43.3%        +33    68.4%
  QuietBrk           99        +3216     40.4%        +32    12.7%
  RSI-MR            246        +2976     65.4%        +12    11.8%
  TrendPB           106        +1679     59.4%        +16     6.6%
  DualMA             20         +127     35.0%         +6     0.5%
  TOTAL             991       +25299
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           8346    6692       1644         10       22       79.9%
  Breakout         8558    2359       4812       1387      261       24.5%
  QuietBrk         2698     501       2119         78       47       16.8%
  TrendPB          7116     579       2849       3688       72        7.1%
  RSI-MR           7514     728       4525       2261       98        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             97   9.8%    69.1%     +139.5      +13535
  strategy            894  90.2%    48.0%      +13.2      +11764

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       9.6%   90.4%    82.0%      39.1%   +181.8      +17.5
  DualMA        90.0%   10.0%    38.9%       0.0%    +18.4     -101.9
  QuietBrk      29.3%   70.7%    65.5%      30.0%   +141.9      -12.9
  RSI-MR         0.0%  100.0%     0.0%      65.4%     +0.0      +12.1
  TrendPB        0.0%  100.0%     0.0%      59.4%     +0.0      +15.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-01-06 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-01-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] 2020-01-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-01-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-02-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-02-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2020-02-23 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2020-03-01 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2020-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-03-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      2.33    33.17%    6.79%    1.88  45.8%      823
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          506       +24976     41.9%        +49    82.3%
  QuietBrk           96        +3973     36.5%        +41    13.1%
  TrendPB            98        +1301     59.2%        +13     4.3%
  RSI-MR            114         +105     60.5%         +1     0.3%
  DualMA              9           -5     33.3%         -1    -0.0%
  TOTAL             823       +30351
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7031    1401       5622          8       14       19.7%
  Breakout         7879    6800         82        997      342       82.0%
  QuietBrk         2505     651       1793         61       57       23.7%
  TrendPB          6433     575       2321       3537       83        7.6%
  RSI-MR           5764     470       3467       1827      171        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-01-13 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.18    25.07%    6.05%    1.80  48.5%      923
                         (LLM calls: 54)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          508       +15711     43.1%        +31    68.4%
  QuietBrk          107        +2606     37.4%        +24    11.3%
  TrendPB           112        +2213     57.1%        +20     9.6%
  RSI-MR            180        +1979     65.0%        +11     8.6%
  DualMA             16         +469     50.0%        +29     2.0%
  TOTAL             923       +22977
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           7874    2239       5626          9       17       28.2%
  Breakout         8396    3136       3995       1265      278       34.0%
  QuietBrk         2724    1555       1098         71       41       55.6%
  TrendPB          6763    2128       1139       3496       55       30.7%
  RSI-MR           6492    1472       3037       1983      107       21.0%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                305         8       1.22
  MeanReversionUniverseFilter          1171        19       4.68
  DualMAUniverseFilter                  604        13       2.42
  RCA delta              -0.15    -8.10%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Crash 2020]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 2737  (1321 winners / 1416 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   56.6%   (price continued post-exit)
    False breakout rate  :   37.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.139      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.13%    +0.91%    +1.31%
    Losers       -0.02%    +0.60%    +0.91%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (250 days):
    Avg stability score  : 0.356  (0=fully churning, 1=static)
    Avg daily turnover   : 52.1%
    Avg leader half-life : 2.1 days
    Stability vs PnL corr: +0.052  (>0 = stable universe → better trades)
    Turnover vs success  : +0.057  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               81    58.0%     0.04%
    HIGH_VOL_UPTREND               945    44.0%     1.39%
    LOW_VOL_SIDEWAYS               251    65.3%     4.71%
    LOW_VOL_UPTREND                676    47.0%     1.42%
    MID_VOL_SIDEWAYS               115    71.3%     3.07%
    MID_VOL_UPTREND                669    43.9%     1.70%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2019-09-14 to 2021-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recov 2020–2021   (2020-04-01 → 2021-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          1.87    51.22%    9.01%    2.40  52.7%      169
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             2.62   105.97%   11.72%    1.79  44.6%      822
  QuietBrk 20d             2.42    92.87%   14.52%    1.91  43.6%      546
  TrendPB v2 pct=3%        1.24    29.13%    9.93%    1.36  60.2%      782
  TrendPB v2 pct=5%        1.30    23.55%    6.96%    1.49  60.9%      460
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      1.31    32.35%    7.52%    1.34  58.8%      873
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    3.00    68.25%    6.28%    2.12  51.3%     1985

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1036       +44120     46.3%        +43    65.0%
  QuietBrk          192       +11193     44.8%        +58    16.5%
  RSI-MR            503        +6718     60.6%        +13     9.9%
  DualMA             41        +3873     53.7%        +94     5.7%
  TrendPB           213        +1966     59.2%         +9     2.9%
  TOTAL            1985       +67869
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16452   13264       3164         24       29       80.4%
  Breakout        17177    4707       9629       2841      439       24.8%
  QuietBrk         5273     945       4150        178       99       16.0%
  TrendPB         14309    1152       6003       7154      113        7.3%
  RSI-MR          15042    1436       9119       4487      176        8.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            186   9.4%    74.2%     +216.7      +40306
  strategy           1799  90.6%    49.0%      +15.3      +27564

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       8.9%   91.1%    81.5%      42.9%   +268.5      +20.6
  DualMA        90.2%    9.8%    56.8%      25.0%   +110.7      -56.1
  QuietBrk      29.7%   70.3%    73.7%      32.6%   +201.9       -2.3
  RSI-MR         0.0%  100.0%     0.0%      60.6%     +0.0      +13.4
  TrendPB        0.0%  100.0%     0.0%      59.2%     +0.0       +9.2
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2020-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-04-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2020-05-25 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-05-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2020-06-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [RCAQualityGate] 2020-06-10 → Breakout WR 10.0% < 40% over last 10 trades — CB relaxation disabled
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2020-06-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-06-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-07-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-08-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-13 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-09-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-10-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2020-11-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-11-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2020-12-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-01-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-02-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-03-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-03-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-04-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2021-04-11 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-18 [MIXED/LOW] → DualMA=0.22  Breakout=0.22  QuietBrk=0.22  TrendPB=0.22  RSI-MR=0.10
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2021-04-25 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2021-05-02 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2021-05-09 [BULL_MEDVOL/MEDIUM] → DualMA=0.21  Breakout=0.26  QuietBrk=0.21  TrendPB=0.26  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2021-05-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-05-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-06-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-07-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-08-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-08-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-09-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-10-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2021-11-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-11-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2021-12-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2021-12-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  Adaptive  (5-strat)      2.81    85.60%    8.94%    2.02  49.3%     1711
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1050       +72349     46.7%        +69    85.3%
  QuietBrk          175        +8911     38.9%        +51    10.5%
  TrendPB           203        +1585     59.1%         +8     1.9%
  DualMA             19        +1226     42.1%        +65     1.4%
  RSI-MR            264         +774     59.5%         +3     0.9%
  TOTAL            1711       +84845
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15465    3222      12228         15       20       20.7%
  Breakout        15737   13426        323       1988      537       81.9%
  QuietBrk         4730    1235       3354        141      131       23.3%
  TrendPB         12778     941       4944       6893      119        6.4%
  RSI-MR          13308    1150       7959       4199      483        5.0%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2020-06-10 → Breakout WR 16.7% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   2.79    68.31%    5.91%    2.07  50.6%     1918
                         (LLM calls: 93)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1023       +46900     46.5%        +46    68.9%
  QuietBrk          209       +12169     42.1%        +58    17.9%
  RSI-MR            415        +4740     60.0%        +11     7.0%
  DualMA             39        +2386     53.8%        +61     3.5%
  TrendPB           232        +1906     58.6%         +8     2.8%
  TOTAL            1918       +68101
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          16293    4022      12249         22       28       24.5%
  Breakout        16930    6493       7723       2714      450       35.7%
  QuietBrk         5345    2963       2216        166       89       53.8%
  TrendPB         14079    4827       2153       7099       80       33.7%
  RSI-MR          14765    2903       7343       4519      293       17.7%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                583         9       1.34
  MeanReversionUniverseFilter          2194        20       5.04
  DualMAUniverseFilter                  983        13       2.26
  RCA delta              -0.02   -17.28%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recov 2020–2021]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5614  (2832 winners / 2782 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   54.5%   (price continued post-exit)
    False breakout rate  :   34.7%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.116      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      -0.07%    +0.75%    +1.19%
    Losers       -0.09%    +0.37%    +0.74%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (435 days):
    Avg stability score  : 0.346  (0=fully churning, 1=static)
    Avg daily turnover   : 53.3%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: +0.005  (>0 = stable universe → better trades)
    Turnover vs success  : -0.018  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              330    55.2%     0.72%
    HIGH_VOL_UPTREND              2586    48.6%     1.84%
    LOW_VOL_SIDEWAYS               277    65.3%     5.43%
    LOW_VOL_UPTREND                820    49.5%     1.80%
    MID_VOL_SIDEWAYS               313    60.4%     2.82%
    MID_VOL_UPTREND               1288    48.0%     2.08%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2022-12-31 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Bear  2022        (2022-01-01 → 2022-12-31)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.20    -2.29%   10.37%    0.88  38.3%       81
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.26     2.42%   11.98%    1.06  41.7%      343
  QuietBrk 20d            -0.22    -3.81%   16.98%    0.90  37.3%      220
  TrendPB v2 pct=3%       -1.09   -10.64%   12.14%    0.71  52.3%      241
  TrendPB v2 pct=5%       -0.40    -2.48%    5.86%    0.87  50.0%      116
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.97   -12.12%   15.78%    0.72  48.5%      344
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    0.05     0.07%    7.67%    1.00  40.7%      703

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +2360     38.8%         +6  4016.7%
  DualMA             28         +177     50.0%         +6   301.3%
  TrendPB            50          -89     46.0%         -2  -151.7%
  QuietBrk           72         -895     26.4%        -12 -1523.4%
  RSI-MR            177        -1494     47.5%         -8 -2543.0%
  TOTAL             703          +59
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5822    4523       1297          2       27       77.2%
  Breakout         6042    2093       2989        960      396       28.1%
  QuietBrk         1664     379       1214         71       79       18.0%
  TrendPB          4774     396       2371       2007       63        7.0%
  RSI-MR           5304     741       3075       1488      244        9.4%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             64   9.1%    56.2%      +59.4       +3804
  strategy            639  90.9%    39.1%       -5.9       -3745

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       4.3%   95.7%    81.2%      36.9%   +174.6       -1.2
  DualMA        96.4%    3.6%    48.1%     100.0%     +6.1      +13.1
  QuietBrk      29.2%   70.8%    47.6%      17.6%    +40.3      -34.1
  RSI-MR         0.0%  100.0%     0.0%      47.5%     +0.0       -8.4
  TrendPB        0.0%  100.0%     0.0%      46.0%     +0.0       -1.8
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      0.22     1.53%    9.89%    1.06  38.4%      529
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          376        +3291     38.3%         +9   210.7%
  RSI-MR             37         +273     56.8%         +7    17.5%
  TrendPB            44          -97     43.2%         -2    -6.2%
  DualMA              9         -154     44.4%        -17    -9.8%
  QuietBrk           63        -1752     23.8%        -28  -112.2%
  TOTAL             529        +1562
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           2882     808       2073          1       14       27.6%
  Breakout         5494    4740        212        542      430       78.4%
  QuietBrk         1481     493        940         48      101       26.5%
  TrendPB          4052     433       1694       1925       69        9.0%
  RSI-MR           1872     254       1133        485      156        5.2%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   0.09     0.41%   13.31%    1.01  38.9%      522
                         (LLM calls: 52)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout          371        +3742     37.7%        +10   912.7%
  TrendPB            41          -43     43.9%         -1   -10.5%
  DualMA             10         -166     40.0%        -17   -40.4%
  QuietBrk           45         -541     33.3%        -12  -132.0%
  RSI-MR             55        -2582     47.3%        -47  -629.9%
  TOTAL             522         +410
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           4156    1082       3073          1       13       25.7%
  Breakout         5305    3783        979        543      446       62.9%
  QuietBrk         1283     467        776         40       98       28.8%
  TrendPB          3673     898       1057       1718       48       23.1%
  RSI-MR           1455     379        714        362       57       22.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                306         7       1.23
  MeanReversionUniverseFilter          1030        17       4.15
  DualMAUniverseFilter                  668        16       2.69
  RCA delta              -0.12    -1.12%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Bear  2022]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1754  (692 winners / 1062 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   47.3%   (price continued post-exit)
    False breakout rate  :   37.3%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.295      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.08%    +0.21%    +0.27%
    Losers       -0.15%    -0.17%    -0.47%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (248 days):
    Avg stability score  : 0.327  (0=fully churning, 1=static)
    Avg daily turnover   : 53.7%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.098  (>0 = stable universe → better trades)
    Turnover vs success  : -0.000  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               52    34.6%    -1.70%
    HIGH_VOL_UPTREND               399    36.1%    -0.28%
    LOW_VOL_SIDEWAYS               219    52.1%     1.62%
    LOW_VOL_UPTREND                520    37.7%    -0.31%
    MID_VOL_SIDEWAYS               131    44.3%    -0.10%
    MID_VOL_UPTREND                433    37.4%     0.10%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2021-06-15 to 2024-06-01 ...
[DynamicUniverseAgent] Loaded 149 symbols. Skipped 1: TMCV(no data)

======================================================================
  Period: Recent2022–2024   (2022-01-01 → 2024-06-01)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50          0.49    10.25%   11.79%    1.16  40.5%      205
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d             0.80    26.11%   13.00%    1.19  41.1%      894
  QuietBrk 20d             0.65    20.36%   18.27%    1.18  40.7%      573
  TrendPB v2 pct=3%        0.33     6.01%   15.19%    1.11  57.4%      563
  TrendPB v2 pct=5%        0.87    11.19%    7.31%    1.40  59.8%      266
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80     -0.28    -9.19%   18.38%    0.91  52.9%      908
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)    1.13    22.42%    7.67%    1.35  45.5%     1933

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1049       +15242     41.8%        +15    77.0%
  QuietBrk          229        +1888     33.2%         +8     9.5%
  TrendPB           117        +1233     56.4%        +11     6.2%
  DualMA             61        +1069     52.5%        +18     5.4%
  RSI-MR            477         +359     55.8%         +1     1.8%
  TOTAL            1933       +19792
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          17391   13788       3595          8       67       78.9%
  Breakout        17847    5426       9817       2604      963       25.0%
  QuietBrk         5465    1171       4139        155      235       17.1%
  TrendPB         14233     882       7647       5704      101        5.5%
  RSI-MR          15500    1793       9008       4699      539        8.1%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop            190   9.8%    63.7%      +95.0      +18058
  strategy           1743  90.2%    43.5%       +1.0       +1734

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       6.9%   93.1%    73.6%      39.5%   +154.5       +4.2
  DualMA        86.9%   13.1%    54.7%      37.5%    +22.4      -14.9
  QuietBrk      28.4%   71.6%    60.0%      22.6%    +88.4      -23.5
  RSI-MR         0.0%  100.0%     0.0%      55.8%     +0.0       +0.8
  TrendPB        0.0%  100.0%     0.0%      56.4%     +0.0      +10.5
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2022-01-02 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2022-01-09 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-01-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [RCAQualityGate] 2022-01-18 → Breakout WR 35.0% < 40% over last 20 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-01-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2022-01-30 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-02-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-02-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-13 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-20 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-03-27 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-04-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-04-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-05-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-05-29 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-06-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2022-07-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2022-07-24 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-07-31 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-07 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-08-21 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-08-28 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-09-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-09-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-09-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-02 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-09 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-10-16 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-23 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2022-10-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-11-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-11-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2022-12-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2022-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-01-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-01-22 [MIXED/LOW] → DualMA=0.25  Breakout=0.25  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-01-29 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-02-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.35  TrendPB=0.20  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2023-02-19 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-02-26 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2023-03-12 [MIXED/LOW] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2023-03-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-03-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2023-04-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2023-04-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2023-05-01 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-05-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-06-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-06-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-02 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-07-30 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-08-27 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-09-24 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-10-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2023-10-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-11-27 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2023-12-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-22 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-01-28 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-11 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-18 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-02-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-03 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-10 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2024-03-17 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-25 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-03-31 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-04-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-05 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-12 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2024-05-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  Adaptive  (5-strat)      1.54    41.78%    9.89%    1.48  45.0%     1540
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1020       +27377     41.9%        +27    76.7%
  QuietBrk          212        +6108     37.7%        +29    17.1%
  TrendPB           112        +1255     56.2%        +11     3.5%
  RSI-MR            172         +674     65.1%         +4     1.9%
  DualMA             24         +274     45.8%        +11     0.8%
  TOTAL            1540       +35689
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          13411    2706      10698          7       42       19.9%
  Breakout        16233   14320        314       1599     1074       81.6%
  QuietBrk         5362    1602       3665         95      273       24.8%
  TrendPB         12474     783       5964       5727      109        5.4%
  RSI-MR          10351    1029       5985       3337      602        4.1%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2022-01-19 → Breakout WR 30.0% < 40% over last 20 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)   1.09    24.35%   13.31%    1.34  45.8%     1706
                         (LLM calls: 126)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  Breakout         1007       +19070     42.2%        +19    87.8%
  QuietBrk          219        +2445     37.9%        +11    11.3%
  TrendPB           114        +1794     56.1%        +16     8.3%
  DualMA             32         -247     43.8%         -8    -1.1%
  RSI-MR            334        -1352     58.4%         -4    -6.2%
  TOTAL            1706       +21709
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA          15052    3923      11123          6       48       25.7%
  Breakout        16690    6498       8086       2106     1071       32.5%
  QuietBrk         5205    2934       2151        120      230       52.0%
  TrendPB         12713    5212       2113       5388       77       40.4%
  RSI-MR          10710    2372       5069       3269      303       19.3%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                734         8       1.24
  MeanReversionUniverseFilter          2457        19       4.14
  DualMAUniverseFilter                 1376        16       2.32
  RCA delta              -0.45   -17.44%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Recent2022–2024]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 5179  (2353 winners / 2826 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   55.1%   (price continued post-exit)
    False breakout rate  :   32.1%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.204      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.01%    +0.44%    +0.87%
    Losers       -0.04%    +0.10%    +0.26%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (594 days):
    Avg stability score  : 0.320  (0=fully churning, 1=static)
    Avg daily turnover   : 54.4%
    Avg leader half-life : 2.0 days
    Stability vs PnL corr: -0.052  (>0 = stable universe → better trades)
    Turnover vs success  : -0.008  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS              266    50.4%     0.25%
    HIGH_VOL_UPTREND              2176    45.9%     0.71%
    LOW_VOL_SIDEWAYS               340    50.0%     1.40%
    LOW_VOL_UPTREND               1054    42.5%     0.49%
    MID_VOL_SIDEWAYS               264    52.7%     0.40%
    MID_VOL_UPTREND               1079    43.0%     1.04%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════
[DynamicUniverseAgent] Bulk fetching 150 symbols from 2024-06-15 to 2026-03-24 ...
[DynamicUniverseAgent] Loaded 150 symbols. Skipped 0: none

======================================================================
  Period: Live  2025–2026   (2025-01-01 → 2026-03-24)
  Universe: 150 symbols → DynamicUniverse top 80 → UniverseSelection top 20
  Costs: 0.10% commission + 0.05% slippage per side (all returns net of costs)
======================================================================
  Strategy               Sharpe    Return    MaxDD      PF     WR  #Trades
  --------------------------------------------------------------------  [Medium-term]
  DualMA SMA20/50         -0.00    -0.55%    7.80%    0.98  33.7%      104
  --------------------------------------------------------------------  [Short-term]
  Breakout 10d            -0.69   -10.61%   12.90%    0.80  37.4%      409
  QuietBrk 20d             0.05    -0.27%    8.43%    0.99  38.8%      263
  TrendPB v2 pct=3%        0.23     1.50%    3.84%    1.09  53.3%      135
  TrendPB v2 pct=5%        0.96     3.66%    1.97%    1.74  56.6%       53
  --------------------------------------------------------------------  [Mean-reversion]
  RSI-MR  os=5  ob=80      0.36     3.82%    5.86%    1.10  53.6%      351
  --------------------------------------------------------------------  [Multi-strategy baseline — equal weight]
  EqualWeight (5-strat)   -0.62    -3.56%    4.31%    0.81  37.1%      647

  --------------------------------------------------------------------  [Strategy PnL Attribution — EqualWeight]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           87         +365     31.0%         +4   -10.3%
  TrendPB            18          -37     50.0%         -2     1.0%
  RSI-MR            164         -329     50.6%         -2     9.2%
  DualMA             14         -751     14.3%        -54    21.1%
  Breakout          364        -2809     32.7%         -8    78.9%
  TOTAL             647        -3561
  --------------------------------------------------------------------  [EqualWeight — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           5807    4437       1368          2       41       75.7%
  Breakout         5694    1949       2960        785      484       25.7%
  QuietBrk         1996     474       1473         49      134       17.0%
  TrendPB          4297     237       2582       1478       30        4.8%
  RSI-MR           4908     758       2820       1330      302        9.3%

  --------------------------------------------------------------------  [EqualWeight — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85

  --------------------------------------------------------------------  [Exit Attribution — EqualWeight]
  Reason           Trades     %   WinRate    Avg PnL    Total PnL
  atr_stop             39   6.0%    51.3%      +25.5        +995
  strategy            608  94.0%    36.2%       -7.5       -4556

  Strategy       ATR%  Strat%   ATR WR   Strat WR   ATR Avg   Strat Avg
  Breakout       3.3%   96.7%    58.3%      31.8%    +35.8       -9.2
  DualMA        85.7%   14.3%    16.7%       0.0%    -54.2      -50.2
  QuietBrk      17.2%   82.8%    73.3%      22.2%    +81.1      -11.8
  RSI-MR         0.0%  100.0%     0.0%      50.6%     +0.0       -2.0
  TrendPB        0.0%  100.0%     0.0%      50.0%     +0.0       -2.0
  --------------------------------------------------------------------  [Multi-strategy adaptive — LLM weights]
  [AdaptiveSelector] 2025-01-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-06 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-12 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-19 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-26 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-01-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-05 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-02-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-02 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-09 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] 2025-03-16 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-03-23 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → BULL_MEDVOL (after 2 weeks)
  [AdaptiveSelector] 2025-03-31 [BULL_MEDVOL/MEDIUM] → DualMA=0.05  Breakout=0.45  QuietBrk=0.05  TrendPB=0.45  RSI-MR=0.00
  [RCAQualityGate] 2025-04-01 → Breakout WR 9.1% < 40% over last 11 trades — CB relaxation disabled
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-06 [BULL_MEDVOL/MEDIUM] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding BULL_MEDVOL
  [AdaptiveSelector] 2025-04-14 [BULL_MEDVOL/MEDIUM] → DualMA=0.15  Breakout=0.45  QuietBrk=0.15  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: BULL_MEDVOL → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-04-20 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-04-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-04 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-05-25 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-01 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-08 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-15 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-06-22 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2025-06-29 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-06 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-07-13 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-20 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-07-27 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2025-08-03 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-10 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2025-08-17 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-24 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-08-31 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-07 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-14 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-21 [CRASH_HIGHVOL/HIGH] → DualMA=0.24  Breakout=0.36  QuietBrk=0.10  TrendPB=0.24  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2025-09-28 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.40  TrendPB=0.00  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: CRASH_HIGHVOL → MIXED (after 2 weeks)
  [AdaptiveSelector] 2025-10-05 [MIXED/LOW] → DualMA=0.05  Breakout=0.45  QuietBrk=0.25  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding MIXED
  [AdaptiveSelector] 2025-10-12 [MIXED/LOW] → DualMA=0.20  Breakout=0.45  QuietBrk=0.20  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: MIXED → RECOVERY (after 2 weeks)
  [AdaptiveSelector] 2025-10-19 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-10-26 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-02 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-09 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-11-16 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-23 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-11-30 [RECOVERY/HIGH] → DualMA=0.15  Breakout=0.35  QuietBrk=0.30  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-07 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] 2025-12-14 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BEAR_EARLY (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-21 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2025-12-28 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: BULL_SUSTAINED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-04 [RECOVERY/HIGH] → DualMA=0.16  Breakout=0.37  QuietBrk=0.27  TrendPB=0.15  RSI-MR=0.05
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-11 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: BULL_MEDVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-18 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: CRASH_HIGHVOL (1/2 weeks) — holding RECOVERY
  [AdaptiveSelector] 2026-01-26 [RECOVERY/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.40  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime transition confirmed: RECOVERY → CRASH_HIGHVOL (after 2 weeks)
  [AdaptiveSelector] 2026-02-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: MIXED (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-02-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] Regime pending: RECOVERY (1/2 weeks) — holding CRASH_HIGHVOL
  [AdaptiveSelector] 2026-02-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.15  Breakout=0.45  QuietBrk=0.25  TrendPB=0.15  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-01 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-08 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.30  TrendPB=0.25  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-15 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  [AdaptiveSelector] 2026-03-22 [CRASH_HIGHVOL/HIGH] → DualMA=0.00  Breakout=0.45  QuietBrk=0.45  TrendPB=0.10  RSI-MR=0.00
  Adaptive  (5-strat)     -0.45    -4.04%    6.33%    0.85  33.9%      528
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk           95        +1251     30.5%        +13   -31.7%
  RSI-MR             42           -5     40.5%         -0     0.1%
  TrendPB            15           -8     46.7%         -1     0.2%
  DualMA              4          -44     25.0%        -11     1.1%
  Breakout          372        -5133     33.6%        -14   130.3%
  TOTAL             528        -3940
  --------------------------------------------------------------------  [Adaptive — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           3649     728       2921          0       20       19.4%
  Breakout         5534    4984         17        533      490       81.2%
  QuietBrk         2066     692       1342         32      129       27.3%
  TrendPB          3992     185       2240       1567       33        3.8%
  RSI-MR           2424     345       1437        642      232        4.7%

  --------------------------------------------------------------------  [Adaptive — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  --------------------------------------------------------------------  [Multi-strategy adaptive + RegimeContextAgent]
  [RCAQualityGate] 2025-04-01 → Breakout WR 8.3% < 40% over last 12 trades — CB relaxation disabled
  Adaptive+RCA (5-strat)  -0.12    -1.02%    4.87%    0.95  37.7%      533
                         (LLM calls: 66)

  --------------------------------------------------------------------  [Strategy PnL Attribution — Adaptive+RCA]
  Strategy       Trades      PnL (₹)   WinRate   Avg/trade   Share%
  ----------------------------------------------------------------
  QuietBrk          105        +1278     31.4%        +12  -124.8%
  RSI-MR            112         +608     56.2%         +5   -59.4%
  TrendPB            17         -252     47.1%        -15    24.6%
  DualMA             12         -661     25.0%        -55    64.6%
  Breakout          287        -1997     32.8%         -7   195.1%
  TOTAL             533        -1024
  --------------------------------------------------------------------  [Adaptive+RCA — signal-drop diagnostics]
  Strategy       issued     won  prio_loss  own_block  buy_rej  pass_thru%
  DualMA           4824    1424       3400          0       34       28.8%
  Breakout         4770    1955       2121        694      448       31.6%
  QuietBrk         2205    1160       1010         35      142       46.2%
  TrendPB          3857    1739        771       1347       29       44.3%
  RSI-MR           3564     714       1939        911      282       12.1%

  --------------------------------------------------------------------  [Adaptive+RCA — union-filter overlap (per trading day)]
  Filter                              total   max/day   mean/day
  BreakoutUniverseFilter                  0         0       0.00
  ActivityTailFilter                      0         0       0.00
  PullbackUniverseFilter                249         8       0.82
  MeanReversionUniverseFilter           993        18       3.26
  DualMAUniverseFilter                  565        11       1.85
  RCA delta              + 0.33  +   3.02%

  ══════════════════════════════════════════════════════════════════
  OPPORTUNITY QUALITY SUMMARY  [Live  2025–2026]
  ══════════════════════════════════════════════════════════════════
  Trades analyzed  : 1708  (620 winners / 1088 losers)
  ──────────────────────────────────────────────────────────────────
  Breakout quality:
    Follow-through rate  :   52.6%   (price continued post-exit)
    False breakout rate  :   27.6%   (MFE>2% but final return <0)
    Persistence half-life:    0.0 days (median survival above entry)
    Avg MFE efficiency   : -0.339      (1.00 = exit at peak)
  ──────────────────────────────────────────────────────────────────
  Continuation decay (post-exit drift):
                      1D        3D        5D
    Winners      +0.05%    +0.04%    +0.24%
    Losers       +0.31%    +0.31%    +0.79%
  ──────────────────────────────────────────────────────────────────
  Universe diagnostics (305 days):
    Avg stability score  : 0.299  (0=fully churning, 1=static)
    Avg daily turnover   : 57.9%
    Avg leader half-life : 1.8 days
    Stability vs PnL corr: +0.107  (>0 = stable universe → better trades)
    Turnover vs success  : +0.000  (<0 = higher churn → fewer successes)
  ──────────────────────────────────────────────────────────────────
  Per-regime breakdown (entry regime):
    Regime                           N  WinRate    AvgRet
    HIGH_VOL_SIDEWAYS               46    47.8%     0.31%
    HIGH_VOL_UPTREND               372    39.0%    -0.28%
    LOW_VOL_SIDEWAYS               195    32.3%    -0.35%
    LOW_VOL_UPTREND                552    34.6%    -0.32%
    MID_VOL_SIDEWAYS                89    33.7%    -1.57%
    MID_VOL_UPTREND                454    37.2%    -0.15%
  ──────────────────────────────────────────────────────────────────
  ══════════════════════════════════════════════════════════════════

======================================================================


```
