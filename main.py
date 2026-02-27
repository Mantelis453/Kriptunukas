"""
Crypto Trading Bot - Main Entry Point
AI-powered paper trading bot for Bybit testnet
"""
import yaml
import schedule
import time
import signal
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Import custom modules
from utils.logger import setup_logger
from db.database import Database
from data.collector import DataCollector
from data.indicators import calculate_all_indicators
from ai.analyzer import get_ai_signal
from trading.risk import RiskManager
from trading.executor import TradeExecutor
from notifications.telegram import TelegramNotifier

# Global variables
config = {}
db = None
collector = None
risk_manager = None
executor = None
telegram = None
logger = None
dry_run = False
demo_mode = False
initial_balance = 0


def load_config(config_path: str = 'config.yaml') -> dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config file

    Returns:
        Configuration dictionary
    """
    try:
        with open(config_path, 'r') as f:
            conf = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return conf
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        sys.exit(1)


def initialize_modules():
    """Initialize all bot modules."""
    global db, collector, risk_manager, executor, telegram, initial_balance

    logger.info("Initializing modules...")

    # Database
    db = Database(config['database']['path'])

    # Data collector
    collector = DataCollector(config['exchange'], demo_mode=demo_mode)

    # Risk manager
    risk_manager = RiskManager(config['risk'])

    # Trade executor
    if not dry_run:
        executor = TradeExecutor(config['exchange'])
    else:
        logger.info("DRY RUN mode: Trade execution disabled")

    # Telegram notifier
    telegram = TelegramNotifier(config.get('telegram', {}))

    # Get initial balance
    try:
        initial_balance = collector.fetch_balance()
        logger.info(f"Initial balance: {initial_balance} USDT")
    except Exception as e:
        logger.error(f"Failed to fetch initial balance: {e}")
        initial_balance = 10000  # Default for testing

    logger.info("All modules initialized successfully")


def run_analysis(symbol: str):
    """
    Run complete analysis and trading logic for a symbol.

    Args:
        symbol: Trading pair to analyze
    """
    try:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running analysis for {symbol}")
        logger.info(f"{'='*60}")

        # 1. Fetch latest candles
        logger.info("Fetching market data...")
        candles_1h = collector.fetch_candles(symbol, '1h', limit=200)
        db.save_candles(symbol, '1h', candles_1h)

        # Fetch 4h candles as well for additional context
        candles_4h = collector.fetch_candles(symbol, '4h', limit=200)
        db.save_candles(symbol, '4h', candles_4h)

        # 2. Calculate indicators (using 1h timeframe)
        logger.info("Calculating technical indicators...")
        indicators = calculate_all_indicators(candles_1h)

        # 3. Fetch current position and balance
        logger.info("Fetching portfolio status...")
        portfolio_balance = collector.fetch_balance()
        open_positions = collector.fetch_open_positions(symbol)
        current_position = open_positions[0] if open_positions else None

        # 4. Get AI signal
        logger.info("Requesting AI analysis...")
        signal = get_ai_signal(
            symbol=symbol,
            indicators=indicators,
            current_position=current_position,
            portfolio_balance=portfolio_balance,
            config=config['ai']
        )

        # 5. Save signal to database
        signal_id = db.save_signal(signal)
        logger.info(f"Signal saved: {signal['action']} (confidence: {signal['confidence']}%)")

        # 6. Save AI log
        db.save_ai_log({
            'symbol': symbol,
            'prompt': 'Generated in analyzer',
            'response': signal.get('ai_raw_response', ''),
            'model': 'claude_cli',
            'latency_ms': signal.get('latency_ms', 0)
        })

        # 7. Process signal
        action = signal.get('action')

        if action in ['BUY', 'SELL']:
            # Validate signal through risk manager
            open_trades = db.get_open_trades(symbol)
            trades_today = db.get_trades_today()
            last_trade = db.get_last_trade(symbol)

            is_valid, reason = risk_manager.validate_signal(
                signal=signal,
                portfolio_balance=portfolio_balance,
                open_trades=open_trades,
                trades_today=trades_today,
                last_trade=last_trade
            )

            if is_valid:
                logger.info(f"Signal validated: {reason}")

                # Calculate position size
                current_price = indicators.get('current_price')
                position_size = risk_manager.calculate_position_size(
                    signal=signal,
                    portfolio_balance=portfolio_balance,
                    current_price=current_price
                )

                logger.info(f"Position size calculated: {position_size:.6f}")

                # Execute trade
                if not dry_run and executor:
                    trade_result = executor.place_market_order(
                        symbol=symbol,
                        side=action.lower(),
                        quantity=position_size,
                        stop_loss=signal.get('stop_loss'),
                        take_profit=signal.get('take_profit')
                    )

                    # Save trade to database
                    if trade_result.get('success'):
                        trade_id = db.save_trade({
                            'signal_id': signal_id,
                            'symbol': symbol,
                            'side': action,
                            'quantity': position_size,
                            'entry_price': trade_result.get('price', current_price),
                            'stop_loss': signal.get('stop_loss'),
                            'take_profit': signal.get('take_profit'),
                            'status': 'OPEN',
                            'exchange_order_id': trade_result.get('order_id')
                        })
                        logger.info(f"Trade saved to database: ID={trade_id}")

                        # Send Telegram notification
                        telegram.send_trade_alert(signal, trade_result)
                    else:
                        logger.error(f"Trade execution failed: {trade_result.get('error')}")
                        telegram.send_error_alert(
                            "Trade execution failed",
                            trade_result.get('details')
                        )
                else:
                    logger.info(f"DRY RUN: Would execute {action} order for {position_size:.6f} {symbol}")
                    telegram.send_trade_alert(signal)

            else:
                logger.warning(f"Signal rejected: {reason}")

        elif action == 'CLOSE':
            # Close existing position
            if current_position:
                logger.info("AI recommends closing position")

                if not dry_run and executor:
                    close_result = executor.close_position(symbol, current_position)

                    if close_result.get('success'):
                        # Update trade in database
                        open_trades = db.get_open_trades(symbol)
                        if open_trades:
                            trade = open_trades[0]
                            entry_price = trade.get('entry_price', 0)
                            exit_price = close_result.get('price', 0)
                            pnl = (exit_price - entry_price) * trade.get('quantity', 0)
                            pnl_percent = (pnl / (entry_price * trade.get('quantity', 1))) * 100

                            db.update_trade(trade['id'], {
                                'exit_price': exit_price,
                                'pnl': pnl,
                                'pnl_percent': pnl_percent,
                                'status': 'CLOSED'
                            })

                            logger.info(f"Position closed. PnL: {pnl:+.2f} USDT ({pnl_percent:+.2f}%)")
                            telegram.send_trade_alert(signal, close_result)
                else:
                    logger.info("DRY RUN: Would close position")
            else:
                logger.info("No position to close")

        elif action == 'HOLD':
            logger.info(f"AI recommends HOLD: {signal.get('reasoning')}")

            # Check if we should adjust stop-loss
            if signal.get('adjust_stop_loss') and current_position:
                new_sl = signal['adjust_stop_loss']
                logger.info(f"AI recommends adjusting stop-loss to {new_sl}")

                if not dry_run and executor:
                    executor.adjust_stop_loss(symbol, current_position, new_sl)

        logger.info(f"Analysis complete for {symbol}\n")

    except Exception as e:
        logger.error(f"Error in analysis for {symbol}: {e}", exc_info=True)
        telegram.send_error_alert(f"Analysis error for {symbol}", str(e))


def run_monitor():
    """Monitor open positions and update their status."""
    try:
        logger.info("Running position monitor...")

        # Get all open trades from database
        open_trades = db.get_open_trades()

        for trade in open_trades:
            try:
                symbol = trade.get('symbol')

                # Fetch current positions from exchange
                exchange_positions = collector.fetch_open_positions(symbol)

                # Check if position still exists on exchange
                position_exists = False
                for pos in exchange_positions:
                    if abs(pos.get('size', 0)) > 0:
                        position_exists = True

                        # Update unrealized PnL in database
                        db.update_trade(trade['id'], {
                            'unrealized_pnl': pos.get('unrealized_pnl', 0)
                        })
                        break

                # If position no longer exists, it was closed (SL/TP hit)
                if not position_exists:
                    logger.info(f"Position closed on exchange: {symbol}")

                    # Fetch final price
                    ticker = collector.fetch_ticker(symbol)
                    exit_price = ticker.get('price', 0)

                    # Calculate PnL
                    entry_price = trade.get('entry_price', 0)
                    quantity = trade.get('quantity', 0)
                    side = trade.get('side', 'BUY')

                    if side == 'BUY':
                        pnl = (exit_price - entry_price) * quantity
                    else:
                        pnl = (entry_price - exit_price) * quantity

                    pnl_percent = (pnl / (entry_price * quantity)) * 100 if (entry_price * quantity) > 0 else 0

                    # Update trade
                    db.update_trade(trade['id'], {
                        'exit_price': exit_price,
                        'pnl': pnl,
                        'pnl_percent': pnl_percent,
                        'status': 'CLOSED'
                    })

                    logger.info(f"Trade updated: PnL={pnl:+.2f} USDT ({pnl_percent:+.2f}%)")

            except Exception as e:
                logger.error(f"Error monitoring trade {trade.get('id')}: {e}")

        # Take portfolio snapshot
        try:
            balance = collector.fetch_balance()
            all_positions = collector.fetch_open_positions()
            trades_today = db.get_trades_today()
            daily_pnl = risk_manager.calculate_daily_pnl(trades_today, all_positions)

            db.save_portfolio_snapshot({
                'total_balance': balance,
                'available_balance': balance,
                'unrealized_pnl': sum(p.get('unrealized_pnl', 0) for p in all_positions),
                'open_positions': len(all_positions),
                'daily_pnl': daily_pnl
            })

        except Exception as e:
            logger.error(f"Error saving portfolio snapshot: {e}")

        logger.info("Position monitor complete\n")

    except Exception as e:
        logger.error(f"Error in position monitor: {e}", exc_info=True)


def run_daily_report():
    """Generate and send daily trading report."""
    try:
        logger.info("Generating daily report...")

        # Get today's trades
        trades_today = db.get_trades_today()

        # Calculate statistics
        total_trades = len(trades_today)
        closed_trades = [t for t in trades_today if t.get('status') == 'CLOSED']

        wins = len([t for t in closed_trades if (t.get('pnl', 0) or 0) > 0])
        losses = len([t for t in closed_trades if (t.get('pnl', 0) or 0) < 0])
        win_rate = (wins / len(closed_trades) * 100) if closed_trades else 0

        total_pnl = sum(t.get('pnl', 0) or 0 for t in closed_trades)

        pnl_values = [t.get('pnl', 0) or 0 for t in closed_trades]
        best_trade = max(pnl_values) if pnl_values else 0
        worst_trade = min(pnl_values) if pnl_values else 0

        # Get current status
        balance = collector.fetch_balance()
        open_positions = len(db.get_open_trades())

        # Prepare stats
        stats = {
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'open_positions': open_positions,
            'balance': balance
        }

        # Send report
        telegram.send_daily_report(stats)

        logger.info(f"Daily report sent: {total_trades} trades, PnL: {total_pnl:+.2f} USDT")

    except Exception as e:
        logger.error(f"Error generating daily report: {e}", exc_info=True)


def setup_scheduler():
    """Setup scheduled jobs."""
    logger.info("Setting up scheduler...")

    analysis_interval = config['schedule']['analysis_interval_minutes']
    monitor_interval = config['schedule']['monitor_interval_minutes']

    # Schedule analysis for each symbol
    for symbol in config['symbols']:
        schedule.every(analysis_interval).minutes.do(run_analysis, symbol=symbol)
        logger.info(f"Scheduled analysis for {symbol} every {analysis_interval} minutes")

    # Schedule position monitoring
    schedule.every(monitor_interval).minutes.do(run_monitor)
    logger.info(f"Scheduled position monitor every {monitor_interval} minutes")

    # Schedule daily report at 23:55
    schedule.every().day.at("23:55").do(run_daily_report)
    logger.info("Scheduled daily report at 23:55")


def print_banner():
    """Print startup banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║        🤖 CRYPTO TRADING BOT - AI POWERED 🤖          ║
    ║                                                       ║
    ║              Paper Trading on Bybit Testnet          ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

    # Print config summary
    print(f"\n📊 Configuration Summary:")
    print(f"   • Exchange: {config['exchange']['name']} ({'TESTNET' if config['exchange']['testnet'] else 'MAINNET'})")
    print(f"   • Symbols: {', '.join(config['symbols'])}")
    print(f"   • Timeframes: {', '.join(config['timeframes'])}")
    print(f"   • Max Risk/Trade: {config['risk']['max_risk_per_trade'] * 100}%")
    print(f"   • Max Daily Drawdown: {config['risk']['max_daily_drawdown'] * 100}%")
    print(f"   • Max Open Positions: {config['risk']['max_open_positions']}")
    print(f"   • Analysis Interval: {config['schedule']['analysis_interval_minutes']} minutes")
    print(f"   • Telegram: {'Enabled' if config.get('telegram', {}).get('enabled') else 'Disabled'}")

    # Mode status
    if demo_mode:
        print(f"   • Mode: DEMO MODE (public API only, no authentication)")
    elif dry_run:
        print(f"   • Mode: DRY RUN (analysis only, no trades)")
    else:
        print(f"   • Mode: LIVE TRADING")
    print()


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    logger.info("\n\nShutdown signal received. Cleaning up...")

    # Send shutdown notification
    if telegram:
        telegram.send_shutdown_notification()

    # Close database
    if db:
        db.close()

    logger.info("Goodbye! 👋")
    sys.exit(0)


