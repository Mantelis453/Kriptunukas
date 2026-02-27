"""
SQLite database operations for the crypto trading bot.
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Database:
    """Handles all database operations for the trading bot."""

    def __init__(self, db_path: str = "./bot.db"):
        """
        Initialize database connection and create tables.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        # Create directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        logger.info(f"Database initialized at {db_path}")

    def _create_tables(self):
        """Create all required tables if they don't exist."""
        cursor = self.conn.cursor()

        # Candles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS candles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                timeframe TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume REAL NOT NULL,
                UNIQUE(symbol, timeframe, timestamp)
            )
        """)

        # Signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                reasoning TEXT,
                entry_price REAL,
                stop_loss REAL,
                take_profit REAL,
                position_size_pct REAL,
                indicators_json TEXT,
                ai_raw_response TEXT,
                prompt_version TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Trades table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id INTEGER,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity REAL NOT NULL,
                entry_price REAL NOT NULL,
                exit_price REAL,
                stop_loss REAL,
                take_profit REAL,
                status TEXT DEFAULT 'OPEN',
                pnl REAL,
                pnl_percent REAL,
                exchange_order_id TEXT,
                opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                FOREIGN KEY (signal_id) REFERENCES signals(id)
            )
        """)

        # Portfolio snapshots table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_balance REAL NOT NULL,
                available_balance REAL NOT NULL,
                unrealized_pnl REAL DEFAULT 0,
                open_positions INTEGER DEFAULT 0,
                daily_pnl REAL DEFAULT 0,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # AI logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT,
                model TEXT DEFAULT 'claude_cli',
                latency_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_candles_symbol_timeframe
            ON candles(symbol, timeframe, timestamp DESC)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_trades_symbol_status
            ON trades(symbol, status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_signals_created
            ON signals(created_at DESC)
        """)

        self.conn.commit()
        logger.info("Database tables created/verified")

    def save_candles(self, symbol: str, timeframe: str, df) -> int:
        """
        Save OHLCV candles to database.

        Args:
            symbol: Trading pair symbol
            timeframe: Candle timeframe
            df: Pandas DataFrame with candle data

        Returns:
            Number of rows inserted
        """
        cursor = self.conn.cursor()
        inserted = 0

        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO candles
                    (symbol, timeframe, timestamp, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    symbol,
                    timeframe,
                    int(row['timestamp']),
                    float(row['open']),
                    float(row['high']),
                    float(row['low']),
                    float(row['close']),
                    float(row['volume'])
                ))
                if cursor.rowcount > 0:
                    inserted += 1
            except Exception as e:
                logger.error(f"Error saving candle: {e}")

        self.conn.commit()
        return inserted

    def save_signal(self, signal_dict: Dict[str, Any]) -> int:
        """
        Save AI trading signal to database.

        Args:
            signal_dict: Dictionary containing signal data

        Returns:
            ID of inserted signal
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO signals
            (symbol, action, confidence, reasoning, entry_price, stop_loss,
             take_profit, position_size_pct, indicators_json, ai_raw_response, prompt_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            signal_dict.get('symbol'),
            signal_dict.get('action'),
            signal_dict.get('confidence'),
            signal_dict.get('reasoning'),
            signal_dict.get('entry_price'),
            signal_dict.get('stop_loss'),
            signal_dict.get('take_profit'),
            signal_dict.get('position_size_pct'),
            json.dumps(signal_dict.get('indicators', {})),
            signal_dict.get('ai_raw_response'),
            signal_dict.get('prompt_version', 'v1')
        ))

        self.conn.commit()
        return cursor.lastrowid

    def save_trade(self, trade_dict: Dict[str, Any]) -> int:
        """
        Save trade to database.

        Args:
            trade_dict: Dictionary containing trade data

        Returns:
            ID of inserted trade
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO trades
            (signal_id, symbol, side, quantity, entry_price, stop_loss,
             take_profit, status, exchange_order_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade_dict.get('signal_id'),
            trade_dict.get('symbol'),
            trade_dict.get('side'),
            trade_dict.get('quantity'),
            trade_dict.get('entry_price'),
            trade_dict.get('stop_loss'),
            trade_dict.get('take_profit'),
            trade_dict.get('status', 'OPEN'),
            trade_dict.get('exchange_order_id')
        ))

        self.conn.commit()
        return cursor.lastrowid

    def update_trade(self, trade_id: int, updates_dict: Dict[str, Any]):
        """
        Update existing trade in database.

        Args:
            trade_id: ID of trade to update
            updates_dict: Dictionary of fields to update
        """
        cursor = self.conn.cursor()

        # Build UPDATE query dynamically
        fields = []
        values = []
        for key, value in updates_dict.items():
            fields.append(f"{key} = ?")
            values.append(value)

        if 'status' in updates_dict and updates_dict['status'] == 'CLOSED':
            fields.append("closed_at = CURRENT_TIMESTAMP")

        values.append(trade_id)
        query = f"UPDATE trades SET {', '.join(fields)} WHERE id = ?"

        cursor.execute(query, values)
        self.conn.commit()

    def save_portfolio_snapshot(self, snapshot_dict: Dict[str, Any]) -> int:
        """
        Save portfolio snapshot to database.

        Args:
            snapshot_dict: Dictionary containing portfolio data

        Returns:
            ID of inserted snapshot
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO portfolio_snapshots
            (total_balance, available_balance, unrealized_pnl, open_positions, daily_pnl)
            VALUES (?, ?, ?, ?, ?)
        """, (
            snapshot_dict.get('total_balance'),
            snapshot_dict.get('available_balance'),
            snapshot_dict.get('unrealized_pnl', 0),
            snapshot_dict.get('open_positions', 0),
            snapshot_dict.get('daily_pnl', 0)
        ))

        self.conn.commit()
        return cursor.lastrowid

    def save_ai_log(self, log_dict: Dict[str, Any]) -> int:
        """
        Save AI interaction log to database.

        Args:
            log_dict: Dictionary containing AI log data

        Returns:
            ID of inserted log
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO ai_logs
            (symbol, prompt, response, model, latency_ms)
            VALUES (?, ?, ?, ?, ?)
        """, (
            log_dict.get('symbol'),
            log_dict.get('prompt'),
            log_dict.get('response'),
            log_dict.get('model', 'claude_cli'),
            log_dict.get('latency_ms')
        ))

        self.conn.commit()
        return cursor.lastrowid

    def get_open_trades(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Get all open trades, optionally filtered by symbol.

        Args:
            symbol: Trading pair symbol (optional)

        Returns:
            List of trade dictionaries
        """
        cursor = self.conn.cursor()

        if symbol:
            cursor.execute("""
                SELECT * FROM trades
                WHERE status = 'OPEN' AND symbol = ?
                ORDER BY opened_at DESC
            """, (symbol,))
        else:
            cursor.execute("""
                SELECT * FROM trades
                WHERE status = 'OPEN'
                ORDER BY opened_at DESC
            """)

        return [dict(row) for row in cursor.fetchall()]

    def get_trades_today(self) -> List[Dict]:
        """
        Get all trades from today.

        Returns:
            List of trade dictionaries
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM trades
            WHERE DATE(opened_at) = DATE('now')
            ORDER BY opened_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    def get_last_trade(self, symbol: str) -> Optional[Dict]:
        """
        Get the most recent trade for a symbol.

        Args:
            symbol: Trading pair symbol

        Returns:
            Trade dictionary or None
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM trades
            WHERE symbol = ?
            ORDER BY opened_at DESC
            LIMIT 1
        """, (symbol,))

        row = cursor.fetchone()
        return dict(row) if row else None

    def get_latest_signal(self, symbol: str) -> Optional[Dict]:
        """
        Get the most recent signal for a symbol.

        Args:
            symbol: Trading pair symbol

        Returns:
            Signal dictionary or None
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM signals
            WHERE symbol = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (symbol,))

        row = cursor.fetchone()
        return dict(row) if row else None

    def close(self):
        """Close database connection."""
        self.conn.close()
        logger.info("Database connection closed")
