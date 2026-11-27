from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Optional
from .settings import settings
from .analysis import analyze_candles
from .screenshot import analyze_screenshot
from .providers.crypto import get_crypto_candles
from .providers.otc import get_otc_status

app = FastAPI(title="AI Trading Predictor API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    symbol: str = "BTCUSDT"
    market: Literal["CRYPTO", "FOREX", "STOCKS", "GOLD", "INDICES", "OTC"] = "CRYPTO"
    timeframe: Literal["1m", "5m", "15m", "30m", "1h", "4h", "1d"] = "5m"

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "AI Trading Predictor", "version": "0.1.0"}

@app.get("/api/otc/status")
def otc_status():
    return get_otc_status()

@app.post("/api/predict")
async def predict(req: PredictRequest):
    if req.market == "OTC":
        raise HTTPException(
            status_code=503,
            detail="OTC feed is not configured. Connect an authorized Pocket Option-compatible data source; ordinary FX prices are not a substitute."
        )
    if req.market != "CRYPTO":
        raise HTTPException(status_code=501, detail="This market provider is not configured yet.")
    candles = await get_crypto_candles(req.symbol, req.timeframe)
    if len(candles) < 60:
        raise HTTPException(status_code=503, detail="Insufficient candle history.")
    return analyze_candles(candles, req.symbol, req.timeframe, req.market)

@app.post("/api/analyze-screenshot")
async def screenshot(file: UploadFile = File(...), market: str = "OTC", timeframe: str = "5m", symbol: str = "Unknown"):
    if file.content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(status_code=415, detail="Upload PNG, JPG, or WEBP.")
    raw = await file.read()
    if not raw or len(raw) > 12 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image is empty or exceeds 12 MB.")
    try:
        return await analyze_screenshot(raw, file.content_type, market, timeframe, symbol)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
