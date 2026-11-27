import base64, json
from openai import AsyncOpenAI
from .settings import settings

SYSTEM_PROMPT = '''
You are a cautious chart-image analyst. Inspect only what is visible in the uploaded trading screenshot.
Never invent exact prices, indicators, timestamps, volume, or hidden candles. If text is unreadable, say so.
Distinguish observations from inference. Do not claim certainty or guaranteed profit.
Return JSON with keys: market_context, symbol_seen, timeframe_seen, visible_observations (array),
patterns (array), support_resistance (array), indicators_read (object), next_candle_assessment
(object with direction UP/DOWN/NEUTRAL, up_probability null or number, down_probability null or number,
confidence LOW/MEDIUM/HIGH, signal BUY/SELL/NO TRADE), reasons (array), limitations (array).
Probabilities must be null unless there is enough clear information to make a defensible estimate.
When uncertain, choose NEUTRAL and NO TRADE.
'''

async def analyze_screenshot(raw: bytes, mime: str, market: str, timeframe: str, symbol: str):
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Add it to backend/.env.")
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    data_url = f"data:{mime};base64,{base64.b64encode(raw).decode()}"
    response = await client.chat.completions.create(
        model=settings.openai_vision_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": f"User context: market={market}, timeframe={timeframe}, symbol={symbol}. Analyze the screenshot."},
                {"type": "image_url", "image_url": {"url": data_url, "detail": "high"}}
            ]}
        ],
        temperature=0.1
    )
    result = json.loads(response.choices[0].message.content)
    result["analysis_mode"] = "screenshot_vision"
    result["disclaimer"] = "Image-only assessment; not a live feed and not a guarantee of the next candle."
    return result
