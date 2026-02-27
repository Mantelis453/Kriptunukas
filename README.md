# 🤖 Crypto Trading Bot - AI Powered

A sophisticated paper trading bot for Bybit testnet featuring AI-powered analysis using Claude CLI.

## 📋 Features

- **AI-Powered Analysis**: Uses Claude CLI for intelligent trading signals
- **Technical Indicators**: RSI, MACD, Bollinger Bands, EMA, ATR, and more
- **Risk Management**: Position sizing, stop-loss, take-profit, daily drawdown limits
- **Paper Trading**: Safe testing on Bybit testnet
- **Telegram Notifications**: Real-time alerts for trades and daily reports
- **Database Tracking**: SQLite database for all trades, signals, and AI logs
- **Scheduler**: Automated analysis and monitoring

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd crypto-bot
pip3 install -r requirements.txt
```

### 2. Configure API Keys

Edit `config.yaml` and add your credentials:

```yaml
exchange:
  api_key: "YOUR_BYBIT_TESTNET_API_KEY"
  api_secret: "YOUR_BYBIT_TESTNET_API_SECRET"
```

**Get Bybit Testnet API Keys:**
1. Visit https://testnet.bybit.com
2. Register for an account
3. Go to API Management
4. Create new API key

### 3. (Optional) Configure Telegram

To receive notifications:

```yaml
telegram:
  bot_token: "YOUR_TELEGRAM_BOT_TOKEN"
  chat_id: "YOUR_TELEGRAM_CHAT_ID"
  enabled: true
```

**Get Telegram Bot Token:**
1. Message @BotFather on Telegram
2. Send /newbot and follow instructions
3. Copy the bot token
4. Message your bot to get your chat_id (use @userinfobot)

### 4. Install Claude CLI

The bot requires Claude CLI for AI analysis:

```bash
# Install Claude CLI (if not already installed)
# Visit: https://docs.anthropic.com/en/docs/claude-code
```

### 5. Run the Bot

**Dry Run Mode** (recommended first):
```bash
python3 main.py --dry-run --once
```

This runs one analysis cycle without executing real trades.

**Live Paper Trading:**
```bash
python3 main.py
```

The bot will run continuously, analyzing markets at configured intervals.

## 📊 Project Structure

```
crypto-bot/
├── config.yaml              # Configuration
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── data/
│   ├── collector.py         # Fetch data from Bybit
│   └── indicators.py        # Technical indicators
├── ai/
│   └── analyzer.py          # Claude CLI integration
├── trading/
│   ├── risk.py              # Risk management
│   └── executor.py          # Order execution
├── db/
│   └── database.py          # SQLite operations
├── notifications/
│   └── telegram.py          # Telegram alerts
└── utils/
    └── logger.py            # Logging
```

## ⚙️ Configuration

Key settings in `config.yaml`:

- **symbols**: Trading pairs (default: BTCUSDT, ETHUSDT)
- **risk.max_risk_per_trade**: 2% of portfolio per trade
- **risk.max_daily_drawdown**: 5% maximum daily loss
- **risk.max_open_positions**: Maximum 3 concurrent positions
- **schedule.analysis_interval_minutes**: Run analysis every 60 minutes
- **ai.min_confidence**: Minimum 70% confidence for trades

## 🔍 How It Works

1. **Data Collection**: Fetches OHLCV candles from Bybit
2. **Indicator Calculation**: Computes RSI, MACD, Bollinger Bands, EMAs, etc.
3. **AI Analysis**: Sends indicators to Claude CLI for trading signal
4. **Risk Validation**: Checks position limits, drawdown, cooldown periods
5. **Trade Execution**: Places orders with stop-loss and take-profit
6. **Position Monitoring**: Tracks open positions and updates PnL
7. **Daily Reporting**: Generates statistics and performance reports

## 📝 Command Line Options

```bash
python3 main.py [options]

Options:
  --dry-run    Run without executing real trades (analysis only)
  --once       Run one analysis cycle and exit (for testing)
  --config     Path to config file (default: config.yaml)
```

## 🗄️ Database

All data is stored in `bot.db` (SQLite):

- **candles**: Historical OHLCV data
- **signals**: AI trading signals
- **trades**: Executed trades with PnL
- **portfolio_snapshots**: Balance and performance over time
- **ai_logs**: All AI interactions

## 📈 Trading Rules

The AI follows conservative rules:

1. **BUY**: Only in BULLISH trend or NEUTRAL with RSI < 35
2. **SELL/CLOSE**: When RSI > 70 or trend reversal
3. **Stop-Loss**: 1.5x ATR from entry
4. **Take-Profit**: Minimum 2:1 reward-to-risk ratio
5. **Position Size**: 1-5% of portfolio based on confidence
6. **HOLD**: When uncertain - never forces trades

## 🛡️ Risk Management

Built-in safety features:

- Maximum 2% risk per trade
- Maximum 5% daily drawdown limit
- Maximum 3 open positions
- 2-hour cooldown between trades on same symbol
- Minimum 2:1 reward-to-risk ratio
- Emergency stop at 10% total drawdown

## 📱 Telegram Notifications

When enabled, you'll receive:

- 🟢 **Trade Alerts**: Buy/sell signals with reasoning
- 📊 **Daily Reports**: Win rate, PnL, best/worst trades
- 🚨 **Error Alerts**: System errors and issues
- 🤖 **Status Updates**: Bot startup/shutdown

## 🐛 Troubleshooting

**"API key is invalid"**
- Ensure you're using Bybit TESTNET credentials
- Check that API key has trading permissions

**"Claude CLI not found"**
- Install Claude CLI: https://docs.anthropic.com/en/docs/claude-code
- Ensure `claude` command is in your PATH

**"Failed to fetch candles"**
- Check internet connection
- Verify Bybit testnet is accessible

## ⚠️ Disclaimer

This is a paper trading bot for educational purposes. Even on testnet:
- Test thoroughly before any live trading
- Past performance doesn't guarantee future results
- Use at your own risk
- Not financial advice

## 📄 License

MIT License - feel free to modify and use as needed.

## 🤝 Contributing

This bot was built as a complete crypto trading system. Feel free to:
- Add new indicators
- Implement additional exchanges
- Enhance AI prompts
- Add more risk management rules

---

**Happy Trading! 🚀**
