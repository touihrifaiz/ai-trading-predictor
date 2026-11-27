import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from ta.volatility import BollingerBands, AverageTrueRange

def analyze_candles(candles, symbol, timeframe, market):
    df = pd.DataFrame(candles)
    close = df["close"].astype(float)
    high, low = df["high"].astype(float), df["low"].astype(float)
    df["rsi"] = RSIIndicator(close, window=14).rsi()
    df["ema9"] = EMAIndicator(close, window=9).ema_indicator()
    df["ema21"] = EMAIndicator(close, window=21).ema_indicator()
    df["ema50"] = EMAIndicator(close, window=50).ema_indicator()
    macd = MACD(close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()
    bb = BollingerBands(close)
    df["bb_high"], df["bb_low"] = bb.bollinger_hband(), bb.bollinger_lband()
    last = df.iloc[-1]
    score = 0
    reasons = []
    if last["ema9"] > last["ema21"]:
        score += 1; reasons.append("EMA 9 أعلى من EMA 21")
    else:
        score -= 1; reasons.append("EMA 9 أسفل EMA 21")
    if last["macd"] > last["macd_signal"]:
        score += 1; reasons.append("MACD أعلى من خط الإشارة")
    else:
        score -= 1; reasons.append("MACD أسفل خط الإشارة")
    if last["rsi"] > 55:
        score += 1; reasons.append("RSI يميل إلى الزخم الصاعد")
    elif last["rsi"] < 45:
        score -= 1; reasons.append("RSI يميل إلى الزخم الهابط")
    direction = "UP" if score >= 2 else "DOWN" if score <= -2 else "NEUTRAL"
    confidence = min(70, 50 + abs(score) * 7) if direction != "NEUTRAL" else 0
    return {
        "symbol": symbol, "market": market, "timeframe": timeframe,
        "direction": direction, "up_probability": round(50 + score * 8, 1),
        "down_probability": round(50 - score * 8, 1),
        "confidence": confidence, "signal": "NO TRADE" if direction == "NEUTRAL" else ("BUY" if direction == "UP" else "SELL"),
        "last_price": float(close.iloc[-1]), "reasons": reasons,
        "indicators": {"rsi": round(float(last["rsi"]), 2), "ema9": round(float(last["ema9"]), 6),
                       "ema21": round(float(last["ema21"]), 6), "ema50": round(float(last["ema50"]), 6),
                       "macd": round(float(last["macd"]), 6)},
        "data_note": "Rule-based baseline only; scores are not calibrated probabilities and are not a trained AI model.",
        "last_candle_time": str(df.iloc[-1].get("time", "unknown"))
    }