def main():
    """Main entry point."""
    global config, logger, dry_run, demo_mode

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI-Powered Crypto Trading Bot')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode (no real trades)')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (public API only, no authentication)')
    parser.add_argument('--once', action='store_true', help='Run one analysis cycle and exit')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    args = parser.parse_args()

    dry_run = args.dry_run
    demo_mode = args.demo

    # If demo mode, also enable dry_run
    if demo_mode:
        dry_run = True

    # Setup logger first
    logger = setup_logger(
        name='crypto_bot',
        log_file='./bot.log',
        level='INFO'
    )

    # Load configuration
    config = load_config(args.config)

    # Update logger with config
    logger = setup_logger(
        name='crypto_bot',
        log_file=config['logging']['file'],
        level=config['logging']['level']
    )

    # Print banner
    print_banner()

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize modules
    try:
        initialize_modules()
    except Exception as e:
        logger.error(f"Failed to initialize modules: {e}")
        sys.exit(1)

    # Test exchange connection
    logger.info("Testing exchange connection...")
    if not collector.test_connection():
        logger.error("Exchange connection test failed. Exiting.")
        if not demo_mode:
            sys.exit(1)
        else:
            logger.warning("Demo mode: Continuing despite connection test failure")
    else:
        logger.info("Exchange connection successful ✓")

    # Send startup notification
    mode_str = 'DEMO' if demo_mode else ('DRY RUN' if dry_run else 'LIVE')
    config_summary = (
        f"Exchange: {config['exchange']['name']}\n"
        f"Symbols: {', '.join(config['symbols'])}\n"
        f"Mode: {mode_str}\n"
        f"Balance: {initial_balance:.2f} USDT"
    )
    telegram.send_startup_notification(config_summary)

    # Run once mode
    if args.once:
        logger.info("Running in ONCE mode - single analysis cycle")
        for symbol in config['symbols']:
            run_analysis(symbol)
        run_monitor()
        logger.info("Single cycle complete. Exiting.")
        sys.exit(0)

    # Setup scheduler
    setup_scheduler()

    # Run initial analysis immediately
    logger.info("Running initial analysis for all symbols...")
    for symbol in config['symbols']:
        run_analysis(symbol)

    # Main loop
    logger.info("🚀 Bot is now running. Press Ctrl+C to stop.\n")

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
            time.sleep(60)  # Wait before continuing


if __name__ == "__main__":
    main()
