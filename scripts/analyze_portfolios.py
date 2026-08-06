#!/usr/bin/env python3
"""
Read-only system diagnosis for live paper portfolios.
Reconstructs closed trades from signal_queue FILLED rows, computes exit-quality
metrics (MFE, MFE efficiency, give-back, days-from-peak) and the late-exit vs
bad-entry disambiguation (MFE distribution, day-1 negative rate).

READ-ONLY. No writes. Does not touch api/.
"""
import os, re, statistics as st
from collections import defaultdict, deque
from datetime import date
from pathlib import Path

# ---- load .env (read-only) ----
for line in Path(__file__).resolve().parents[1].joinpath(".env").read_text().splitlines():
    s = line.strip()
    if s and not s.startswith("#") and "=" in s:
        k, v = s.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

from sqlalchemy import create_engine, text
ENG = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)

SESSIONS = {"pt_ujjwal": "Ujjwal's Portfolio", "pt_4765a5": "Shubham1"}
WM_RE = re.compile(r"watermark ([\d.]+)")
ATR_RE = re.compile(r"ATR\(([\d.]+)\)")

def fetch_fills(session_id):
    q = text("""
        select signal_date, symbol, action, strategy, regime_label, weight,
               fill_price, fill_qty, notes
        from signal_queue
        where session_id=:sid and status='FILLED' and fill_price is not null and fill_qty is not null
        order by signal_date asc, created_at asc""")
    with ENG.connect() as c:
        return [dict(r._mapping) for r in c.execute(q, {"sid": session_id})]

def load_ohlc(symbols):
    """Return {symbol: {'dates':[...], 'idx':{date:i}, 'o/h/l/c':[...]}}"""
    out = {}
    with ENG.connect() as c:
        for sym in symbols:
            rows = c.execute(text("""
                select timestamp::date as d, open, high, low, close
                from market_ohlc where symbol=:s and timestamp >= '2026-03-01'
                order by timestamp asc"""), {"s": sym}).fetchall()
            if not rows:
                continue
            ds = [r[0] for r in rows]
            out[sym] = {
                "dates": ds, "idx": {d: i for i, d in enumerate(ds)},
                "o": [float(r[1]) for r in rows], "h": [float(r[2]) for r in rows],
                "l": [float(r[3]) for r in rows], "c": [float(r[4]) for r in rows],
            }
    return out

def latest_close(ohlc, sym):
    return ohlc[sym]["c"][-1] if sym in ohlc else None

def reconstruct(fills):
    """FIFO lot matching -> list of closed trades + list of open lots."""
    lots = defaultdict(deque)   # symbol -> deque of dicts
    closed, opens = [], []
    for f in fills:
        sym, qty, price = f["symbol"], int(f["fill_qty"]), float(f["fill_price"])
        if qty <= 0:
            continue
        if f["action"] == "BUY":
            m = ATR_RE.search(f["notes"] or "")
            lots[sym].append({
                "qty": qty, "price": price, "date": f["signal_date"],
                "strategy": f["strategy"], "regime": f["regime_label"],
                "weight": f["weight"], "atr": float(m.group(1)) if m else None,
            })
        elif f["action"] == "SELL":
            notes = f["notes"] or ""
            reason = ("atr_stop" if "Trailing ATR stop" in notes
                      else "strategy_exit" if "Strategy exit" in notes else "other")
            wm = WM_RE.search(notes)
            watermark = float(wm.group(1)) if wm else None
            remaining = qty
            while remaining > 0 and lots[sym]:
                lot = lots[sym][0]
                take = min(remaining, lot["qty"])
                closed.append({
                    "symbol": sym, "entry_date": lot["date"], "exit_date": f["signal_date"],
                    "entry_price": lot["price"], "exit_price": price, "qty": take,
                    "entry_strategy": lot["strategy"], "entry_regime": lot["regime"],
                    "entry_weight": lot["weight"], "entry_atr": lot["atr"],
                    "exit_reason": reason, "watermark": watermark,
                })
                lot["qty"] -= take; remaining -= take
                if lot["qty"] == 0:
                    lots[sym].popleft()
            # if remaining>0 here, it's a SELL with no matching lot (ignore, data gap)
    for sym, dq in lots.items():
        for lot in dq:
            opens.append({"symbol": sym, **lot})
    return closed, opens

def trading_slice(o, sym, d0, d1):
    """indices of dates in (d0, d1] for symbol."""
    if sym not in o:
        return []
    ds = o[sym]["dates"]
    return [i for i, d in enumerate(ds) if d0 < d <= d1]

