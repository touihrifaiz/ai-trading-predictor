def get_otc_status():
    return {
        "configured": False,
        "provider": None,
        "status": "not_configured",
        "message": "No authorized Pocket Option OTC feed is connected. Do not substitute regular EUR/USD or synthetic sample data."
    }

# Implement this adapter only for a data source you are authorized to access.
# Expected normalized candle schema:
# [{"time": ..., "open": ..., "high": ..., "low": ..., "close": ..., "volume": ...}]
