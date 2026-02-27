"""
Telegram notifications for trading bot.
"""
import requests
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles Telegram bot notifications."""

    def __init__(self, config: Dict):
        """
        Initialize Telegram notifier.

        Args:
            config: Telegram configuration dictionary
        """
        self.config = config
        self.enabled = config.get('enabled', False)
        self.bot_token = config.get('bot_token', '')
        self.chat_id = config.get('chat_id', '')

        if self.enabled:
            if not self.bot_token or not self.chat_id:
                logger.warning("Telegram enabled but token/chat_id not configured")
                self.enabled = False
            else:
                logger.info("Telegram notifications enabled")
        else:
            logger.info("Telegram notifications disabled")

    def send_message(self, text: str, parse_mode: str = 'HTML') -> bool:
        """
        Send a message via Telegram bot.

        Args:
            text: Message text
            parse_mode: Parse mode (HTML or Markdown)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            logger.debug("Telegram disabled, skipping message")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': text,
                'parse_mode': parse_mode
            }

            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            logger.debug("Telegram message sent successfully")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False

    def format_trade_alert(self, signal: Dict, trade: Optional[Dict] = None) -> str:
        """
        Format a trade alert message.

        Args:
            signal: AI signal dictionary
            trade: Trade execution result (optional)

        Returns:
            Formatted message string
        """
        action = signal.get('action', 'UNKNOWN')
        symbol = signal.get('symbol', 'UNKNOWN')
        confidence = signal.get('confidence', 0)
        reasoning = signal.get('reasoning', 'No reasoning provided')

        # Choose emoji based on action
        if action == 'BUY':
            emoji = '🟢'
        elif action == 'SELL':
            emoji = '🔴'
        elif action == 'CLOSE':
            emoji = '⚪'
        else:
            emoji = '🟡'

        # Build message
        message = f"{emoji} <b>{action} SIGNAL</b>\n\n"
        message += f"<b>Symbol:</b> {symbol}\n"
        message += f"<b>Confidence:</b> {confidence}%\n"

        if signal.get('entry_price'):
            message += f"<b>Entry:</b> {signal['entry_price']}\n"

        if signal.get('stop_loss'):
            message += f"<b>Stop Loss:</b> {signal['stop_loss']}\n"

        if signal.get('take_profit'):
            message += f"<b>Take Profit:</b> {signal['take_profit']}\n"

        if signal.get('position_size_pct'):
            message += f"<b>Position Size:</b> {signal['position_size_pct']}%\n"

        message += f"\n<b>Reasoning:</b>\n{reasoning}\n"

        # Add trade execution details if available
        if trade:
            message += f"\n<b>--- Execution ---</b>\n"
            if trade.get('success'):
                message += f"✅ Order executed successfully\n"
                message += f"<b>Order ID:</b> {trade.get('order_id')}\n"
                message += f"<b>Quantity:</b> {trade.get('quantity', 0):.6f}\n"
                if trade.get('price'):
                    message += f"<b>Fill Price:</b> {trade['price']}\n"
            else:
                message += f"❌ Execution failed\n"
                message += f"<b>Error:</b> {trade.get('error', 'Unknown')}\n"

        return message

    def format_daily_report(self, stats: Dict) -> str:
        """
        Format a daily trading report.

        Args:
            stats: Dictionary with daily statistics

        Returns:
            Formatted report string
        """
        total_trades = stats.get('total_trades', 0)
        wins = stats.get('wins', 0)
        losses = stats.get('losses', 0)
        win_rate = stats.get('win_rate', 0)
        total_pnl = stats.get('total_pnl', 0)
        open_positions = stats.get('open_positions', 0)
        balance = stats.get('balance', 0)

        # Determine PnL emoji
        pnl_emoji = '📈' if total_pnl >= 0 else '📉'

        message = "📊 <b>DAILY TRADING REPORT</b>\n\n"
        message += f"<b>Total Trades:</b> {total_trades}\n"

        if total_trades > 0:
            message += f"<b>Wins:</b> {wins} | <b>Losses:</b> {losses}\n"
            message += f"<b>Win Rate:</b> {win_rate:.1f}%\n"

        message += f"\n{pnl_emoji} <b>Total PnL:</b> {total_pnl:+.2f} USDT\n"

        if stats.get('best_trade'):
            message += f"<b>Best Trade:</b> +{stats['best_trade']:.2f} USDT\n"

        if stats.get('worst_trade'):
            message += f"<b>Worst Trade:</b> {stats['worst_trade']:.2f} USDT\n"

        message += f"\n<b>Open Positions:</b> {open_positions}\n"
        message += f"<b>Balance:</b> {balance:.2f} USDT\n"

        # Add performance indicator
        if total_pnl > 0:
            message += f"\n✨ Profitable day!"
        elif total_pnl < 0:
            message += f"\n⚠️ Negative day - review strategy"
        else:
            message += f"\n➖ Break-even day"

        return message

    def format_error_alert(self, error: str, details: Optional[str] = None) -> str:
        """
        Format an error alert message.

        Args:
            error: Error message
            details: Additional error details (optional)

        Returns:
            Formatted error message
        """
        message = "🚨 <b>ERROR ALERT</b>\n\n"
        message += f"<b>Error:</b> {error}\n"

        if details:
            message += f"\n<b>Details:</b>\n{details}\n"

        return message

    def send_trade_alert(self, signal: Dict, trade: Optional[Dict] = None):
        """
        Send a trade alert notification.

        Args:
            signal: AI signal dictionary
            trade: Trade execution result (optional)
        """
        message = self.format_trade_alert(signal, trade)
        self.send_message(message)

    def send_daily_report(self, stats: Dict):
        """
        Send daily trading report.

        Args:
            stats: Daily statistics dictionary
        """
        message = self.format_daily_report(stats)
        self.send_message(message)

    def send_error_alert(self, error: str, details: Optional[str] = None):
        """
        Send error alert notification.

        Args:
            error: Error message
            details: Additional details (optional)
        """
        message = self.format_error_alert(error, details)
        self.send_message(message)

    def send_startup_notification(self, config_summary: str):
        """
        Send bot startup notification.

        Args:
            config_summary: Summary of bot configuration
        """
        message = "🤖 <b>BOT STARTED</b>\n\n"
        message += config_summary
        self.send_message(message)

    def send_shutdown_notification(self):
        """Send bot shutdown notification."""
        message = "🛑 <b>BOT STOPPED</b>\n\n"
        message += "Trading bot has been shut down."
        self.send_message(message)
