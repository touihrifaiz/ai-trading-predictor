# AI Trading Predictor

A responsive starter project for:
- Pocket Option screenshot analysis (image upload -> vision analysis)
- Separate OTC and real-market data adapters
- Candlestick chart UI
- Technical indicators and transparent rule-based baseline signals
- Prediction history and basic performance tracking

## Important limitations
- This is a runnable development scaffold, not a profitable trading system.
- Pocket Option does not provide a generally documented public developer API. The OTC adapter is intentionally disabled until you provide an authorized data feed/export. Do not use unofficial account/session-cookie automation.
- The app never places trades. It only analyzes and displays research signals.
- Screenshot-derived prices/indicators are estimates and may be unreadable. The analyzer labels uncertainty rather than inventing values.
- AI screenshot analysis requires an OpenAI API key. Market data requires a provider key or a supported public exchange feed.

## Run locally

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env for screenshot analysis
uvicorn app.main:app --reload
```

Backend: http://localhost:8000  
API docs: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend: http://localhost:5173

## Data sources
- Crypto: Binance public market candles (no key required for public market data; subject to regional/provider availability).
- Other real markets: configure Twelve Data or another licensed provider in `backend/app/providers/`.
- Pocket Option OTC: configure a provider you are authorized to use in `backend/app/providers/otc.py`. The default adapter returns `not_configured`; it does not substitute ordinary FX prices and call them OTC.

## Screenshot analyzer
The backend sends the uploaded chart image to the OpenAI vision model when `OPENAI_API_KEY` is configured. The response is constrained to JSON and includes visible observations, uncertainty, and a cautious directional assessment. This is not a guarantee of the next candle.

## Before live deployment
1. Choose/contract a market-data provider and confirm its redistribution rights.
2. Supply an authorized Pocket Option OTC data source or manual chart export workflow.
3. Add authentication, rate limits, persistent database, audit logs, monitoring, and secure secret management.
4. Train and validate models on time-ordered data with walk-forward validation, fees and slippage.
5. Calibrate probabilities on out-of-sample data. Do not interpret raw model scores as probabilities.


## Android APK build
The frontend is configured for Capacitor. The GitHub Actions workflow at `.github/workflows/android-apk.yml` builds a debug APK.
1. Push this project to a GitHub repository (main branch).
2. Deploy the backend to a public HTTPS host and set repository secret `VITE_API_BASE_URL` to its base URL (for example `https://your-api.example.com`).
3. Open GitHub → Actions → Build Android APK → run workflow (or push to main).
4. Download `ai-trading-predictor-debug-apk` from the workflow run's Artifacts.
5. Install the APK on Android. For distribution outside testing, create a signed release build.

The APK is a mobile client. Backend hosting and API keys remain separate and must not be embedded in the APK.
