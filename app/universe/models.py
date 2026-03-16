from dataclasses import dataclass, field


@dataclass
class UniverseCandidate:
    """
    A single symbol that passed the volume + volatility filters
    for a given trading day, along with its ranking signals.

    Core signals (always populated):
      relative_volume         — today_volume / avg_volume_20d
      daily_return            — (close - prev_close) / prev_close
      atr_ratio               — atr_14 / close  (range relative to price)

    Trend signals (populated by DynamicUniverseAgent; used by per-strategy filters):
      sma_20_above_sma_50     — True when stock is in a medium-term uptrend
      sma_20_slope_positive   — True when SMA_20 is still rising (trend accelerating)
      return_3d               — 3-day return; negative = stock pulling back
      rolling_vol_5d          — 5-day realised volatility (activity level)
    """
    symbol:                str
    score:                 float   # composite ranking score
    relative_volume:       float   # today_volume / avg_volume_20d
    daily_return:          float   # (close - prev_close) / prev_close
    atr_ratio:             float   # atr_14 / close  (range relative to price)

    # Trend / momentum signals — default to neutral so existing call sites
    # that don't supply them remain valid.
    sma_20_above_sma_50:   bool  = field(default=False)
    sma_20_slope_positive: bool  = field(default=False)
    return_3d:             float = field(default=0.0)
    rolling_vol_5d:        float = field(default=0.0)
