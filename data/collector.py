"""
Data collection from crypto exchanges using ccxt.
Supports: Binance, Bybit, and more
"""
import ccxt
import pandas as pd
import time
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DataCollector:
    """Handles data collection from crypto exchanges using ccxt."""

    def __init__(self, config: Dict, demo_mode: bool = False):
        """
        Initialize exchange connection.

        Args:
            config: Exchange configuration dictionary
            demo_mode: If True, use public API only (no authentication needed)
        """
        self.config = config
        self.exchange = None
        self.demo_mode = demo_mode
        self.exchange_name = config.get('name', 'binance').lower()
        self._connect()

    def _connect(self):
        """Establish connection to exchange."""
        try:
            exchange_config = {
                'enableRateLimit': True,
                'options': {}
            }

            # Exchange-specific configurations
            if self.exchange_name == 'binance':
                exchange_config['options']['defaultType'] = 'future'  # USDT-M Futures
                # Binance testnet URL (updated to new demo endpoint)
                if self.config.get('testnet', True):
                    exchange_config['urls'] = {
                        'api': {
                            'public': 'https://demo-fapi.binance.com/fapi/v1',
                            'private': 'https://demo-fapi.binance.com/fapi/v1',
                        }
                    }

            elif self.exchange_name == 'bybit':
                exchange_config['options']['defaultType'] = 'linear'
                if self.config.get('testnet', True):
                    exchange_config['options']['testnet'] = True

            # Only add credentials if not in demo mode
            if not self.demo_mode:
                exchange_config['apiKey'] = self.config.get('api_key')
                exchange_config['secret'] = self.config.get('api_secret')

            # Create exchange instance
            if self.exchange_name == 'binance':
                self.exchange = ccxt.binance(exchange_config)
            elif self.exchange_name == 'bybit':
                self.exchange = ccxt.bybit(exchange_config)
            else:
                raise ValueError(f"Unsupported exchange: {self.exchange_name}")

            self.exchange.load_markets()

            mode = "DEMO MODE (public API only)" if self.demo_mode else "authenticated"
            env = 'testnet' if self.config.get('testnet') else 'mainnet'
            logger.info(f"Connected to {self.exchange_name.upper()} {env} - {mode}")

        except Exception as e:
            logger.error(f"Failed to connect to {self.exchange_name}: {e}")
            if not self.demo_mode:
                logger.warning("Try running with --demo flag to test without authentication")
            raise

    def fetch_candles(self, symbol: str, timeframe: str = '1h', limit: int = 200) -> pd.DataFrame:
        """
        Fetch OHLCV candles from Bybit.

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Candle timeframe (e.g., '1h', '4h')
            limit: Number of candles to fetch

        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume

        Raises:
            Exception: If fetch fails after retries
        """
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                # Fetch OHLCV data
                ohlcv = self.exchange.fetch_ohlcv(
                    symbol=symbol,
                    timeframe=timeframe,
                    limit=limit
                )

                # Convert to DataFrame
                df = pd.DataFrame(
                    ohlcv,
                    columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
                )

                # Convert timestamp to milliseconds (if not already)
                df['timestamp'] = df['timestamp'].astype(int)

                logger.info(f"Fetched {len(df)} candles for {symbol} {timeframe}")
                return df

            except ccxt.NetworkError as e:
                logger.warning(f"Network error fetching candles (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch candles after {max_retries} attempts")
                    raise

            except ccxt.ExchangeError as e:
                logger.error(f"Exchange error fetching candles: {e}")
                raise

            except Exception as e:
                logger.error(f"Unexpected error fetching candles: {e}")
                raise

        # This should not be reached, but just in case
        return pd.DataFrame()

    def fetch_ticker(self, symbol: str) -> Dict:
        """
        Fetch current ticker data for a symbol.

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')

        Returns:
            Dictionary with current price, 24h change, volume

        Raises:
            Exception: If fetch fails after retries
        """
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                ticker = self.exchange.fetch_ticker(symbol)

                return {
                    'symbol': symbol,
                    'price': ticker.get('last', 0),
                    'change_24h': ticker.get('percentage', 0),
                    'volume_24h': ticker.get('quoteVolume', 0),
                    'high_24h': ticker.get('high', 0),
                    'low_24h': ticker.get('low', 0),
                    'timestamp': ticker.get('timestamp', int(time.time() * 1000))
                }

            except ccxt.NetworkError as e:
                logger.warning(f"Network error fetching ticker (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    logger.error(f"Failed to fetch ticker after {max_retries} attempts")
                    raise

            except Exception as e:
                logger.error(f"Error fetching ticker: {e}")
                raise

        return {}

    def fetch_balance(self) -> float:
        """
        Fetch available USDT balance.

        Returns:
            Available USDT balance

        Raises:
            Exception: If fetch fails after retries
        """
        # Return mock balance in demo mode
        if self.demo_mode:
            mock_balance = 10000.0
            logger.info(f"[DEMO] Available USDT balance: {mock_balance}")
            return mock_balance

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                balance = self.exchange.fetch_balance()
                usdt_balance = balance.get('USDT', {}).get('free', 0)

                logger.info(f"Available USDT balance: {usdt_balance}")
                return float(usdt_balance)

            except ccxt.NetworkError as e:
                logger.warning(f"Network error fetching balance (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    logger.error(f"Failed to fetch balance after {max_retries} attempts")
                    raise

            except Exception as e:
                logger.error(f"Error fetching balance: {e}")
                raise

        return 0.0

    def fetch_open_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Fetch open positions from exchange.

        Args:
            symbol: Trading pair (optional, None for all positions)

        Returns:
            List of position dictionaries with entry price, size, unrealized PnL

        Raises:
            Exception: If fetch fails after retries
        """
        # Return empty positions in demo mode
        if self.demo_mode:
            logger.info(f"[DEMO] No open positions")
            return []

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                positions = self.exchange.fetch_positions(symbols=[symbol] if symbol else None)

                # Filter out closed positions and format data
                open_positions = []
                for pos in positions:
                    # Skip if position size is zero or None
                    contracts = pos.get('contracts', 0)
                    if not contracts or contracts == 0:
                        continue

                    open_positions.append({
                        'symbol': pos.get('symbol'),
                        'side': pos.get('side'),
                        'size': contracts,
                        'entry_price': pos.get('entryPrice', 0),
                        'current_price': pos.get('markPrice', 0),
                        'unrealized_pnl': pos.get('unrealizedPnl', 0),
                        'percentage': pos.get('percentage', 0),
                        'leverage': pos.get('leverage', 1),
                        'liquidation_price': pos.get('liquidationPrice', 0)
                    })

                logger.info(f"Found {len(open_positions)} open positions")
                return open_positions

            except ccxt.NetworkError as e:
                logger.warning(f"Network error fetching positions (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    logger.error(f"Failed to fetch positions after {max_retries} attempts")
                    raise

            except Exception as e:
                logger.error(f"Error fetching positions: {e}")
                raise

        return []

    def test_connection(self) -> bool:
        """
        Test exchange connection and credentials.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            # In demo mode, just test public API
            if self.demo_mode:
                # Different symbol format for different exchanges
                if self.exchange_name == 'binance':
                    self.exchange.fetch_ticker('BTC/USDT')
                else:  # bybit
                    self.exchange.fetch_ticker('BTC/USDT:USDT')
                logger.info("[DEMO] Public API connection test successful")
                return True

            # Try to fetch balance to test credentials
            self.exchange.fetch_balance()
            logger.info("Exchange connection test successful")
            return True

        except Exception as e:
            logger.error(f"Exchange connection test failed: {e}")
            return False
