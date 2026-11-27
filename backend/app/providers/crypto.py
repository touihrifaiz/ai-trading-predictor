import httpx

async def get_crypto_candles(symbol="BTCUSDT", timeframe="5m", limit=300):
    url = "https://api.binance.com/api/v3/klines"
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params={"symbol": symbol.upper(), "interval": timeframe, "limit": limit})
        r.raise_for_status()
        rows = r.json()
    return [{"time": row[0], "open": float(row[1]), "high": float(row[2]),
             "low": float(row[3]), "close": float(row[4]), "volume": float(row[5])} for row in rows]
