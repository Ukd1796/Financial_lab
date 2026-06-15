"""
Meta-layer recalibration verification harness.

Runs `run_experiments.py` in ADAPTIVE_ONLY mode (Adaptive + Adaptive+RCA only,
across all 7 periods) and appends the full output to
`docs/meta_recalibration_test.md` with a timestamped header.

This is the verification companion to the 2026-05-30 recalibration of
`_STRATEGY_REGIME_PERFORMANCE` / `_REGIME_ALLOCATION_RULES` /
`_REGIME_WEIGHT_BOUNDS` in `app/meta/adaptive_selector.py`. EqualWeight + solo
strategies are skipped because they do not exercise the meta layer.

Run:
    PYTHONHASHSEED=0 finance/bin/python3 run_meta_recalibration_test.py

Env vars (set automatically if unset):
    ADAPTIVE_ONLY=1      — skip EqualWeight + solo (must — meta-only test)
    LLM_CACHE_ENABLED=1  — disk-cached LLM calls (cache key is sensitive to
                           the recalibrated prompt content, so the first run
                           will populate fresh cache entries)

To re-run the prior bounds for an A/B baseline, temporarily swap
`_REGIME_WEIGHT_BOUNDS` ↔ `PRIOR_REGIME_WEIGHT_BOUNDS` in adaptive_selector.py
and re-run this script — the doc-append keeps both runs side-by-side.
"""
from __future__ import annotations

import io
import os
import sys
from datetime import datetime
from pathlib import Path

# Default env BEFORE importing run_experiments (it reads env at import time).
#
# ADAPTIVE_ONLY=0 so the Adaptive+RCA block in run_experiments.py:1095 actually
# executes (it's gated on `not ADAPTIVE_ONLY`). Required for any change that
# depends on broad-universe inputs (`pct_above_sma50_broad`,
# `avg_rolling_vol_5d`) to be visible in the comparison — plain Adaptive
# operates on the narrow snapshot only.
#
# Cost: solo strategies + EqualWeight also run (they don't use the meta layer),
# adding ~30-60s per period. For the 7-period suite that's an extra ~5 min vs
# the prior ADAPTIVE_ONLY=1 setting. Worth it — the prior runs missed the RCA
# selector entirely.
os.environ.setdefault("ADAPTIVE_ONLY", "0")
os.environ.setdefault("LLM_CACHE_ENABLED", "1")

ROOT = Path(__file__).resolve().parent
DOC  = ROOT / "docs" / "meta_recalibration_test.md"


class _Tee:
    """Mirror every write to both real stdout and an in-memory buffer."""

    def __init__(self, buf: io.StringIO) -> None:
        self._buf  = buf
        self._real = sys.__stdout__

    def write(self, s: str) -> int:
        self._real.write(s)
        self._buf.write(s)
        return len(s)

    def flush(self) -> None:
        self._real.flush()


def _header(ts: str) -> str:
    return (
        "\n\n---\n\n"
        f"## Meta Recalibration Test — {ts}\n\n"
        "**Mode:** ADAPTIVE_ONLY (Adaptive + Adaptive+RCA across all 7 periods)  \n"
        "**Tables:** recalibrated `_STRATEGY_REGIME_PERFORMANCE` + "
        "`_REGIME_WEIGHT_BOUNDS` (see `app/meta/adaptive_selector.py`)  \n"
        "**Costs:** 0.10% commission + 0.05% slippage per side  \n"
        f"**Env:** `PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED', 'unset')}`, "
        f"`LLM_CACHE_ENABLED={os.environ.get('LLM_CACHE_ENABLED')}`, "
        f"`ADAPTIVE_ONLY={os.environ.get('ADAPTIVE_ONLY')}`\n\n"
        "```\n"
    )


def main() -> None:
    from run_experiments import main as run_experiments_main

    buf = io.StringIO()
    sys.stdout = _Tee(buf)
    try:
        run_experiments_main()
    finally:
        sys.stdout = sys.__stdout__

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    DOC.parent.mkdir(parents=True, exist_ok=True)
    with DOC.open("a") as f:
        f.write(_header(ts) + buf.getvalue() + "\n```\n")

    print(f"\n  Results appended to {DOC.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
