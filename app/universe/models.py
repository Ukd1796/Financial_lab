from dataclasses import dataclass


@dataclass
class UniverseCandidate:
    """
    A single symbol that passed the volume + volatility filters
    for a given trading day, along with its ranking signals.
    """
    symbol:          str
    score:           float   # composite ranking score
    relative_volume: float   # today_volume / avg_volume_20d
    daily_return:    float   # (close - prev_close) / prev_close
    atr_ratio:       float   # atr_14 / close  (range relative to price)
