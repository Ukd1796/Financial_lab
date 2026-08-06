"""A/B the meta-layer vol-swap over Recovery + Bear (branch code).
Toggle via META_VOL=narrow|broad (see adaptive_selector._vol)."""
from datetime import datetime
import run_ujjwal_baseline as rb

rb.PERIODS = {
    "Recov 2020-2021": (datetime(2020, 4, 1),  datetime(2021, 12, 31)),
    "Bear  2022     ": (datetime(2022, 1, 1),  datetime(2022, 12, 31)),
}

if __name__ == "__main__":
    rb.run_baseline(equal_weight_only=False)  # EqW (control) + Adaptive+RCA
