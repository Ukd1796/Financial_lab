from typing import List, Optional
from app.data.models import MarketOHLC


def simple_moving_average(prices: List[float], window: int) -> List[Optional[float]]:
    sma = []
    for i in range(len(prices)):
        if i < window - 1:
            sma.append(None)
        else:
            sma.append(sum(prices[i - window + 1 : i + 1]) / window)
    return sma


def average_true_range(
    highs: List[float],
    lows: List[float],
    closes: List[float],
    period: int = 14,
) -> List[Optional[float]]:

    trs = [None]  # index 0 has no previous close

    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        trs.append(tr)

    atr = [None] * len(closes)

    for i in range(period, len(trs)):
        window = [tr for tr in trs[i - period + 1 : i + 1] if tr is not None]
        if len(window) == period:
            atr[i] = sum(window) / period

    return atr


def relative_strength_index(
    prices: List[float],
    period: int,
) -> List[Optional[float]]:
    """
    Standard RSI using simple rolling averages of gains and losses over
    `period` price changes (requires period + 1 prices to produce first value).

    RSI = 100 - (100 / (1 + RS))
    RS  = avg_gain / avg_loss  over the window

    Returns None for indices with insufficient history.
    """
    rsi: List[Optional[float]] = [None] * len(prices)

    for i in range(period, len(prices)):
        gains  = 0.0
        losses = 0.0
        for j in range(i - period + 1, i + 1):
            delta = prices[j] - prices[j - 1]
            if delta > 0:
                gains  += delta
            else:
                losses += abs(delta)

        avg_gain = gains  / period
        avg_loss = losses / period

        if avg_loss == 0:
            rsi[i] = 100.0
        else:
            rs     = avg_gain / avg_loss
            rsi[i] = 100.0 - (100.0 / (1.0 + rs))

    return rsi

