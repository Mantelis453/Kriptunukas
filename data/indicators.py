"""
Technical indicator calculations using the ta library.
"""
import pandas as pd
import numpy as np
from typing import Optional
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import VolumeWeightedAveragePrice
import logging

logger = logging.getLogger(__name__)


def calculate_all_indicators(df: pd.DataFrame) -> dict:
    """
    Calculate all technical indicators for trading analysis.

    Args:
        df: DataFrame with columns: timestamp, open, high, low, close, volume

    Returns:
        Dictionary containing all calculated indicators
    """
    try:
        # Make a copy to avoid modifying original
        data = df.copy()

        # Ensure we have enough data
        if len(data) < 200:
            logger.warning(f"Limited data available: {len(data)} candles (recommended: 200+)")

        # Calculate RSI
        rsi_indicator = RSIIndicator(close=data['close'], window=14)
        rsi = round(rsi_indicator.rsi().iloc[-1], 2)

        # Calculate MACD
        macd_indicator = MACD(
            close=data['close'],
            window_slow=26,
            window_fast=12,
            window_sign=9
        )
        macd_line = round(macd_indicator.macd().iloc[-1], 2)
        macd_signal = round(macd_indicator.macd_signal().iloc[-1], 2)
        macd_histogram = round(macd_indicator.macd_diff().iloc[-1], 2)

        # Calculate Bollinger Bands
        bb_indicator = BollingerBands(close=data['close'], window=20, window_dev=2)
        bb_upper = round(bb_indicator.bollinger_hband().iloc[-1], 2)
        bb_middle = round(bb_indicator.bollinger_mavg().iloc[-1], 2)
        bb_lower = round(bb_indicator.bollinger_lband().iloc[-1], 2)

        # Calculate BB position (0-100 scale)
        current_price = data['close'].iloc[-1]
        if bb_upper != bb_lower:
            bb_position = round(((current_price - bb_lower) / (bb_upper - bb_lower)) * 100, 2)
        else:
            bb_position = 50.0

        # Calculate EMAs
        ema_20_indicator = EMAIndicator(close=data['close'], window=20)
        ema_50_indicator = EMAIndicator(close=data['close'], window=50)
        ema_200_indicator = EMAIndicator(close=data['close'], window=200)

        ema_20 = round(ema_20_indicator.ema_indicator().iloc[-1], 2)
        ema_50 = round(ema_50_indicator.ema_indicator().iloc[-1], 2)
        ema_200 = round(ema_200_indicator.ema_indicator().iloc[-1], 2) if len(data) >= 200 else None

        # Calculate ATR
        atr_indicator = AverageTrueRange(
            high=data['high'],
            low=data['low'],
            close=data['close'],
            window=14
        )
        atr = round(atr_indicator.average_true_range().iloc[-1], 2)

        # Calculate Volume metrics
        volume_sma = data['volume'].rolling(window=20).mean().iloc[-1]
        current_volume = data['volume'].iloc[-1]
        volume_ratio = round(current_volume / volume_sma, 2) if volume_sma > 0 else 1.0

        # Determine overall trend
        trend = determine_trend(ema_20, ema_50, ema_200)

        # Calculate support and resistance levels
        support_resistance = calculate_support_resistance(data.tail(50))

        # Get last 10 candles summary
        last_candles = get_last_candles_summary(data.tail(10))

        # Compile all indicators
        indicators = {
            'current_price': round(current_price, 2),
            'rsi': rsi,
            'macd': {
                'line': macd_line,
                'signal': macd_signal,
                'histogram': macd_histogram
            },
            'bollinger_bands': {
                'upper': bb_upper,
                'middle': bb_middle,
                'lower': bb_lower,
                'position': bb_position
            },
            'ema': {
                'ema_20': ema_20,
                'ema_50': ema_50,
                'ema_200': ema_200
            },
            'atr': atr,
            'volume': {
                'current': round(current_volume, 2),
                'average': round(volume_sma, 2),
                'ratio': volume_ratio
            },
            'trend': trend,
            'support_resistance': support_resistance,
            'last_10_candles': last_candles
        }

        logger.info(f"Calculated indicators: Price={current_price}, RSI={rsi}, Trend={trend}")
        return indicators

    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
        raise


def determine_trend(ema_20: float, ema_50: float, ema_200: Optional[float]) -> str:
    """
    Determine overall market trend based on EMA alignment.

    Args:
        ema_20: 20-period EMA
        ema_50: 50-period EMA
        ema_200: 200-period EMA (optional)

    Returns:
        Trend classification: BULLISH, BEARISH, or NEUTRAL
    """
    if ema_200 is None:
        # If we don't have 200 EMA, use just 20 and 50
        if ema_20 > ema_50:
            return "BULLISH"
        elif ema_20 < ema_50:
            return "BEARISH"
        else:
            return "NEUTRAL"

    # Full EMA alignment
    if ema_20 > ema_50 > ema_200:
        return "BULLISH"
    elif ema_20 < ema_50 < ema_200:
        return "BEARISH"
    else:
        return "NEUTRAL"


def calculate_support_resistance(df: pd.DataFrame) -> dict:
    """
    Calculate support and resistance levels based on recent pivot points.

    Args:
        df: DataFrame with recent candle data (last 50 candles recommended)

    Returns:
        Dictionary with support and resistance levels
    """
    try:
        # Find local highs and lows
        highs = df['high'].values
        lows = df['low'].values

        # Calculate pivot points
        pivot_highs = []
        pivot_lows = []

        for i in range(2, len(df) - 2):
            # Pivot high: higher than 2 candles on each side
            if highs[i] > max(highs[i-2:i]) and highs[i] > max(highs[i+1:i+3]):
                pivot_highs.append(highs[i])

            # Pivot low: lower than 2 candles on each side
            if lows[i] < min(lows[i-2:i]) and lows[i] < min(lows[i+1:i+3]):
                pivot_lows.append(lows[i])

        # Get strongest levels (most recent and significant)
        resistance_levels = sorted(pivot_highs, reverse=True)[:3] if pivot_highs else []
        support_levels = sorted(pivot_lows, reverse=True)[:3] if pivot_lows else []

        return {
            'resistance': [round(r, 2) for r in resistance_levels],
            'support': [round(s, 2) for s in support_levels]
        }

    except Exception as e:
        logger.warning(f"Error calculating support/resistance: {e}")
        return {'resistance': [], 'support': []}


def get_last_candles_summary(df: pd.DataFrame) -> list:
    """
    Get summary of last N candles.

    Args:
        df: DataFrame with last N candles

    Returns:
        List of dictionaries with candle information
    """
    try:
        candles = []
        for _, row in df.iterrows():
            # Determine candle type
            candle_type = "GREEN" if row['close'] >= row['open'] else "RED"
            body_size = abs(row['close'] - row['open'])
            range_size = row['high'] - row['low']
            body_percent = round((body_size / range_size * 100), 1) if range_size > 0 else 0

            candles.append({
                'open': round(row['open'], 2),
                'high': round(row['high'], 2),
                'low': round(row['low'], 2),
                'close': round(row['close'], 2),
                'volume': round(row['volume'], 2),
                'type': candle_type,
                'body_percent': body_percent
            })

        return candles

    except Exception as e:
        logger.warning(f"Error getting candles summary: {e}")
        return []
