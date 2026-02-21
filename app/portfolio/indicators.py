def average_true_range(highs, lows, closes, period=14):

    trs = []

    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i-1]),
            abs(lows[i] - closes[i-1])
        )
        trs.append(tr)

    atr = [None] * period

    for i in range(period, len(trs)):
        atr.append(sum(trs[i-period:i]) / period)

    return atr
