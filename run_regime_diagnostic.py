"""
Per-period regime-classifier diagnostic harness.

Runs a SINGLE period through Adaptive + Adaptive+RCA, writes every
AdaptiveStrategySelector rebalance (snapshot inputs, classifier label, LLM
weights) to a JSONL log under issues/, then auto-invokes
scripts/diagnose_regime_labels.py to produce a markdown analysis next to it.

The whole point: debug ONE period at a time, see whether the regime classifier
labelled it correctly, before changing anything.

USAGE
-----
    PYTHONHASHSEED=0 finance/bin/python3 run_regime_diagnostic.py Bull
    PYTHONHASHSEED=0 finance/bin/python3 run_regime_diagnostic.py Live
    PYTHONHASHSEED=0 finance/bin/python3 run_regime_diagnostic.py Recent

Period argument is a case-insensitive substring match against PERIODS keys in
run_experiments.py — "Bull" matches "Bull  2019–2020", "Live" matches
"Live  2025–2026", etc.

OUTPUTS (under issues/, with a slugified period prefix)
    issues/<slug>_regime_labels.jsonl   — raw per-rebalance log
    issues/<slug>_run.md                — full backtest stdout
    issues/<slug>_regime_diagnostic.md  — analysis report

ENV
    PYTHONHASHSEED=0  — required (reproducibility for LLM cache hits)
    LLM_CACHE_ENABLED  — defaults to 1
    ADAPTIVE_ONLY      — defaults to 1 (no solo / EqualWeight; meta layer only)
"""
from __future__ import annotations

import io
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT   = Path(__file__).resolve().parent
ISSUES = ROOT / "issues"


def _slug(period: str) -> str:
    # "Bull  2019–2020" → "Bull_2019_2020"
    s = re.sub(r"\s+", "_", period.strip())
    s = re.sub(r"[^\w]+", "_", s, flags=re.UNICODE)
    return re.sub(r"_+", "_", s).strip("_")


def _resolve_period(query: str) -> str:
    """Match `query` (case-insensitive substring) against PERIODS keys."""
    from run_experiments import PERIODS
    q = query.strip().lower()
    matches = [k for k in PERIODS if q in k.lower()]
    if not matches:
        raise SystemExit(
            f"No period matches '{query}'. Available:\n  - "
            + "\n  - ".join(k.strip() for k in PERIODS)
        )
    if len(matches) > 1:
        raise SystemExit(
            f"'{query}' matches multiple periods — be more specific:\n  - "
            + "\n  - ".join(k.strip() for k in matches)
        )
    return matches[0]


class _Tee:
    def __init__(self, buf: io.StringIO) -> None:
        self._buf  = buf
        self._real = sys.__stdout__

    def write(self, s: str) -> int:
        self._real.write(s)
        self._buf.write(s)
        return len(s)

    def flush(self) -> None:
        self._real.flush()


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <period-substring>  (e.g. Bull, Live, Bear)")

    period_query = sys.argv[1]

    # Defaults — required for clean diagnostic runs.
    # ADAPTIVE_ONLY=0 so BOTH the plain Adaptive selector (narrow-universe
    # snapshot via build_regime_snapshot) AND the Adaptive+RCA selector (broad
    # 150-symbol enriched snapshot via RegimeContextAgent) execute. Both write
    # to the same ADAPTIVE_LOG_PATH; the analyser distinguishes them by the
    # presence of the `pct_above_sma50_broad` field (None on plain Adaptive,
    # populated on RCA). Solo strategies + EqualWeight will also run — they
    # don't touch the AdaptiveSelector so they add no log entries, just stdout.
    os.environ.setdefault("ADAPTIVE_ONLY", "0")
    os.environ.setdefault("LLM_CACHE_ENABLED", "1")

    ISSUES.mkdir(parents=True, exist_ok=True)

    period_label = _resolve_period(period_query)
    slug         = _slug(period_label)
    log_path     = ISSUES / f"{slug}_regime_labels.jsonl"
    run_md       = ISSUES / f"{slug}_run.md"
    report_md    = ISSUES / f"{slug}_regime_diagnostic.md"

    # Clear any prior log so this run's analysis isn't contaminated by an
    # earlier run's entries.
    if log_path.exists():
        log_path.unlink()

    # Critical wiring: PERIOD env var is read by both run_experiments.py (to
    # filter PERIODS) and AdaptiveSelector (to tag each JSONL row).
    os.environ["PERIOD"]            = period_label.strip()
    os.environ["ADAPTIVE_LOG_PATH"] = str(log_path)

    print(f"\n[regime-diagnostic] Period:  {period_label}")
    print(f"[regime-diagnostic] Log out: {log_path}")
    print(f"[regime-diagnostic] Report : {report_md}\n")

    # Run the backtest with stdout teed to a markdown file.
    from run_experiments import main as run_experiments_main

    buf = io.StringIO()
    sys.stdout = _Tee(buf)
    try:
        run_experiments_main()
    finally:
        sys.stdout = sys.__stdout__

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    run_md.write_text(
        f"# Regime Diagnostic Run — {period_label} — {ts}\n\n"
        f"**Period:** {period_label}  \n"
        f"**Log:** `{log_path.relative_to(ROOT)}`  \n"
        f"**Env:** `PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED','unset')}`, "
        f"`LLM_CACHE_ENABLED={os.environ.get('LLM_CACHE_ENABLED')}`, "
        f"`ADAPTIVE_ONLY={os.environ.get('ADAPTIVE_ONLY')}`\n\n"
        "```\n" + buf.getvalue() + "\n```\n"
    )

    # Invoke the analyser.
    if not log_path.is_file() or log_path.stat().st_size == 0:
        print(f"\n[regime-diagnostic] WARNING — no JSONL entries written to {log_path}.")
        print("[regime-diagnostic] The selector may not have rebalanced (LLM call count zero).")
        return

    from scripts.diagnose_regime_labels import _load, _render
    entries = _load(log_path)
    report  = _render(entries, log_path)
    report_md.write_text(report)

    print(f"\n[regime-diagnostic] Done.")
    print(f"  Raw log:    {log_path.relative_to(ROOT)}  ({len(entries)} rebalances)")
    print(f"  Full run:   {run_md.relative_to(ROOT)}")
    print(f"  Diagnostic: {report_md.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
