# 🎮 Demo Mode - Run Without Valid API Keys

Since you're having API key issues, here's how to test the bot in demo mode:

## Option 1: Use Public Data Only (Recommended for Testing)

I'll create a demo mode that:
- ✅ Fetches real market data (public API, no auth needed)
- ✅ Calculates real technical indicators
- ✅ Gets real AI signals from Claude
- ❌ Doesn't execute trades (shows what it would do)

This lets you test the entire bot logic without valid API credentials!

## Option 2: Fix Your API Keys (For Real Trading)

### Step-by-Step API Key Creation:

1. **Go to Bybit TESTNET** (not regular Bybit!)
   ```
   https://testnet.bybit.com
   ```

2. **Sign up or log in**
   - Use any email (no verification needed for testnet)
   - You'll get free testnet USDT automatically

3. **Create API Key:**
   - Click your profile (top right)
   - Go to "API" section
   - Click "Create New Key"

4. **IMPORTANT Settings:**
   - **Type**: "System-generated API Keys" (not sub-account)
   - **Permissions**: Check these boxes:
     - ✅ Read/Write
     - ✅ Contract (or "Derivatives")
     - ✅ Wallet (optional)
   - **IP Restriction**: Leave empty or add your IP
   - **Read-only mode**: UNCHECK this!

5. **Save the keys:**
   - API Key: Usually starts with letters/numbers, 20-30 chars
   - Secret Key: Longer, 30-40+ chars
   - **Copy them immediately!** Secret shown only once

6. **Verify:**
   - Keys should be LONGER than what you have now
   - API Key: 18 chars → Should be 20-30+ chars
   - Secret: 36 chars → Should be similar, but make sure it's complete

### Common Mistakes:

❌ Using mainnet keys on testnet (or vice versa)
❌ Not enabling "Contract/Derivatives" permission
❌ Enabling "Read-only" mode
❌ Copying keys with extra spaces or quotes
❌ Not copying the complete key

## Quick Test:

After getting new keys, run:
```bash
python3 test_connection.py
```

It should show:
```
✓ SUCCESS with Linear Testnet
  USDT Balance: 10000.0
```

Then you can run the real bot!

---

**Want me to create the demo mode now?** It will let you test everything except actual trade execution.