def enrich(closed, ohlc):
    for t in closed:
        sym = t["symbol"]; ep = t["entry_price"]
        t["ret"] = t["exit_price"] / ep - 1.0
        t["pnl"] = (t["exit_price"] - ep) * t["qty"]
        idxs = trading_slice(ohlc, sym, t["entry_date"], t["exit_date"])
        if idxs:
            highs = [ohlc[sym]["h"][i] for i in idxs]
            lows = [ohlc[sym]["l"][i] for i in idxs]
            mfe_price = max(highs); mae_price = min(lows)
            peak_i = idxs[highs.index(mfe_price)]
            t["mfe_pct"] = mfe_price / ep - 1.0
            t["mae_pct"] = mae_price / ep - 1.0
            t["hold_days"] = len(idxs)
            # days from peak to exit (trading days)
            t["days_from_peak"] = idxs[-1] - peak_i
            # mfe in ATR units
            t["mfe_atr"] = (mfe_price - ep) / t["entry_atr"] if t["entry_atr"] else None
            # give-back: fraction of the peak move we surrendered
            t["give_back"] = (mfe_price - t["exit_price"]) / (mfe_price - ep) if mfe_price > ep else None
            # mfe efficiency (final captured / peak available)
            t["mfe_eff"] = (t["ret"] / t["mfe_pct"]) if t["mfe_pct"] > 0 else None
            # day-1 outcome: close on first held day vs entry
            first_i = idxs[0]
            t["day1_ret"] = ohlc[sym]["c"][first_i] / ep - 1.0
            # post-exit drift +1/+3/+5 trading days after exit_date
            ex_idx = ohlc[sym]["idx"].get(t["exit_date"])
            def drift(n):
                if ex_idx is None: return None
                j = ex_idx + n
                if j < len(ohlc[sym]["c"]):
                    return ohlc[sym]["c"][j] / t["exit_price"] - 1.0
                return None
            t["drift_1"], t["drift_3"], t["drift_5"] = drift(1), drift(3), drift(5)
        else:
            for k in ("mfe_pct","mae_pct","hold_days","days_from_peak","mfe_atr",
                      "give_back","mfe_eff","day1_ret","drift_1","drift_3","drift_5"):
                t[k] = None
    return closed

def pct(x): return f"{x*100:+.1f}%" if x is not None else "  n/a"
def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None
def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs)/len(xs) if xs else None

