from typing import List
from app.data.models import MarketOHLC


def simple_moving_average(prices: List[float], window: int) -> List[float]:
    sma = []
    for i in range(len(prices)):
        if i < window - 1:
            sma.append(None)
        else:
            sma.append(sum(prices[i-window+1:i+1]) / window)
    return sma

def average_true_range(highs, lows, closes, period=14):

    trs = [None]  # align index 0 with records

    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1])
        )
        trs.append(tr)

    atr = [None] * len(closes)

    for i in range(period, len(trs)):
        window = [tr for tr in trs[i - period + 1 : i + 1] if tr is not None]

        if len(window) == period:
            atr[i] = sum(window) / period

    return atr

