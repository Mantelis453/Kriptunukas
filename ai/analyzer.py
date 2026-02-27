"""
AI-powered trading analysis using Google Gemini API.
"""
import json
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")


def get_ai_signal(
    symbol: str,
    indicators: Dict,
    current_position: Optional[Dict],
    portfolio_balance: float,
    config: Dict
) -> Dict:
    """
    Get AI trading signal using Google Gemini API.

    Args:
        symbol: Trading pair symbol
        indicators: Dictionary of calculated technical indicators
        current_position: Current open position or None
        portfolio_balance: Available portfolio balance
        config: AI configuration

    Returns:
        Dictionary with action, confidence, reasoning, and trade parameters
    """
    start_time = time.time()

    try:
        # Check if Gemini is available
        if not GEMINI_AVAILABLE:
            return _default_hold_signal(
                symbol,
                "Gemini API not available",
                "",
                "google-generativeai package not installed",
                0
            )

        # Get API key from config
        api_key = config.get('gemini_api_key')
        if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
            return _default_hold_signal(
                symbol,
                "Gemini API key not configured",
                "",
                "Please add gemini_api_key to config.yaml",
                0
            )

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Build the prompt
        prompt = _build_prompt(symbol, indicators, current_position, portfolio_balance)

        # Get model name from config (default to gemini-2.5-flash)
        # Note: Use just 'gemini-2.5-flash' not 'models/gemini-2.5-flash'
        model_name = config.get('model', 'gemini-2.5-flash')

        # Call Gemini API
        logger.info(f"Calling Gemini API ({model_name}) for {symbol} analysis...")

        model = genai.GenerativeModel(model_name)

        # Generate response
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # Lower temperature for more consistent outputs
                top_p=0.8,
                top_k=40,
                max_output_tokens=1024,
            )
        )

        # Calculate latency
        latency_ms = int((time.time() - start_time) * 1000)

        # Get response text
        response_text = response.text.strip()

        # Log the raw response for debugging
        logger.debug(f"Raw AI response: {response_text[:500]}")

        # Parse JSON response
        signal = _parse_ai_response(response_text)

        # Add metadata
        signal['symbol'] = symbol
        signal['indicators'] = indicators
        signal['ai_raw_response'] = response_text
        signal['prompt_version'] = config.get('prompt_version', 'v1')
        signal['latency_ms'] = latency_ms

        logger.info(
            f"AI Signal for {symbol}: {signal['action']} "
            f"(confidence: {signal['confidence']}%)"
        )

        return signal

    except Exception as e:
        logger.error(f"Error getting AI signal: {e}")
        latency_ms = int((time.time() - start_time) * 1000)
        return _default_hold_signal(
            symbol,
            f"Error: {str(e)}",
            prompt if 'prompt' in locals() else "",
            str(e),
            latency_ms
        )