def report(session_id, name):
    fills = fetch_fills(session_id)
    syms = sorted({f["symbol"] for f in fills})
    ohlc = load_ohlc(syms)
    closed, opens = reconstruct(fills)
    enrich(closed, ohlc)

    realised = sum(t["pnl"] for t in closed)
    unreal = 0.0
    for lot in opens:
        lc = latest_close(ohlc, lot["symbol"])
        if lc is not None:
            unreal += (lc - lot["price"]) * lot["qty"]
    start = 100000.0
    total = realised + unreal
    wins = [t for t in closed if t["ret"] > 0]
    losses = [t for t in closed if t["ret"] <= 0]

    print(f"\n{'='*72}\n{name}  ({session_id})\n{'='*72}")
    print(f"closed trades: {len(closed)}   open lots: {len(opens)}")
    print(f"realised P&L: Rs {realised:,.0f}   unrealised: Rs {unreal:,.0f}   "
          f"total: Rs {total:,.0f}   return: {total/start*100:+.1f}%")
    print(f"win rate: {len(wins)/len(closed)*100:.0f}%   "
          f"avg win: {pct(mean([t['ret'] for t in wins]))}   "
          f"avg loss: {pct(mean([t['ret'] for t in losses]))}   "
          f"avg trade: {pct(mean([t['ret'] for t in closed]))}")

    print(f"\n-- EXIT QUALITY --")
    print(f"median MFE efficiency (captured/peak): {mean([t['mfe_eff'] for t in closed]):.2f} mean / "
          f"{med([t['mfe_eff'] for t in closed]):.2f} median" if med([t['mfe_eff'] for t in closed]) is not None else "n/a")
    gb = [t['give_back'] for t in closed if t['give_back'] is not None]
    print(f"median give-back of peak move: {med(gb)*100:.0f}%   mean: {mean(gb)*100:.0f}%   (n={len(gb)})")
    print(f"median days from peak to exit: {med([t['days_from_peak'] for t in closed])}   "
          f"mean: {mean([t['days_from_peak'] for t in closed]):.1f}")
    print(f"median hold: {med([t['hold_days'] for t in closed])} td   "
          f"winners: {med([t['hold_days'] for t in wins])}   losers: {med([t['hold_days'] for t in losses])}")

    print(f"\n-- LATE-EXIT vs BAD-ENTRY --")
    n = len(closed)
    never_green = [t for t in closed if t["mfe_pct"] is not None and t["mfe_pct"] <= 0.005]
    green1 = [t for t in closed if t["mfe_atr"] is not None and t["mfe_atr"] >= 1.0]
    green2 = [t for t in closed if t["mfe_atr"] is not None and t["mfe_atr"] >= 2.0]
    gaveback = [t for t in closed if t["mfe_atr"] is not None and t["mfe_atr"] >= 1.0 and t["ret"] <= 0]
    day1neg = [t for t in closed if t["day1_ret"] is not None and t["day1_ret"] < 0]
    print(f"never meaningfully green (MFE<=0.5%):   {len(never_green)}/{n} = {len(never_green)/n*100:.0f}%")
    print(f"reached >=1 ATR in profit:              {len(green1)}/{n} = {len(green1)/n*100:.0f}%")
    print(f"reached >=2 ATR in profit:              {len(green2)}/{n} = {len(green2)/n*100:.0f}%")
    print(f"went >=1 ATR green THEN closed red:     {len(gaveback)}/{n} = {len(gaveback)/n*100:.0f}%  <- late-exit signal")
    print(f"underwater by end of day 1:             {len(day1neg)}/{n} = {len(day1neg)/n*100:.0f}%  <- bad-entry signal")

    print(f"\n-- BY EXIT REASON --")
    byr = defaultdict(list)
    for t in closed: byr[t["exit_reason"]].append(t)
    for r, ts in sorted(byr.items(), key=lambda kv: -len(kv[1])):
        gb_r = [t['give_back'] for t in ts if t['give_back'] is not None]
        print(f"  {r:14s} n={len(ts):3d}  avg ret {pct(mean([t['ret'] for t in ts]))}  "
              f"win {sum(1 for t in ts if t['ret']>0)/len(ts)*100:3.0f}%  "
              f"give-back {med(gb_r)*100:.0f}%" if gb_r else
              f"  {r:14s} n={len(ts):3d}  avg ret {pct(mean([t['ret'] for t in ts]))}  "
              f"win {sum(1 for t in ts if t['ret']>0)/len(ts)*100:3.0f}%")

    print(f"\n-- BY ENTRY STRATEGY --")
    bys = defaultdict(list)
    for t in closed: bys[t["entry_strategy"]].append(t)
    for sname, ts in sorted(bys.items(), key=lambda kv: sum(x["pnl"] for x in kv[1])):
        print(f"  {sname:10s} n={len(ts):3d}  pnl Rs {sum(t['pnl'] for t in ts):>8,.0f}  "
              f"avg ret {pct(mean([t['ret'] for t in ts]))}  win {sum(1 for t in ts if t['ret']>0)/len(ts)*100:3.0f}%")

    print(f"\n-- BY ENTRY REGIME --")
    byg = defaultdict(list)
    for t in closed: byg[t["entry_regime"]].append(t)
    for g, ts in sorted(byg.items(), key=lambda kv: sum(x["pnl"] for x in kv[1])):
        print(f"  {str(g):20s} n={len(ts):3d}  pnl Rs {sum(t['pnl'] for t in ts):>8,.0f}  "
              f"avg ret {pct(mean([t['ret'] for t in ts]))}")
    return closed

if __name__ == "__main__":
    allc = {}
    for sid, nm in SESSIONS.items():
        allc[sid] = report(sid, nm)
    print("\n" + "="*72)
    print("POOLED (both portfolios = two samples of the same system)")
    print("="*72)
    pooled = [t for ts in allc.values() for t in ts]
    n = len(pooled)
    gaveback = [t for t in pooled if t["mfe_atr"] is not None and t["mfe_atr"] >= 1.0 and t["ret"] <= 0]
    never = [t for t in pooled if t["mfe_pct"] is not None and t["mfe_pct"] <= 0.005]
    day1 = [t for t in pooled if t["day1_ret"] is not None and t["day1_ret"] < 0]
    print(f"trades={n}  late-exit(>=1ATR green then red)={len(gaveback)/n*100:.0f}%  "
          f"never-green={len(never)/n*100:.0f}%  day1-negative={len(day1)/n*100:.0f}%")
