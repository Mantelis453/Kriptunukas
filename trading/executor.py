"""
Trade execution on crypto exchanges using ccxt.
Supports: Binance, Bybit, and more
"""
import ccxt
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class TradeExecutor:
    """Handles order execution on crypto exchanges."""

    def __init__(self, config: Dict):
        """
        Initialize trade executor with exchange connection.

        Args:
            config: Exchange configuration dictionary
        """
        self.config = config
        self.exchange = None
        self.exchange_name = config.get('name', 'binance').lower()
        self._connect()

    def _connect(self):
        """Establish connection to exchange."""
        try:
            exchange_config = {
                'apiKey': self.config.get('api_key'),
                'secret': self.config.get('api_secret'),
                'enableRateLimit': True,
                'options': {}
            }

            # Exchange-specific configurations
            if self.exchange_name == 'binance':
                exchange_config['options']['defaultType'] = 'future'
                # Binance testnet URL
                if self.config.get('testnet', True):
                    exchange_config['urls'] = {
                        'api': {
                            'public': 'https://testnet.binancefuture.com/fapi/v1',
                            'private': 'https://testnet.binancefuture.com/fapi/v1',
                        }
                    }

            elif self.exchange_name == 'bybit':
                exchange_config['options']['defaultType'] = 'future'
                if self.config.get('testnet', True):
                    exchange_config['options']['testnet'] = True

            # Create exchange instance
            if self.exchange_name == 'binance':
                self.exchange = ccxt.binance(exchange_config)
            elif self.exchange_name == 'bybit':
                self.exchange = ccxt.bybit(exchange_config)
            else:
                raise ValueError(f"Unsupported exchange: {self.exchange_name}")

            self.exchange.load_markets()
            logger.info(f"Trade executor connected to {self.exchange_name.upper()}")

        except Exception as e:
            logger.error(f"Failed to connect trade executor: {e}")
            raise

    def place_market_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Dict:
        """
        Place a market order with optional stop-loss and take-profit.

        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            side: Order side ('buy' or 'sell')
            quantity: Order quantity in base currency
            stop_loss: Stop-loss price (optional)
            take_profit: Take-profit price (optional)

        Returns:
            Order response dictionary

        Raises:
            Exception: If order placement fails
        """
        try:
            logger.info(
                f"Placing {side.upper()} market order: {symbol} "
                f"qty={quantity:.6f} SL={stop_loss} TP={take_profit}"
            )

            # Place market order
            order = self.exchange.create_market_order(
                symbol=symbol,
                side=side.lower(),
                amount=quantity
            )

            logger.info(
                f"Order placed successfully: ID={order.get('id')} "
                f"Status={order.get('status')}"
            )

            # Set stop-loss and take-profit if provided
            if stop_loss or take_profit:
                self._set_sl_tp(symbol, side, quantity, stop_loss, take_profit)

            return {
                'success': True,
                'order_id': order.get('id'),
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'price': order.get('average') or order.get('price', 0),
                'status': order.get('status'),
                'timestamp': order.get('timestamp'),
                'raw_order': order
            }

        except ccxt.InsufficientFunds as e:
            logger.error(f"Insufficient funds for order: {e}")
            return {
                'success': False,
                'error': 'Insufficient funds',
                'details': str(e)
            }

        except ccxt.InvalidOrder as e:
            logger.error(f"Invalid order: {e}")
            return {
                'success': False,
                'error': 'Invalid order',
                'details': str(e)
            }

        except ccxt.NetworkError as e:
            logger.error(f"Network error placing order: {e}")
            return {
                'success': False,
                'error': 'Network error',
                'details': str(e)
            }

        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return {
                'success': False,
                'error': 'Unknown error',
                'details': str(e)
            }

    def _set_sl_tp(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_loss: Optional[float],
        take_profit: Optional[float]
    ):
        """
        Set stop-loss and take-profit for a position.

        Args:
            symbol: Trading pair
            side: Original order side
            quantity: Position quantity
            stop_loss: Stop-loss price
            take_profit: Take-profit price
        """
        try:
            # Determine the opposite side for SL/TP orders
            sl_tp_side = 'sell' if side.lower() == 'buy' else 'buy'

            # Set stop-loss
            if stop_loss:
                try:
                    sl_order = self.exchange.create_order(
                        symbol=symbol,
                        type='stop_market',
                        side=sl_tp_side,
                        amount=quantity,
                        params={
                            'stopPrice': stop_loss,
                            'reduceOnly': True
                        }
                    )
                    logger.info(f"Stop-loss set at {stop_loss}: {sl_order.get('id')}")
                except Exception as e:
                    logger.error(f"Failed to set stop-loss: {e}")

            # Set take-profit
            if take_profit:
                try:
                    tp_order = self.exchange.create_order(
                        symbol=symbol,
                        type='limit',
                        side=sl_tp_side,
                        amount=quantity,
                        price=take_profit,
                        params={'reduceOnly': True}
                    )
                    logger.info(f"Take-profit set at {take_profit}: {tp_order.get('id')}")
                except Exception as e:
                    logger.error(f"Failed to set take-profit: {e}")

        except Exception as e:
            logger.error(f"Error setting SL/TP: {e}")

    def close_position(self, symbol: str, position: Dict) -> Dict:
        """
        Close an open position at market price.

        Args:
            symbol: Trading pair
            position: Position dictionary with side and size

        Returns:
            Order response dictionary

        Raises:
            Exception: If position closing fails
        """
        try:
            side = position.get('side', '').lower()
            size = position.get('size', 0)

            # Determine closing side (opposite of position side)
            if side == 'long' or side == 'buy':
                close_side = 'sell'
            else:
                close_side = 'buy'

            logger.info(f"Closing {side.upper()} position: {symbol} qty={size}")

            # Place market order to close
            order = self.exchange.create_market_order(
                symbol=symbol,
                side=close_side,
                amount=abs(size),
                params={'reduceOnly': True}
            )

            logger.info(f"Position closed: ID={order.get('id')}")

            return {
                'success': True,
                'order_id': order.get('id'),
                'symbol': symbol,
                'side': close_side,
                'quantity': abs(size),
                'price': order.get('average') or order.get('price', 0),
                'status': order.get('status'),
                'raw_order': order
            }

        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return {
                'success': False,
                'error': 'Failed to close position',
                'details': str(e)
            }

    def get_order_status(self, order_id: str, symbol: str) -> Dict:
        """
        Get status of an order.

        Args:
            order_id: Exchange order ID
            symbol: Trading pair

        Returns:
            Order status dictionary

        Raises:
            Exception: If status fetch fails
        """
        try:
            order = self.exchange.fetch_order(order_id, symbol)

            return {
                'order_id': order.get('id'),
                'status': order.get('status'),
                'filled': order.get('filled', 0),
                'remaining': order.get('remaining', 0),
                'price': order.get('average') or order.get('price', 0),
                'raw_order': order
            }

        except Exception as e:
            logger.error(f"Error fetching order status: {e}")
            return {
                'error': 'Failed to fetch order status',
                'details': str(e)
            }

    def adjust_stop_loss(
        self,
        symbol: str,
        position: Dict,
        new_stop_loss: float
    ) -> bool:
        """
        Adjust stop-loss for an open position.

        Args:
            symbol: Trading pair
            position: Position dictionary
            new_stop_loss: New stop-loss price

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Adjusting stop-loss for {symbol} to {new_stop_loss}")

            # Cancel existing stop-loss orders
            open_orders = self.exchange.fetch_open_orders(symbol)
            for order in open_orders:
                if order.get('type') == 'stop_market':
                    try:
                        self.exchange.cancel_order(order['id'], symbol)
                        logger.info(f"Cancelled old stop-loss: {order['id']}")
                    except Exception as e:
                        logger.warning(f"Failed to cancel order {order['id']}: {e}")

            # Set new stop-loss
            side = position.get('side', '').lower()
            size = position.get('size', 0)
            sl_side = 'sell' if side == 'long' or side == 'buy' else 'buy'

            sl_order = self.exchange.create_order(
                symbol=symbol,
                type='stop_market',
                side=sl_side,
                amount=abs(size),
                params={
                    'stopPrice': new_stop_loss,
                    'reduceOnly': True
                }
            )

            logger.info(f"New stop-loss set: {sl_order.get('id')}")
            return True

        except Exception as e:
            logger.error(f"Error adjusting stop-loss: {e}")
            return False

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """
        Cancel an open order.

        Args:
            order_id: Exchange order ID
            symbol: Trading pair

        Returns:
            True if successful, False otherwise
        """
        try:
            self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Order cancelled: {order_id}")
            return True

        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False