def _build_prompt(
    symbol: str,
    indicators: Dict,
    current_position: Optional[Dict],
    portfolio_balance: float
) -> str:
    """
    Build detailed prompt for Gemini API.

    Args:
        symbol: Trading pair symbol
        indicators: Technical indicators dictionary
        current_position: Current position or None
        portfolio_balance: Available balance

    Returns:
        Formatted prompt string
    """
    # Extract indicators
    price = indicators.get('current_price', 0)
    rsi = indicators.get('rsi', 0)
    macd = indicators.get('macd', {})
    bb = indicators.get('bollinger_bands', {})
    ema = indicators.get('ema', {})
    atr = indicators.get('atr', 0)
    volume = indicators.get('volume', {})
    trend = indicators.get('trend', 'NEUTRAL')
    sr = indicators.get('support_resistance', {})
    candles = indicators.get('last_10_candles', [])

    # Format position details
    if current_position:
        position_str = (
            f"OPEN {current_position.get('side', 'LONG')} - "
            f"Size: {current_position.get('size', 0)}, "
            f"Entry: {current_position.get('entry_price', 0)}, "
            f"PnL: {current_position.get('unrealized_pnl', 0)}"
        )
    else:
        position_str = "NONE"

    # Format candles
    candles_str = "\n".join([
        f"  {i+1}. O:{c['open']} H:{c['high']} L:{c['low']} C:{c['close']} "
        f"V:{c['volume']} ({c['type']}, body:{c['body_percent']}%)"
        for i, c in enumerate(candles)
    ])

    # Build prompt
    prompt = f"""You are a systematic crypto trading analyst. You analyze technical indicators and market structure to generate precise trading signals. You are conservative and risk-averse. You ONLY respond with valid JSON, no other text.

MARKET DATA:
Symbol: {symbol}
Current Price: {price}
Timeframe: 1h

TECHNICAL INDICATORS:
- RSI(14): {rsi}
- MACD Line: {macd.get('line', 0)}, Signal: {macd.get('signal', 0)}, Histogram: {macd.get('histogram', 0)}
- Bollinger Bands: Upper {bb.get('upper', 0)}, Middle {bb.get('middle', 0)}, Lower {bb.get('lower', 0)}
- BB Position: {bb.get('position', 50)}% (0=at lower band, 100=at upper band)
- EMA 20: {ema.get('ema_20', 0)}, EMA 50: {ema.get('ema_50', 0)}, EMA 200: {ema.get('ema_200', 'N/A')}
- ATR(14): {atr}
- Volume Ratio: {volume.get('ratio', 1)}x average
- Overall Trend: {trend}
- Support Levels: {sr.get('support', [])}
- Resistance Levels: {sr.get('resistance', [])}

RECENT CANDLES (newest last):
{candles_str}

CURRENT POSITION: {position_str}
PORTFOLIO BALANCE: {portfolio_balance} USDT

TRADING RULES:
1. BUY signals: Only when trend is BULLISH, or NEUTRAL with RSI < 35 and price near BB lower band
2. SELL/close signals: When RSI > 70, or price hits BB upper band in bearish trend, or trend reversal confirmed
3. Stop-loss: Place at 1.5x ATR below entry for longs, above for shorts
4. Take-profit: Minimum 2:1 reward-to-risk ratio
5. Position size: 1-5% of portfolio based on confidence
6. HOLD if uncertain - never force a trade
7. If in a position, evaluate whether to HOLD, CLOSE, or ADJUST stop-loss
8. Confidence must be 0-100. Only signal BUY or SELL if confidence >= 70

Respond with ONLY this JSON (no markdown, no code blocks, just raw JSON):
{{"action": "BUY" | "SELL" | "HOLD" | "CLOSE", "confidence": 0-100, "reasoning": "2-3 sentence explanation", "entry_price": number_or_null, "stop_loss": number_or_null, "take_profit": number_or_null, "position_size_pct": 1-5_or_null, "adjust_stop_loss": number_or_null}}"""

    return prompt


def _parse_ai_response(response_text: str) -> Dict:
    """
    Parse AI response JSON.

    Args:
        response_text: Raw response from Gemini API

    Returns:
        Parsed signal dictionary

    Raises:
        ValueError: If JSON parsing fails
    """
    try:
        # Remove markdown code blocks if present
        response_text = response_text.replace('```json', '').replace('```', '').strip()

        # Try to extract JSON from response (in case there's extra text)
        # Look for { ... } pattern
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')

        if start_idx == -1 or end_idx == -1:
            raise ValueError("No JSON object found in response")

        json_str = response_text[start_idx:end_idx + 1]
        signal = json.loads(json_str)

        # Validate required fields
        required_fields = ['action', 'confidence', 'reasoning']
        for field in required_fields:
            if field not in signal:
                raise ValueError(f"Missing required field: {field}")

        # Validate action
        valid_actions = ['BUY', 'SELL', 'HOLD', 'CLOSE']
        if signal['action'] not in valid_actions:
            logger.warning(f"Invalid action: {signal['action']}, defaulting to HOLD")
            signal['action'] = 'HOLD'

        # Ensure confidence is in range
        signal['confidence'] = max(0, min(100, int(signal['confidence'])))

        return signal

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Response text: {response_text[:500]}")
        raise ValueError(f"Invalid JSON response: {e}")

    except Exception as e:
        logger.error(f"Error parsing AI response: {e}")
        logger.error(f"Full response: {response_text[:1000]}")
        raise


def _default_hold_signal(
    symbol: str,
    reason: str,
    prompt: str,
    response: str,
    latency_ms: int
) -> Dict:
    """
    Return a default HOLD signal when AI call fails.

    Args:
        symbol: Trading pair symbol
        reason: Reason for default signal
        prompt: The prompt that was sent
        response: The error response
        latency_ms: Call latency in milliseconds

    Returns:
        Default HOLD signal dictionary
    """
    return {
        'symbol': symbol,
        'action': 'HOLD',
        'confidence': 0,
        'reasoning': f"Default HOLD signal: {reason}",
        'entry_price': None,
        'stop_loss': None,
        'take_profit': None,
        'position_size_pct': None,
        'adjust_stop_loss': None,
        'ai_raw_response': response,
        'prompt_version': 'v1',
        'latency_ms': latency_ms,
        'error': True
    }
