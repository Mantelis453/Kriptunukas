# 🔧 Setup Guide - Step by Step

## Step 1: Get Bybit Testnet API Credentials

1. **Visit Bybit Testnet**
   - Go to: https://testnet.bybit.com
   - Click "Sign Up" (top right)
   - Create an account (use any email, no verification needed for testnet)

2. **Get Testnet Funds**
   - After logging in, you'll automatically receive testnet USDT
   - If not, look for "Testnet Faucet" or contact support

3. **Create API Key**
   - Go to Account → API Management
   - Click "Create New Key"
   - Set permissions:
     - ✅ Read
     - ✅ Trade (Contract)
     - ✅ Wallet (optional)
   - **Important**: Copy both API Key and Secret Key immediately!
   - Save them securely - you won't see the secret again

4. **Update config.yaml**
   ```yaml
   exchange:
     name: bybit
     testnet: true
     api_key: "YOUR_API_KEY_HERE"
     api_secret: "YOUR_SECRET_KEY_HERE"
   ```

## Step 2: Test Your Setup

Run a dry-run test:

```bash
cd crypto-bot
python3 main.py --dry-run --once
```

You should see:
- ✅ Configuration loaded
- ✅ Modules initialized
- ✅ Exchange connection successful
- ✅ Market data fetched
- ✅ Indicators calculated
- ✅ AI analysis completed

## Step 3: (Optional) Setup Telegram Notifications

1. **Create a Telegram Bot**
   - Open Telegram and message @BotFather
   - Send: `/newbot`
   - Choose a name: "My Trading Bot"
   - Choose a username: "mytradingbot123_bot" (must end with _bot)
   - Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Your Chat ID**
   - Message your new bot (click the link BotFather provides)
   - Send any message to it
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find "chat":{"id": **123456789**} in the response
   - That number is your chat_id

3. **Update config.yaml**
   ```yaml
   telegram:
     bot_token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
     chat_id: "123456789"
     enabled: true
   ```

## Step 4: Run Your First Analysis

Start the bot in dry-run mode:

```bash
python3 main.py --dry-run
```

The bot will:
- Fetch market data every 60 minutes
- Analyze with AI
- Log all signals (but not execute trades)
- Send Telegram notifications (if configured)

Press `Ctrl+C` to stop.

## Step 5: Go Live (Paper Trading)

When you're ready to enable paper trading:

```bash
python3 main.py
```

Now the bot will:
- Execute trades on Bybit testnet
- Track positions and PnL
- Send trade alerts
- Generate daily reports

## Common Issues

### Issue: "command not found: python3"
**Solution**: Try `python` instead of `python3`

### Issue: "ModuleNotFoundError"
**Solution**: Install dependencies:
```bash
pip3 install -r requirements.txt
```

### Issue: "Claude CLI not found"
**Solution**:
- Ensure Claude CLI is installed
- Check it's in your PATH: `which claude`
- If not, install from: https://docs.anthropic.com/en/docs/claude-code

### Issue: "API key is invalid"
**Solution**:
- Make sure you're using TESTNET credentials, not mainnet
- Verify the API key has trading permissions
- Check there are no extra spaces in config.yaml

### Issue: No Telegram messages
**Solution**:
- Send a message to your bot first
- Verify chat_id is correct
- Check bot_token is valid
- Ensure `enabled: true` in config

## Understanding the Output

When running, you'll see:

```
2026-02-26 00:18:55 - crypto_bot - INFO - Running analysis for BTCUSDT
2026-02-26 00:18:56 - crypto_bot - INFO - Fetching market data...
2026-02-26 00:18:57 - crypto_bot - INFO - Calculating technical indicators...
2026-02-26 00:18:58 - crypto_bot - INFO - Requesting AI analysis...
2026-02-26 00:19:05 - crypto_bot - INFO - AI Signal for BTCUSDT: HOLD (confidence: 65%)
```

### Signal Types:
- **HOLD**: AI recommends waiting (most common)
- **BUY**: AI identifies buying opportunity
- **SELL**: AI identifies selling opportunity
- **CLOSE**: AI recommends closing an open position

### Confidence Levels:
- **0-69%**: Signal rejected (below threshold)
- **70-79%**: Moderate confidence
- **80-89%**: High confidence
- **90-100%**: Very high confidence

## Next Steps

1. **Monitor Performance**
   - Check `bot.db` database for all trades
   - Review daily reports at 23:55
   - Analyze AI reasoning for each signal

2. **Adjust Configuration**
   - Modify risk parameters in `config.yaml`
   - Change analysis interval (default: 60 min)
   - Add/remove trading symbols

3. **Customize AI Prompts**
   - Edit `ai/analyzer.py`
   - Modify trading rules in the prompt
   - Add your own technical indicators

## Safety Reminders

- ✅ This is TESTNET (no real money)
- ✅ Test thoroughly before considering live trading
- ✅ Never share API keys
- ✅ Keep `testnet: true` in config
- ✅ Monitor the bot regularly
- ✅ Review all trades and signals

---

**Questions?** Check the main README.md or review the code comments.

**Ready to start?** Run `python3 main.py --dry-run --once` now!
