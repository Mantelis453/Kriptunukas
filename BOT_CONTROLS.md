# 🎮 Bot Control Commands

## Current Status: ✅ RUNNING

Your bot is running in the background analyzing markets!

## 🛑 Stop the Bot

### Quick Stop:
```bash
./stop_bot.sh
```

### Manual Stop:
```bash
pkill -f "python3 main.py"
```

### Verify it stopped:
```bash
ps aux | grep "python3 main.py" | grep -v grep
```
(Should show nothing if stopped)

## 🔄 Restart the Bot

```bash
python3 main.py --demo
```

## 📊 Monitor the Bot

### View Live Logs:
```bash
tail -f bot.log
```

### View Last 50 Log Lines:
```bash
tail -50 bot.log
```

### Check Latest Signals:
```bash
sqlite3 bot.db "SELECT symbol, action, confidence, substr(reasoning, 1, 80) as reason FROM signals ORDER BY created_at DESC LIMIT 5;"
```

### Check Database Size:
```bash
ls -lh bot.db
```

### View All Tables:
```bash
sqlite3 bot.db ".tables"
```

## 📱 Telegram Commands

Your Telegram bot: **@balciobot**

You'll receive messages for:
- 🤖 Bot startup/shutdown
- 🟢 BUY signals (confidence ≥ 70%)
- 🔴 SELL signals (confidence ≥ 70%)
- 📊 Daily reports (23:55)
- 🚨 Error alerts

## 🔧 Change Settings

Edit `config.yaml` and restart the bot:

### Change Analysis Frequency:
```yaml
schedule:
  analysis_interval_minutes: 30  # Change from 60 to 30
```

### Add More Symbols:
```yaml
symbols:
  - BTCUSDT
  - ETHUSDT
  - SOLUSDT  # Add this
  - BNBUSDT  # Add this
```

### Adjust Risk:
```yaml
risk:
  max_risk_per_trade: 0.01  # Change from 2% to 1%
  max_open_positions: 5      # Change from 3 to 5
```

After editing, stop and restart:
```bash
./stop_bot.sh
python3 main.py --demo
```

## 🐛 Troubleshooting

### Bot Not Responding?

Check if it's running:
```bash
ps aux | grep "python3 main.py" | grep -v grep
```

Check logs for errors:
```bash
tail -50 bot.log | grep ERROR
```

### No Telegram Messages?

Test Telegram:
```bash
python3 test_telegram.py
```

Check config:
```bash
cat config.yaml | grep -A 3 telegram
```

### High CPU Usage?

Normal during analysis (AI calls). Check current activity:
```bash
tail -20 bot.log
```

## 📈 Performance Stats

### View Trading Statistics:
```bash
sqlite3 bot.db << EOF
SELECT
    symbol,
    action,
    AVG(confidence) as avg_confidence,
    COUNT(*) as total_signals
FROM signals
GROUP BY symbol, action;
EOF
```

### View Today's Activity:
```bash
sqlite3 bot.db << EOF
SELECT
    symbol,
    action,
    confidence,
    datetime(created_at, 'localtime') as time
FROM signals
WHERE DATE(created_at) = DATE('now')
ORDER BY created_at DESC;
EOF
```

## 🚀 Different Run Modes

### Demo Mode (Current):
```bash
python3 main.py --demo
```
- No API keys needed
- Real market data
- Mock balance: $10,000

### Dry Run (With API Keys):
```bash
python3 main.py --dry-run
```
- Uses real API keys
- Real balance check
- No trade execution

### Live Paper Trading (With API Keys):
```bash
python3 main.py
```
- Executes real trades on testnet
- Full risk management
- Real position tracking

### Run Once (Test):
```bash
python3 main.py --demo --once
```
- Single analysis cycle
- Then exits

## 📋 Daily Routine

### Morning:
```bash
# Check bot is running
ps aux | grep "python3 main.py" | grep -v grep

# View overnight signals
sqlite3 bot.db "SELECT symbol, action, confidence FROM signals WHERE DATE(created_at) = DATE('now') ORDER BY created_at DESC;"
```

### Evening:
- Check Telegram for daily report (arrives at 23:55)
- Review bot.log for any errors
- Check database growth

### Weekly:
- Archive old logs: `mv bot.log bot_$(date +%Y%m%d).log`
- Backup database: `cp bot.db bot_backup_$(date +%Y%m%d).db`

## 🎯 Quick Reference

| Command | Purpose |
|---------|---------|
| `./stop_bot.sh` | Stop the bot |
| `python3 main.py --demo` | Start in demo mode |
| `tail -f bot.log` | Watch logs live |
| `python3 test_telegram.py` | Test Telegram |
| `sqlite3 bot.db ".tables"` | Show database tables |

## 📚 Documentation

- `RUN_CONTINUOUSLY.md` - Continuous mode guide
- `TELEGRAM_GUIDE.md` - Telegram setup
- `BINANCE_TESTNET_SETUP.md` - Exchange setup
- `README.md` - Main documentation

---

**Bot is running! Check your Telegram for updates** 📱
