# 🔑 Binance Testnet Setup Guide

## Why Binance Testnet?

✅ **Easy to access** - Simple registration
✅ **Free testnet funds** - 1000 USDT given automatically
✅ **Reliable API** - Well-documented and stable
✅ **No verification** - Start trading immediately
✅ **Perfect for testing** - Identical to real Binance Futures

## Step-by-Step Setup

### 1. Register for Binance Testnet

**Visit:** https://testnet.binancefuture.com/

1. Click **"Register"** (top right)
2. Enter an **email** (can be fake, e.g., `test@test.com`)
3. Create a **password**
4. Click **"Create Account"**
5. ✅ **Done!** You're logged in

**No email verification needed!**

### 2. Get Free Testnet Funds

After logging in:
1. You'll automatically have **1000 USDT** in your account
2. Go to **"Wallet"** → **"Futures"** to see your balance
3. If you need more funds, there's a **"Get Test Funds"** button

### 3. Create API Keys

1. Click your **email** (top right) → **"API Management"**
2. Click **"Create API"** button
3. **Label**: Enter any name (e.g., "Trading Bot")
4. Click **"Create"**
5. ✅ You'll see:
   - **API Key**: Long string starting with letters/numbers
   - **Secret Key**: Even longer string (shown only once!)

**IMPORTANT:** Copy both keys immediately!

### 4. Configure API Key Permissions

After creating the API key:
1. You'll see your API key in the list
2. Click **"Edit"** next to it
3. Enable these permissions:
   - ✅ **Enable Reading**
   - ✅ **Enable Futures**
   - ❌ Leave others unchecked
4. **IP Restriction**: Leave empty (or add your IP if you know it)
5. Click **"Save"**

### 5. Update config.yaml

Open `config.yaml` in the crypto-bot folder and update:

```yaml
exchange:
  name: binance
  testnet: true
  api_key: "YOUR_API_KEY_HERE"
  api_secret: "YOUR_SECRET_KEY_HERE"
```

**Example** (with fake keys):
```yaml
exchange:
  name: binance
  testnet: true
  api_key: "d9pQ2K8xF7vR3mL5nB4hT6wJ1sY0gC2aE8iU9oP"
  api_secret: "X5zM9nB8vC3xW2qL7pK4jH1sG6fD9aS0iU5yT3rE2wQ1mL8kJ7hG6fD5cA4zX3vB2nM1"
```

### 6. Test Your Setup

Run the test connection script:

```bash
cd crypto-bot
python3 test_connection.py
```

You should see:
```
✓ SUCCESS with Linear Testnet
  USDT Balance: 1000.0
```

If successful, run the bot in demo mode:
```bash
python3 main.py --demo --once
```

## 🎯 Quick Reference

| Item | Value |
|------|-------|
| **Website** | https://testnet.binancefuture.com/ |
| **Registration** | No verification needed |
| **Free Funds** | 1000 USDT (auto-credited) |
| **API Docs** | https://testnet.binancefuture.com/en/futures/BTCUSDT |
| **Support** | Community forums |

## Troubleshooting

### "Invalid API Key"
- Make sure you're using **Futures** testnet (not Spot testnet)
- Check that **"Enable Futures"** permission is enabled
- Verify you copied the ENTIRE API key and secret (they're long!)
- No extra spaces before or after the keys in `config.yaml`

### "IP Restricted"
- Go to API Management → Edit your API
- Set IP restriction to **"Unrestricted"**
- Or add your current IP address

### "Insufficient Balance"
- Go to https://testnet.binancefuture.com/
- Click **"Get Test Funds"** button
- You'll receive 1000 USDT

### Can't Access Website
- Try: https://testnet.binancefuture.com/
- Or: https://testnet.binance.vision/
- Clear browser cache and try again

## 🔐 Security Notes

This is a TESTNET - not real money!
- ✅ Safe to experiment
- ✅ Can share API keys publicly (they're worthless)
- ✅ Can reset and create new keys anytime
- ❌ Never use mainnet keys for testing!

## Next Steps

After setup is complete:

1. **Test in Demo Mode** (no API keys needed):
   ```bash
   python3 main.py --demo --once
   ```

2. **Test with Real Testnet Keys** (with your new API keys):
   ```bash
   python3 main.py --dry-run --once
   ```

3. **Run Paper Trading** (execute trades on testnet):
   ```bash
   python3 main.py --once
   ```

4. **Run Continuously**:
   ```bash
   python3 main.py
   ```

---

**Happy Testing! 🚀**

Need help? Check the main README.md or run `python3 test_connection.py` to diagnose issues.
