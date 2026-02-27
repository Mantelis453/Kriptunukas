# 📱 Telegram Notifications Guide

## ✅ Your Setup Status

**Bot Name**: @balciobot (KriptoBotukas)
**Status**: ✅ ACTIVE and WORKING

Your Telegram is already configured and working! You should receive notifications when:
- 🤖 Bot starts/stops
- 🟢 BUY signals detected
- 🔴 SELL signals detected
- 📊 Daily trading reports
- 🚨 Errors occur

## 📨 What Messages You'll Receive

### 1. **Startup Notification**
When you run the bot:
```
🤖 BOT STARTED

Exchange: binance
Symbols: BTCUSDT, ETHUSDT
Mode: DEMO
Balance: 10000.00 USDT
```

### 2. **Trade Alerts** (when confidence >= 70%)
```
🟢 BUY SIGNAL

Symbol: BTCUSDT
Confidence: 85%
Entry: 68500
Stop Loss: 67800
Take Profit: 70200
Position Size: 3%

Reasoning:
Strong bullish momentum with RSI oversold...
```

### 3. **Daily Reports** (at 23:55)
```
📊 DAILY TRADING REPORT

Total Trades: 5
Wins: 3 | Losses: 2
Win Rate: 60.0%

📈 Total PnL: +125.50 USDT
Best Trade: +80.20 USDT
Worst Trade: -35.10 USDT

Open Positions: 1
Balance: 10125.50 USDT

✨ Profitable day!
```

### 4. **Error Alerts**
```
🚨 ERROR ALERT

Error: Failed to fetch market data

Details:
Network timeout after 3 retries
```

## 🧪 Test Your Setup

Run the test script anytime:
```bash
python3 test_telegram.py
```

You should see:
- ✅ Bot is VALID
- ✅ Chat ID is CORRECT
- ✅ Test message sent

## 🔧 Disable/Enable Telegram

### To Disable Notifications:
Edit `config.yaml`:
```yaml
telegram:
  enabled: false  # Change to false
```

### To Enable Again:
```yaml
telegram:
  enabled: true  # Change to true
```

## 🆕 Create a New Bot (Optional)

If you want to create a different Telegram bot:

1. **Open Telegram** and search for: `@BotFather`

2. **Send**: `/newbot`

3. **Choose a name**: "My Trading Bot"

4. **Choose username**: "mytradingbot123_bot" (must end with `_bot`)

5. **Copy the token** you receive (looks like: `123456789:ABCdefGHIjklMNOpqrs`)

6. **Start your bot**:
   - Click the link BotFather gives you
   - Click "START"
   - Send any message

7. **Get your Chat ID**:
   ```bash
   python3 test_telegram.py
   ```
   It will show your Chat ID

8. **Update config.yaml**:
   ```yaml
   telegram:
     bot_token: "your_new_token_here"
     chat_id: "your_chat_id_here"
     enabled: true
   ```

## 📲 Customize Messages

To customize notification messages, edit:
- `notifications/telegram.py`

For example, to change the startup message format, find `format_startup_notification()` and modify the text.

## 🔐 Security Note

Your bot token is visible in `config.yaml`. This is fine for a **testnet** trading bot, but:

⚠️ **Never share mainnet bot tokens**
⚠️ **Don't commit tokens to public GitHub repos**
✅ **Testnet bots are safe to share** (no real money)

## 🎯 Current Configuration

```yaml
telegram:
  bot_token: "8640047183:AAF6aG2L95UdK9aEGw6a50Z1_7J46hdOQhw"
  chat_id: "2053988717"
  enabled: true  ✅
```

## 🚀 Start Receiving Notifications

Run the bot in any mode:

**Demo Mode** (no API keys needed):
```bash
python3 main.py --demo --once
```

**With Binance API keys**:
```bash
python3 main.py --dry-run --once
```

**Live paper trading**:
```bash
python3 main.py
```

You'll receive notifications for:
- Bot startup
- Trading signals (HOLD signals are not sent, only BUY/SELL/CLOSE)
- Daily reports
- Errors

## ✅ Troubleshooting

### Not Receiving Messages?

1. **Check Telegram is enabled** in `config.yaml`
2. **Make sure you started the bot** - Click START in Telegram
3. **Check bot isn't blocked** - Unblock if needed
4. **Run test script**: `python3 test_telegram.py`

### Wrong Chat ID?

Run:
```bash
python3 test_telegram.py
```

It will show all available chat IDs. Update `config.yaml` with the correct one.

### Bot Token Invalid?

Create a new bot with @BotFather and update the token in `config.yaml`.

---

**Your Telegram is ready! 🎉**

Start the bot and check your Telegram app for notifications!
