# 🤖 Kriptunukas - AI-Powered Crypto Trading Bot

<div align="center">

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange.svg)](https://ai.google.dev/)

**AI-powered cryptocurrency trading bot with Gemini integration and Docker VPS deployment**

[Features](#-features) • [Quick Start](#-quick-start) • [VPS Deploy](#-vps-deployment) • [Documentation](#-documentation)

</div>

---

## 🎯 What is Kriptunukas?

Kriptunukas is a production-ready cryptocurrency trading bot that uses **Google Gemini AI** to analyze market data and generate trading signals. It's designed for **paper trading** on Binance testnet, making it perfect for learning and testing strategies without risking real money.

## ✨ Key Highlights

- 🧠 **AI-Powered**: Google Gemini 1.5 Flash for lightning-fast analysis (1-2s)
- 🆓 **Completely Free**: Free Gemini API + Binance testnet (no costs!)
- 🐳 **Docker Ready**: One-command VPS deployment
- 📊 **Technical Analysis**: RSI, MACD, Bollinger Bands, EMAs, volume analysis
- 🛡️ **Risk Management**: Position sizing, stop-loss, take-profit, drawdown limits
- 📱 **Telegram Alerts**: Real-time notifications for all trading signals
- 💾 **Database Tracking**: Complete trade history in SQLite
- 🔄 **Auto-Restart**: Survives crashes and VPS reboots

## 💰 Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| **Gemini AI API** | $0 | Free tier (60 req/min) |
| **Binance Testnet** | $0 | Paper trading only |
| **Telegram Bot** | $0 | Free |
| **VPS Hosting** | $5-6/mo | DigitalOcean, Vultr, Linode |
| **Total** | **$5-6/month** | For 24/7 automated trading! |

## 🚀 Quick Start

### Option 1: Local Testing (5 minutes)

1. **Get Gemini API key** (free): https://makersuite.google.com/app/apikey

2. **Clone and configure:**
```bash
git clone https://github.com/Mantelis453/Kriptunukas.git
cd Kriptunukas
cp config.yaml.example config.yaml
nano config.yaml  # Add your API keys
```

3. **Install and run:**
```bash
pip install -r requirements.txt
python3 main.py --demo --once
```

### Option 2: VPS Deployment (15 minutes)

See [🐳 VPS Deployment](#-vps-deployment) below for complete guide.

---

## 🐳 VPS Deployment

Deploy to a VPS for 24/7 automated trading:

**1. Setup VPS:**
```bash
ssh root@YOUR_VPS_IP

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose -y
```

**2. Upload code:**
```bash
git clone https://github.com/Mantelis453/Kriptunukas.git
cd Kriptunukas
```

**3. Configure:**
```bash
cp config.yaml.example config.yaml
nano config.yaml  # Add your API keys
```

**4. Deploy:**
```bash
./deploy.sh
```

**Done!** Bot runs 24/7 automatically! 🎉

### Management Commands
```bash
docker-compose logs -f      # View logs
docker-compose ps           # Check status
docker-compose restart      # Restart bot
./update.sh                 # Update bot
./backup.sh                 # Backup database
```

---

## 🔑 Required API Keys

| Service | Purpose | Get It | Required |
|---------|---------|--------|----------|
| **Gemini AI** | Trading analysis | [Free Key](https://makersuite.google.com/app/apikey) | ✅ Yes |
| **Binance Testnet** | Paper trading | [Testnet](https://testnet.binancefuture.com/) | ✅ Yes |
| **Telegram Bot** | Notifications | [@BotFather](https://t.me/botfather) | ⚠️ Optional |

## 📊 Project Structure

```
Kriptunukas/
├── 🐳 Docker Files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── 🛠️ Scripts
│   ├── deploy.sh          # One-command deployment
│   ├── update.sh          # Easy updates
│   └── backup.sh          # Database backups
│
├── 🤖 Application
│   ├── main.py            # Entry point
│   ├── config.yaml.example
│   ├── requirements.txt
│   ├── ai/                # Gemini AI integration
│   ├── data/              # Market data & indicators
│   ├── trading/           # Order execution & risk
│   ├── db/                # Database operations
│   ├── notifications/     # Telegram alerts
│   └── utils/             # Logging utilities
│
└── 📚 Documentation (15+ guides)
    ├── VPS_QUICKSTART.md
    ├── VPS_DEPLOYMENT.md
    ├── DEPLOYMENT_CHECKLIST.md
    └── ...
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

1. **Data Collection**: Fetches OHLCV candles from Binance testnet
2. **Indicator Calculation**: Computes RSI, MACD, Bollinger Bands, EMAs, ATR, volume
3. **AI Analysis**: Sends indicators to Gemini AI for trading signal (1-2s response)
4. **Risk Validation**: Checks position limits, drawdown, cooldown periods
5. **Trade Execution**: Places orders with stop-loss and take-profit on testnet
6. **Position Monitoring**: Tracks open positions and updates PnL every 5 minutes
7. **Daily Reporting**: Generates statistics and performance reports at 23:55 UTC
8. **Telegram Alerts**: Real-time notifications for all signals and errors

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

**"Gemini API key not configured"**
- Get free key at: https://makersuite.google.com/app/apikey
- Update `gemini_api_key` in config.yaml

**"API key is invalid"**
- Ensure you're using Binance TESTNET credentials
- Check that API key has trading permissions
- Visit: https://testnet.binancefuture.com/

**"Failed to fetch candles"**
- Check internet connection
- Verify Binance testnet is accessible

**Bot not analyzing?**
- Check logs: `docker-compose logs` or `tail bot.log`
- Verify Gemini API key is set
- Test connection: `python3 test_connection.py`

**No Telegram notifications?**
- Test: `python3 test_telegram.py`
- Verify bot token and chat ID in config.yaml

For detailed guides, see:
- **VPS_QUICKSTART.md** - Quick deployment
- **VPS_DEPLOYMENT.md** - Detailed setup
- **GEMINI_SETUP.md** - API configuration

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
