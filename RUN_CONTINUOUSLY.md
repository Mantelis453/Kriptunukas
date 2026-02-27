# 🔄 Running the Bot Continuously

## What is Continuous Mode?

In continuous mode, the bot will:
- 📊 Analyze markets every **60 minutes** (configurable)
- 👀 Monitor open positions every **5 minutes**
- 📈 Send daily report at **23:55**
- 📱 Send Telegram notifications for all signals
- 💾 Save all data to database
- 🔁 Run forever until you stop it

## Run Continuous Demo Mode

**Start the bot:**
```bash
python3 main.py --demo
```

**What you'll see:**
```
🤖 CRYPTO TRADING BOT - AI POWERED 🤖

📊 Configuration Summary:
   • Exchange: binance (TESTNET)
   • Symbols: BTCUSDT, ETHUSDT
   • Mode: DEMO MODE

🚀 Bot is now running. Press Ctrl+C to stop.

============================================================
Running analysis for BTCUSDT
============================================================
...
```

## What Happens Next?

### Initial Run (Right Now)
- Analyzes BTCUSDT and ETHUSDT immediately
- Sends startup notification to Telegram
- Saves signals to database

### Every 60 Minutes
- Re-analyzes all symbols
- Checks for new trading opportunities
- Sends Telegram alerts for BUY/SELL/CLOSE signals
- Saves new data

### Every 5 Minutes
- Monitors any open positions
- Checks if stop-loss or take-profit hit
- Updates position status
- Takes portfolio snapshot

### Daily at 23:55
- Generates trading report
- Calculates win rate, PnL
- Sends comprehensive report to Telegram

## How to Stop the Bot

**Press**: `Ctrl+C` (or `Cmd+C` on Mac)

You'll see:
```
Shutdown signal received. Cleaning up...
🛑 BOT STOPPED (sent to Telegram)
Goodbye! 👋
```

## Run in Background (Optional)

To run the bot in the background and close terminal:

**Using screen:**
```bash
screen -S tradingbot
python3 main.py --demo
# Press Ctrl+A then D to detach

# To reattach later:
screen -r tradingbot
```

**Using nohup:**
```bash
nohup python3 main.py --demo > bot_output.log 2>&1 &

# To stop:
ps aux | grep main.py
kill <PID>
```

## Monitor the Bot

### View Logs (Real-time)
```bash
tail -f bot.log
```

### Check Database
```bash
sqlite3 bot.db "SELECT symbol, action, confidence, datetime(created_at) FROM signals ORDER BY created_at DESC LIMIT 10;"
```

### View Telegram
All important events are sent to your Telegram bot!

## Customize Schedule

Edit `config.yaml`:
```yaml
schedule:
  analysis_interval_minutes: 60   # Change to 30, 15, etc.
  monitor_interval_minutes: 5     # Change to 1, 2, 10, etc.
```

**Examples:**
- `15` minutes = 4 analyses per hour
- `30` minutes = 2 analyses per hour
- `120` minutes = 1 analysis every 2 hours

## Modes Available

### 1. Demo Mode (Current)
```bash
python3 main.py --demo
```
- ✅ No API keys needed
- ✅ Real market data
- ✅ Real AI analysis
- ❌ No real trades
- 💰 Mock $10,000 balance

### 2. Dry Run Mode (With API Keys)
```bash
python3 main.py --dry-run
```
- ✅ Real API connection
- ✅ Real balance check
- ✅ Full analysis
- ❌ No trade execution
- 📊 Analysis only

### 3. Live Paper Trading (With API Keys)
```bash
python3 main.py
```
- ✅ Real API connection
- ✅ Executes trades on testnet
- ✅ Full risk management
- 💹 Real position tracking
- 📈 Real PnL calculation

## Expected Behavior

### First Hour:
```
10:00 - Initial analysis (BTCUSDT, ETHUSDT)
10:05 - Position monitor check
10:10 - Position monitor check
...
11:00 - Next analysis cycle
```

### Telegram Messages You'll Get:
1. **Now**: Startup notification
2. **Every hour**: If BUY/SELL signal (confidence ≥ 70%)
3. **23:55 daily**: Daily performance report
4. **Any errors**: Error alerts

### Database Growth:
- **signals table**: +2 rows per hour (per symbol)
- **ai_logs table**: +2 rows per hour
- **portfolio_snapshots**: +12 rows per hour (every 5 min)

After 24 hours: ~500 database entries

## Performance Tips

### For Testing (Fast):
```yaml
schedule:
  analysis_interval_minutes: 5   # Analyze every 5 minutes
  monitor_interval_minutes: 1    # Check every minute
```

### For Production (Slow):
```yaml
schedule:
  analysis_interval_minutes: 120  # Analyze every 2 hours
  monitor_interval_minutes: 10    # Check every 10 minutes
```

### Current Settings:
```yaml
schedule:
  analysis_interval_minutes: 60   # Default
  monitor_interval_minutes: 5     # Default
```

## Troubleshooting

### Bot stops unexpectedly
- Check `bot.log` for errors
- Ensure stable internet connection
- Verify Claude CLI is accessible

### No Telegram notifications
- Confirm `enabled: true` in config.yaml
- Run `python3 test_telegram.py`
- Check Telegram app isn't blocking bot

### High CPU usage
- Normal during analysis (Claude AI call)
- Idle between cycles uses minimal CPU

### Database getting large
- Rotate logs: Delete old bot.log entries
- Clean database: Archive old signals
- Current size is small (~1MB per week)

## What to Watch For

### Good Signs ✅
- Regular log entries every hour
- Telegram notifications arriving
- Database growing steadily
- No error messages

### Warning Signs ⚠️
- Repeated connection errors
- No logs for >1 hour
- Telegram not responding
- AI timeout errors

## Next Steps

1. **Start the bot**: `python3 main.py --demo`
2. **Watch Telegram**: You'll get startup notification
3. **Wait ~5 minutes**: See position monitoring logs
4. **Wait ~1 hour**: See next analysis cycle
5. **Check database**: See accumulated data

**The bot will run until you press Ctrl+C!**

---

**Ready?** Let's start it! 🚀
