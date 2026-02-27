"""
Risk management and position sizing for trading bot.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


class RiskManager:
    """Handles risk management and trade validation."""

    def __init__(self, config: Dict):
        """
        Initialize risk manager with configuration.

        Args:
            config: Risk management configuration dictionary
        """
        self.config = config
        self.max_risk_per_trade = config.get('max_risk_per_trade', 0.02)
        self.max_daily_drawdown = config.get('max_daily_drawdown', 0.05)
        self.max_open_positions = config.get('max_open_positions', 3)
        self.cooldown_hours = config.get('cooldown_hours', 2)
        self.min_reward_risk_ratio = config.get('min_reward_risk_ratio', 2.0)

        logger.info(
            f"Risk Manager initialized: Max risk/trade={self.max_risk_per_trade}, "
            f"Max daily drawdown={self.max_daily_drawdown}, "
            f"Max positions={self.max_open_positions}"
        )

    def validate_signal(
        self,
        signal: Dict,
        portfolio_balance: float,
        open_trades: List[Dict],
        trades_today: List[Dict],
        last_trade: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Validate trading signal against risk management rules.

        Args:
            signal: AI trading signal dictionary
            portfolio_balance: Current portfolio balance
            open_trades: List of currently open trades
            trades_today: List of trades from today
            last_trade: Most recent trade for this symbol (optional)

        Returns:
            Tuple of (is_valid: bool, reason: str)
        """
        symbol = signal.get('symbol')
        action = signal.get('action')
        confidence = signal.get('confidence', 0)

        # Rule 1: Check confidence threshold
        min_confidence = self.config.get('min_confidence', 70)
        if confidence < min_confidence:
            return False, f"Confidence {confidence}% below threshold {min_confidence}%"

        # Rule 2: Check if action requires validation
        if action in ['HOLD']:
            return True, "HOLD action requires no validation"

        # Rule 3: Check max open positions
        if action in ['BUY', 'SELL'] and len(open_trades) >= self.max_open_positions:
            return False, f"Max open positions ({self.max_open_positions}) reached"

        # Rule 4: Check daily drawdown limit
        daily_pnl = self.calculate_daily_pnl(trades_today, open_trades)
        max_loss = portfolio_balance * self.max_daily_drawdown

        if daily_pnl < -max_loss:
            return (
                False,
                f"Daily drawdown limit reached: {daily_pnl:.2f} USDT "
                f"(limit: -{max_loss:.2f} USDT)"
            )

        # Rule 5: Check cooldown period
        if last_trade and action in ['BUY', 'SELL']:
            if self.is_in_cooldown(last_trade):
                return (
                    False,
                    f"Symbol {symbol} in cooldown period "
                    f"({self.cooldown_hours}h since last trade)"
                )

        # Rule 6: Check reward-to-risk ratio (for new positions)
        if action in ['BUY', 'SELL']:
            entry = signal.get('entry_price')
            stop_loss = signal.get('stop_loss')
            take_profit = signal.get('take_profit')

            if entry and stop_loss and take_profit:
                risk = abs(entry - stop_loss)
                reward = abs(take_profit - entry)

                if risk > 0:
                    rr_ratio = reward / risk
                    if rr_ratio < self.min_reward_risk_ratio:
                        return (
                            False,
                            f"Reward:Risk ratio {rr_ratio:.2f} below minimum "
                            f"{self.min_reward_risk_ratio}"
                        )
                else:
                    return False, "Invalid stop-loss (same as entry price)"
            elif action in ['BUY', 'SELL']:
                # If we're opening a position, we need these values
                return False, "Missing entry_price, stop_loss, or take_profit"

        # Rule 7: Validate position size
        if action in ['BUY', 'SELL']:
            position_size_pct = signal.get('position_size_pct')
            if not position_size_pct or position_size_pct < 1 or position_size_pct > 5:
                return False, f"Invalid position size: {position_size_pct}%"

        # All checks passed
        return True, "Signal validated successfully"

    def calculate_position_size(
        self,
        signal: Dict,
        portfolio_balance: float,
        current_price: float
    ) -> float:
        """
        Calculate position size based on risk parameters.

        Args:
            signal: Trading signal with entry and stop-loss
            portfolio_balance: Available portfolio balance
            current_price: Current market price

        Returns:
            Position size in base currency (e.g., BTC amount)
        """
        entry_price = signal.get('entry_price', current_price)
        stop_loss = signal.get('stop_loss')

        if not stop_loss or stop_loss == entry_price:
            logger.error("Invalid stop-loss for position sizing")
            return 0.0

        # Calculate risk per trade in USDT
        risk_amount = portfolio_balance * self.max_risk_per_trade

        # Calculate risk per unit
        risk_per_unit = abs(entry_price - stop_loss)

        # Calculate position size
        position_size = risk_amount / risk_per_unit

        # Apply position size percentage limit from AI
        position_size_pct = signal.get('position_size_pct', 2) / 100
        max_position_value = portfolio_balance * position_size_pct
        max_position_size = max_position_value / entry_price

        # Use the smaller of the two
        final_size = min(position_size, max_position_size)

        logger.info(
            f"Position size calculated: {final_size:.6f} "
            f"(risk: {risk_amount:.2f} USDT, "
            f"risk/unit: {risk_per_unit:.2f})"
        )

        return final_size

    def calculate_daily_pnl(
        self,
        trades_today: List[Dict],
        open_trades: List[Dict]
    ) -> float:
        """
        Calculate total PnL for today (realized + unrealized).

        Args:
            trades_today: List of closed trades from today
            open_trades: List of currently open trades

        Returns:
            Total PnL in USDT
        """
        # Sum realized PnL from closed trades today
        realized_pnl = sum(
            trade.get('pnl', 0) or 0
            for trade in trades_today
            if trade.get('status') == 'CLOSED'
        )

        # Sum unrealized PnL from open trades
        unrealized_pnl = sum(
            trade.get('unrealized_pnl', 0) or 0
            for trade in open_trades
        )

        total_pnl = realized_pnl + unrealized_pnl

        logger.debug(
            f"Daily PnL: Realized={realized_pnl:.2f}, "
            f"Unrealized={unrealized_pnl:.2f}, "
            f"Total={total_pnl:.2f}"
        )

        return total_pnl

    def is_in_cooldown(self, last_trade: Dict) -> bool:
        """
        Check if symbol is in cooldown period.

        Args:
            last_trade: Most recent trade dictionary

        Returns:
            True if in cooldown, False otherwise
        """
        if not last_trade:
            return False

        # Get last trade timestamp
        opened_at = last_trade.get('opened_at')
        if not opened_at:
            return False

        # Parse timestamp (SQLite returns string)
        try:
            if isinstance(opened_at, str):
                last_trade_time = datetime.fromisoformat(opened_at.replace('Z', '+00:00'))
            else:
                last_trade_time = opened_at

            # Check if enough time has passed
            cooldown_delta = timedelta(hours=self.cooldown_hours)
            time_since_trade = datetime.now() - last_trade_time

            in_cooldown = time_since_trade < cooldown_delta

            if in_cooldown:
                remaining = cooldown_delta - time_since_trade
                logger.info(
                    f"In cooldown: {remaining.total_seconds() / 3600:.1f}h remaining"
                )

            return in_cooldown

        except Exception as e:
            logger.error(f"Error checking cooldown: {e}")
            return False

    def get_max_position_value(self, portfolio_balance: float) -> float:
        """
        Get maximum position value based on risk settings.

        Args:
            portfolio_balance: Current portfolio balance

        Returns:
            Maximum position value in USDT
        """
        # Maximum position is based on max risk per trade
        # Assuming 1% stop-loss, max position would be risk / 0.01
        return portfolio_balance * self.max_risk_per_trade / 0.01

    def check_emergency_stop(
        self,
        portfolio_balance: float,
        initial_balance: float
    ) -> Tuple[bool, str]:
        """
        Check if emergency stop should be triggered.

        Args:
            portfolio_balance: Current portfolio balance
            initial_balance: Starting portfolio balance

        Returns:
            Tuple of (should_stop: bool, reason: str)
        """
        # Calculate total drawdown
        total_drawdown = (initial_balance - portfolio_balance) / initial_balance

        # Emergency stop at 10% total drawdown
        emergency_threshold = 0.10

        if total_drawdown >= emergency_threshold:
            return (
                True,
                f"Emergency stop triggered: {total_drawdown * 100:.1f}% total drawdown"
            )

        return False, ""
