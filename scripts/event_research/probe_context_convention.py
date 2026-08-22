"""Can an undefined OneD/FourD pair be resolved from the document alone?

Answer, measured 2026-08-18 over all 439 UNRESOLVED_CONTEXT filings: yes, for
72% of them.  See docs/glossary/02-filings-and-xbrl.md.

Read-only: no network, no writes, no API spend.  Nothing here changes how a
filing is stored -- it measures whether the convention *could* be applied.

Discriminating test, not a precision test.

Quarters are not equal in size, so FourD/OneD will not land exactly on N.  The
question is only whether FourD spans MORE than one quarter -- i.e. is the ratio
closer to N (cumulative) than to 1 (both discrete)?  That is a wide, robust
decision, and it is the only one the parser actually needs to make.
"""
import sqlite3, statistics
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

local = lambda t: t.rsplit("}", 1)[-1]
PROBES = ("Income", "Expenses", "RevenueFromOperations", "ProfitBeforeTax")
FQ = {6: 1, 9: 2, 12: 3, 3: 4}

c = sqlite3.connect('data/event_research/event_research.sqlite')
rows = c.execute("""
  SELECT e.raw_storage_path, e.result_period_end
  FROM financial_result_events e JOIN financial_result_facts f ON f.event_id = e.id
  WHERE f.validation_status = 'UNRESOLVED_CONTEXT'
""").fetchall()

v = Counter(); observed_by_q = {}
for path, period_end in rows:
    p = Path(path); expected = FQ.get(int(period_end[5:7])) if period_end else None
    if not p.exists() or expected is None:
        v["unprobeable (missing file / odd period)"] += 1; continue
    try: root = ET.parse(p).getroot()
    except ET.ParseError: v["unparseable"] += 1; continue

    vals = {}
    for el in root.iter():
        ref = el.get("contextRef")
        if ref in ("OneD", "FourD") and (el.text or "").strip():
            vals.setdefault(local(el.tag), {})[ref] = (el.text or "").strip()

    ratios = []
    for name, pair in vals.items():
        if name not in PROBES: continue
        try: o, f = float(pair["OneD"]), float(pair["FourD"])
        except (TypeError, ValueError, KeyError): continue
        if abs(o) > 1e6: ratios.append(f / o)

    has_one = any("OneD" in pr for pr in vals.values())
    if not ratios:
        v["only OneD present (no FourD to compare)" if has_one else "neither present"] += 1
        continue

    r = statistics.median(ratios)
    observed_by_q.setdefault(expected, []).append(r)
    if expected == 1:
        v["Q1 - ratio~1 either way, assignment is harmless"] += 1
    elif abs(r - expected) < abs(r - 1.0):
        v["RESOLVED: FourD cumulative, OneD = quarter"] += 1
    else:
        v["ambiguous - kept UNRESOLVED"] += 1

print(f"{len(rows)} UNRESOLVED_CONTEXT filings\n")
for k, n in v.most_common(): print(f"  {n:5d}  {k}")
good = sum(n for k, n in v.items() if k.startswith(("RESOLVED", "Q1")))
print(f"\nrecoverable: {good}/{len(rows)} = {good/len(rows):.0%}")
print("\nmedian observed ratio by fiscal quarter (expected = the quarter number):")
for q in sorted(observed_by_q):
    xs = observed_by_q[q]
    print(f"   Q{q}: n={len(xs):3d}  median {statistics.median(xs):.2f}  (expected ~{q})")
