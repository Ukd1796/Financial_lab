"""
scripts/diagnose_regime_labels.py
=================================

Reads an ADAPTIVE_LOG_PATH JSONL produced by AdaptiveStrategySelector and emits
a markdown diagnostic into issues/. Designed to answer:

  1. What's the per-regime label distribution for this period?
  2. Are there boundary-case weeks (snapshot values right at a threshold)?
  3. When RCA is active, does the narrow universe (active 80) agree with the
     broad universe (150) on direction? If they diverge, the classifier is
     reading a biased input.
  4. How often does the regime label flip week-over-week?

No tuning, no recalibration — pure observation. Output is markdown so it slots
into the issues/ folder for human review.

USAGE
-----
    finance/bin/python3 -m scripts.diagnose_regime_labels \\
        --log issues/Bull_2019_regime_labels.jsonl \\
        --out issues/Bull_2019_regime_diagnostic.md

The runner wrapper (run_regime_diagnostic.py) calls this automatically after
the backtest finishes — direct invocation is for re-running the analysis on an
existing log without re-running the backtest.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any


# Threshold boundaries from _REGIME_RULES (kept in-sync manually — if the
# classifier rules change, update these). The diagnostic flags weeks whose
# snapshot values land within ±BOUNDARY_BAND of any threshold so we can see
# how much arbitrary classification is happening near the borders.
_THRESHOLDS = {
    "pct_downtrend":  [0.20, 0.35, 0.45],   # TRANSITION_UP / BEAR_EARLY / BEAR_CONFIRMED
    "pct_uptrend":    [0.55, 0.60],          # BULL_LOWVOL / BULL_SUSTAINED|RECOVERY
    "avg_atr_pct":    [0.015, 0.022, 0.023], # BULL_LOWVOL / BULL_SUSTAINED / CRASH_HIGHVOL
}
_BOUNDARY_BAND = 0.03   # weeks within ±3pp of any breadth threshold
_VOL_BOUNDARY  = 0.003  # ±0.3pp for ATR thresholds


def _load(log_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    with log_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def _label_distribution(entries: list[dict], key: str = "regime") -> list[tuple[str, int, float]]:
    counts = Counter(e.get(key, "UNKNOWN") for e in entries if e.get(key))
    n = sum(counts.values()) or 1
    return sorted(
        [(label, c, c / n) for label, c in counts.items()],
        key=lambda r: -r[1],
    )


def _is_rca_entry(e: dict) -> bool:
    """Adaptive+RCA entries carry the broad-universe enrichments."""
    return e.get("pct_above_sma50_broad") is not None


def _classify_from_broad(e: dict) -> str | None:
    """
    Apply the *same* _REGIME_RULES logic but using BROAD-universe inputs:
      pct_uptrend       ← pct_above_sma50_broad
      pct_downtrend     ← (1 - pct_above_sma50_broad)   (proxy — see note)
      avg_atr_pct       ← avg_rolling_vol_5d
      trend             ← unchanged (already broad-derived)

    The downtrend proxy is (1 - pct_above_sma50_broad), NOT
    (1 - advance_decline_ratio). advance_decline_ratio is a single-day
    positive-return ratio (very noisy: ranges 0.08–0.90 day-to-day even in a
    sustained trend), so it's not a regime-style signal. pct_above_sma50_broad
    is a multi-day price-vs-MA signal — its complement (% below SMA50) is the
    closest broad analog to the narrow `pct_downtrend` (% of active set in a
    multi-day DOWNTREND regime).

    Returns None when broad data isn't present for this entry. Rules are
    duplicated here intentionally rather than imported so the analyser is
    standalone and doesn't carry forward bugs from rule edits.
    """
    if not _is_rca_entry(e):
        return None
    up    = e.get("pct_above_sma50_broad")
    vol   = e.get("avg_rolling_vol_5d")
    if up is None or vol is None:
        return None
    down  = 1.0 - up
    trend = e.get("trend")

    if down > 0.35 and vol > 0.023:
        return "CRASH_HIGHVOL"
    if trend == "IMPROVING" and down > 0.20:
        return "TRANSITION_UP"
    if down > 0.45:
        return "BEAR_CONFIRMED"
    if 0.35 <= down <= 0.45:
        return "BEAR_EARLY"
    if up > 0.60 and vol > 0.022:
        return "RECOVERY"
    if up > 0.60 and vol <= 0.022:
        return "BULL_SUSTAINED"
    if up > 0.55 and vol < 0.015:
        return "BULL_LOWVOL"
    if up > 0.55:
        return "BULL_MEDVOL"
    return "MIXED"


def _broad_implied_disagreement(entries: list[dict]) -> list[dict]:
    """Weeks where narrow-keyed label differs from a synthesized broad-keyed label."""
    out = []
    for e in entries:
        broad_implied = _classify_from_broad(e)
        narrow_label  = e.get("regime")
        if broad_implied and narrow_label and broad_implied != narrow_label:
            out.append({
                "date":          e.get("date"),
                "narrow":        narrow_label,
                "broad_implied": broad_implied,
                "pct_uptrend":   e.get("pct_uptrend"),
                "pct_above_sma50_broad": e.get("pct_above_sma50_broad"),
                "avg_atr_pct":   e.get("avg_atr_pct"),
                "avg_rolling_vol_5d": e.get("avg_rolling_vol_5d"),
            })
    return out


def _dedupe_by_date(entries: list[dict]) -> list[dict]:
    """
    Keep the first entry per date. The log contains two records per rebalance
    date — one from plain Adaptive, one from Adaptive+RCA — and the per-date
    sections (boundary cases, transitions) should treat the period as a single
    timeline rather than double-count.
    """
    seen: set = set()
    out: list[dict] = []
    for e in entries:
        d = e.get("date")
        if d and d not in seen:
            seen.add(d)
            out.append(e)
    return out


def _boundary_cases(entries: list[dict]) -> list[dict]:
    """Weeks whose snapshot values sit near a classifier threshold."""
    flagged = []
    for e in entries:
        notes = []
        for field, thresholds in _THRESHOLDS.items():
            v = e.get(field)
            if v is None:
                continue
            band = _VOL_BOUNDARY if field == "avg_atr_pct" else _BOUNDARY_BAND
            for t in thresholds:
                if abs(v - t) <= band:
                    notes.append(f"{field}={v:.3f} (≈{t:.3f})")
        if notes:
            flagged.append({
                "date":   e.get("date"),
                "label":  e.get("regime"),
                "notes":  notes,
            })
    return flagged


def _narrow_vs_broad(entries: list[dict]) -> dict[str, Any] | None:
    """Compare active-80 pct_uptrend vs broad-150 pct_above_sma50_broad."""
    pairs = [
        (e["pct_uptrend"], e["pct_above_sma50_broad"])
        for e in entries
        if e.get("pct_uptrend") is not None
        and e.get("pct_above_sma50_broad") is not None
    ]
    if not pairs:
        return None
    deltas = [n - b for n, b in pairs]
    abs_dev = [abs(d) for d in deltas]
    return {
        "n":            len(pairs),
        "mean_delta":   mean(deltas),
        "max_abs":      max(abs_dev),
        "mean_abs":     mean(abs_dev),
        "narrow_higher_pct": sum(1 for d in deltas if d > 0.05) / len(deltas),
        "broad_higher_pct":  sum(1 for d in deltas if d < -0.05) / len(deltas),
    }


def _transitions(entries: list[dict]) -> tuple[int, list[tuple[str, str, str]]]:
    """Count and list label changes week-over-week."""
    transitions: list[tuple[str, str, str]] = []
    for prev, curr in zip(entries, entries[1:]):
        p_lbl = prev.get("regime")
        c_lbl = curr.get("regime")
        if p_lbl and c_lbl and p_lbl != c_lbl:
            transitions.append((curr.get("date", ""), p_lbl, c_lbl))
    return len(transitions), transitions


def _broad_vs_narrow_label_disagreement(entries: list[dict]) -> list[dict]:
    """Weeks where `regime` (narrow-derived) and `broad_regime` (RCA) differ."""
    out = []
    for e in entries:
        nl = e.get("regime")
        bl = e.get("broad_regime")
        if nl and bl and nl != bl:
            out.append({
                "date":          e.get("date"),
                "narrow_label":  nl,
                "broad_label":   bl,
                "pct_uptrend":   e.get("pct_uptrend"),
                "pct_above_sma50_broad": e.get("pct_above_sma50_broad"),
            })
    return out


def _render(entries: list[dict], log_path: Path) -> str:
    if not entries:
        return f"# Regime Diagnostic\n\nNo entries in `{log_path}`.\n"

    period = entries[0].get("period") or "(no period tag)"
    start  = entries[0].get("date")
    end    = entries[-1].get("date")
    ts     = datetime.now().strftime("%Y-%m-%d %H:%M")

    # The log contains entries from BOTH the plain Adaptive selector AND the
    # Adaptive+RCA selector (one of each per rebalance date). Per-date sections
    # (boundary cases, transitions) need a deduped timeline to avoid double-
    # counting; per-source sections (§1, §3, §4, §4b) handle the split themselves.
    deduped = _dedupe_by_date(entries)

    dist        = _label_distribution(deduped)
    boundary    = _boundary_cases(deduped)
    nb          = _narrow_vs_broad(entries)
    n_trans, transitions = _transitions(deduped)
    disagreement = _broad_vs_narrow_label_disagreement(entries)

    lines: list[str] = []
    add = lines.append

    add(f"# Regime-Classifier Diagnostic — {period}")
    add("")
    add(f"**Generated:** {ts}  ")
    add(f"**Log:** `{log_path}`  ")
    add(f"**Date range:** {start} → {end}  ")
    add(f"**Rebalances logged:** {len(entries)} raw / {len(_dedupe_by_date(entries))} unique dates  ")
    add(f"**Note on broad-implied labels (§1, §4b):** the broad downtrend signal "
        f"is approximated as `1 - pct_above_sma50_broad`, which includes SIDEWAYS "
        f"stocks (not only DOWNTREND). This *overstates* BEAR_* counts in the "
        f"broad-implied column. BULL_SUSTAINED / TRANSITION_UP / RECOVERY counts "
        f"are robust (their rules don't depend on the down proxy).")
    add("")
    add("---")
    add("")

    add("## 1. Label distribution")
    add("")
    # Split entries by source so the user sees plain-Adaptive (narrow snapshot)
    # vs Adaptive+RCA (broad snapshot) populations distinctly. Same-week LLM
    # calls in both selectors → entries are roughly 2× the rebalance count.
    narrow_entries = [e for e in entries if not _is_rca_entry(e)]
    rca_entries    = [e for e in entries if _is_rca_entry(e)]
    add(f"Source split: **{len(narrow_entries)}** plain-Adaptive (narrow snapshot) + "
        f"**{len(rca_entries)}** Adaptive+RCA (broad snapshot enrichments).")
    add("")
    if narrow_entries and rca_entries:
        n_dist = _label_distribution(narrow_entries, "regime")
        r_dist = _label_distribution(rca_entries,    "regime")
        b_dist = _label_distribution(
            [{"regime": _classify_from_broad(e)} for e in rca_entries
             if _classify_from_broad(e)], "regime"
        )
        all_labels = sorted({l for L in (n_dist, r_dist, b_dist) for l, _, _ in L})
        n_map = {l: (c, p) for l, c, p in n_dist}
        r_map = {l: (c, p) for l, c, p in r_dist}
        b_map = {l: (c, p) for l, c, p in b_dist}
        add("| Regime | Adaptive (narrow) | Adaptive+RCA (narrow) | **Broad-implied** if classifier read broad keys |")
        add("|---|---|---|---|")
        for label in all_labels:
            n = n_map.get(label, (0, 0))
            r = r_map.get(label, (0, 0))
            b = b_map.get(label, (0, 0))
            add(f"| `{label}` | {n[0]} ({n[1]:.0%}) | {r[0]} ({r[1]:.0%}) | **{b[0]} ({b[1]:.0%})** |")
        add("")
        add("> The right column is the dispositive evidence. It applies the same "
            "`_REGIME_RULES` logic to the broad-universe inputs (`pct_above_sma50_broad`, "
            "`avg_rolling_vol_5d`, derived broad downtrend) — i.e. what the classifier "
            "would have labelled if it read the 150-stock breadth instead of the 80-stock "
            "active subset.")
        add("")
    else:
        for label, c, pct in dist:
            add(f"| `{label}` | {c} | {pct:.1%} |")
        add("")

    add("## 2. Boundary cases — weeks sitting near a classifier threshold")
    add("")
    add(f"Weeks within ±{_BOUNDARY_BAND:.0%} of a breadth threshold or ±{_VOL_BOUNDARY:.1%} of "
        "an ATR threshold. High count here means small input changes are flipping labels — "
        "classifier is sensitive at the boundary.")
    add("")
    add(f"**Total boundary weeks: {len(boundary)} / {len(entries)} "
        f"({len(boundary)/max(len(entries),1):.0%})**")
    add("")
    if boundary:
        add("| Date | Label | Near-threshold values |")
        add("|---|---|---|")
        for b in boundary[:30]:
            add(f"| {b['date']} | `{b['label']}` | {'; '.join(b['notes'])} |")
        if len(boundary) > 30:
            add(f"| … | … | (+{len(boundary)-30} more — see JSONL for full list) |")
        add("")

    add("## 3. Narrow vs broad universe agreement")
    add("")
    if nb is None:
        add("RCA was not active for this run — no broad-universe data present in the log.")
        add("")
    else:
        add(f"Compared **pct_uptrend** (active 80) vs **pct_above_sma50_broad** (150) "
            f"across {nb['n']} rebalances:")
        add("")
        add(f"- Mean signed Δ (narrow − broad): **{nb['mean_delta']:+.3f}**")
        add(f"- Mean abs Δ: **{nb['mean_abs']:.3f}**")
        add(f"- Max abs Δ: **{nb['max_abs']:.3f}**")
        add(f"- Weeks where narrow exceeds broad by >5pp (upward bias): "
            f"**{nb['narrow_higher_pct']:.0%}**")
        add(f"- Weeks where broad exceeds narrow by >5pp: **{nb['broad_higher_pct']:.0%}**")
        add("")
        if abs(nb["mean_delta"]) > 0.03:
            add(f"> ⚠️ Mean delta is **{nb['mean_delta']:+.3f}** — the active-80 universe is "
                "systematically biased. If positive, the classifier sees a brighter market than "
                "the broad universe actually shows.")
            add("")

    add("## 4. Narrow vs broad LABEL disagreement (regime vs broad_regime)")
    add("")
    if not disagreement:
        add("No disagreements logged — either RCA was off, or narrow and broad classifiers "
            "agreed on every rebalance.")
    else:
        add(f"**{len(disagreement)} rebalances** had different labels between the narrow-keyed "
            "classifier (`regime`) and the broad-snapshot classifier (`broad_regime`):")
        add("")
        add("| Date | Narrow label | Broad label | pct_uptrend | pct_above_sma50_broad |")
        add("|---|---|---|---:|---:|")
        for d in disagreement[:30]:
            n_pct = f"{d['pct_uptrend']:.3f}" if d['pct_uptrend'] is not None else "—"
            b_pct = f"{d['pct_above_sma50_broad']:.3f}" if d['pct_above_sma50_broad'] is not None else "—"
            add(f"| {d['date']} | `{d['narrow_label']}` | `{d['broad_label']}` | {n_pct} | {b_pct} |")
        if len(disagreement) > 30:
            add(f"| … | … | … | … | (+{len(disagreement)-30} more) |")
    add("")

    add("## 4b. Per-week narrow vs **broad-implied** label disagreement")
    add("")
    add("For each Adaptive+RCA rebalance, compare the actual label (derived from "
        "narrow-universe inputs as the live classifier does today) against the label "
        "this rebalance *would have received* if `_REGIME_RULES` consumed broad inputs.")
    add("")
    broad_dis = _broad_implied_disagreement(entries)
    if not rca_entries:
        add("Adaptive+RCA produced no entries in this log (run with `ADAPTIVE_ONLY=0` "
            "to enable). No comparison possible.")
    else:
        n_rca = len(rca_entries)
        pct = len(broad_dis) / max(n_rca, 1)
        add(f"**{len(broad_dis)} of {n_rca} RCA rebalances** ({pct:.0%}) would be "
            "labelled differently under broad inputs.")
        add("")
        if broad_dis:
            add("| Date | Narrow label | Broad-implied | pct_uptrend / pct_above_sma50 | atr / vol_5d |")
            add("|---|---|---|---|---|")
            for d in broad_dis[:40]:
                up_n = f"{d['pct_uptrend']:.2f}" if d.get('pct_uptrend') is not None else "—"
                up_b = f"{d['pct_above_sma50_broad']:.2f}" if d.get('pct_above_sma50_broad') is not None else "—"
                atr  = f"{d['avg_atr_pct']:.3f}" if d.get('avg_atr_pct') is not None else "—"
                vol  = f"{d['avg_rolling_vol_5d']:.3f}" if d.get('avg_rolling_vol_5d') is not None else "—"
                add(f"| {d['date']} | `{d['narrow']}` | `{d['broad_implied']}` | {up_n} / {up_b} | {atr} / {vol} |")
            if len(broad_dis) > 40:
                add(f"| … | … | … | … | (+{len(broad_dis)-40} more — see JSONL) |")
    add("")

    add("## 5. Regime transitions (week-over-week label changes)")
    add("")
    add(f"**Total transitions: {n_trans}** across {len(deduped)} unique-date rebalances "
        f"(stability = {(1 - n_trans/max(len(deduped)-1,1)):.0%})")
    add("")
    if transitions:
        add("| Date | From | To |")
        add("|---|---|---|")
        for date, frm, to in transitions[:30]:
            add(f"| {date} | `{frm}` | `{to}` |")
        if len(transitions) > 30:
            add(f"| … | … | (+{len(transitions)-30} more) |")
    add("")

    add("## 6. What to look for in this report")
    add("")
    add("- **Distribution skew** (§1): if a period everyone calls a 'bull' is "
        "labelled MIXED 70% of the time, the classifier is mis-labelling.")
    add("- **High boundary count** (§2): means small noise flips labels — "
        "the threshold values may need adjustment.")
    add("- **Narrow vs broad mean delta** (§3): if narrow is consistently higher "
        "than broad, the active-80 upward-bias hypothesis is confirmed and "
        "switching the classifier to broad keys is justified.")
    add("- **Label disagreement count** (§4): direct evidence of narrow vs broad "
        "divergence — each row is a week the two universes saw different markets.")
    add("- **Many transitions** (§5): if labels flip > 30% of weeks, the "
        "`regime_stability_weeks=2` gate may be masking real instability.")
    add("")

    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--log", required=True, type=Path, help="JSONL log to read")
    ap.add_argument("--out", required=True, type=Path, help="Markdown report to write")
    args = ap.parse_args()

    if not args.log.is_file():
        raise SystemExit(f"Log file not found: {args.log}")

    entries = _load(args.log)
    report  = _render(entries, args.log)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report)
    print(f"Wrote {args.out}  ({len(entries)} entries analysed)")


if __name__ == "__main__":
    main()
