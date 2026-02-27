# 🤖 Gemini AI Setup Guide

## Why Gemini?

✅ **Free API** - No credit card required
✅ **Fast** - Quick response times
✅ **Reliable** - Stable API from Google
✅ **Easy to use** - Simple integration
✅ **No CLI needed** - Works on any VPS/Docker
✅ **High rate limits** - 60 requests per minute (free tier)

---

## 🔑 Get Your Free Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

(Or search "Google AI Studio API key")

### Step 2: Sign In
- Click "Sign in with Google"
- Use any Google account (Gmail)

### Step 3: Create API Key
1. Click **"Create API Key"**
2. Select **"Create API key in new project"** (or use existing project)
3. Your API key will be generated immediately

### Step 4: Copy Your API Key
```
Example: AIzaSyABC123def456GHI789jkl012MNO345pqr
```

**Important:** Copy it now! You can always view it again later.

---

## ⚙️ Configure the Bot

### Option 1: Update config.yaml (Recommended)

Edit `config.yaml`:
```yaml
ai:
  method: gemini
  model: gemini-1.5-flash  # Fast and free!
  gemini_api_key: "AIzaSyABC123def456GHI789jkl012MNO345pqr"  # Your key here
  min_confidence: 70
  prompt_version: v1
```

### Option 2: Use Environment Variable

```bash
export GEMINI_API_KEY="AIzaSyABC123def456GHI789jkl012MNO345pqr"
```

---

## 📊 Available Models

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| **gemini-1.5-flash** | ⚡ Fastest | Good | Free | **Trading bot (recommended)** |
| **gemini-1.5-pro** | Medium | Excellent | Free | Complex analysis |
| **gemini-pro** | Fast | Very Good | Free | General use |

**Recommendation:** Use `gemini-1.5-flash` for trading - it's fast and free!

---

## 🧪 Test Your API Key

### Install Gemini Package:
```bash
pip3 install google-generativeai
```

### Quick Test:
```bash
python3 << 'EOF'
import google.generativeai as genai

# Replace with your API key
genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Say hello!")
print(response.text)
EOF
```

You should see: "Hello!" or similar response.

---

## 🚀 Run the Bot with Gemini

### Install Dependencies:
```bash
cd crypto-bot
pip3 install -r requirements.txt
```

### Test Once:
```bash
python3 main.py --demo --once
```

You should see:
```
Calling Gemini API (gemini-1.5-flash) for BTCUSDT analysis...
AI Signal for BTCUSDT: HOLD (confidence: 65%)
```

### Run Continuously:
```bash
python3 main.py --demo
```

---

## 💵 Pricing & Limits (Free Tier)

### Free Tier Limits:
- **Rate Limit:** 60 requests per minute
- **Daily Limit:** Generous (thousands of requests)
- **Cost:** $0 (completely free!)

### Our Bot Usage:
- **2 symbols** × **1 request/hour** = **48 requests/day**
- **Well within free limits!** ✅

### If You Need More:
- Paid tier available (very cheap)
- Or reduce analysis frequency in `config.yaml`:
  ```yaml
  schedule:
    analysis_interval_minutes: 120  # Every 2 hours instead of 1
  ```

---

## 🔒 Security Tips

### DO:
✅ Keep API key private
✅ Use environment variables
✅ Add to `.gitignore`
✅ Regenerate if leaked

### DON'T:
❌ Commit API key to GitHub
❌ Share in public channels
❌ Use same key for multiple projects

### Secure Storage:
```bash
# Add to .gitignore
echo "config.yaml" >> .gitignore
echo ".env" >> .gitignore

# Or use environment variable
export GEMINI_API_KEY="your_key_here"
```

---

## 🆚 Gemini vs Claude CLI

| Feature | Gemini API | Claude CLI |
|---------|------------|------------|
| **Setup** | ✅ Easy (API key) | ❌ Need Claude Code installed |
| **VPS/Docker** | ✅ Works everywhere | ❌ Complex setup |
| **Speed** | ⚡ Fast | Medium |
| **Cost** | 🆓 Free | Requires Claude subscription |
| **Reliability** | ✅ Very stable | Depends on CLI availability |
| **Rate Limits** | 60/min | Varies |

**Winner for VPS:** Gemini API 🏆

---

## 🐛 Troubleshooting

### Error: "API key not valid"
- Double-check you copied the full key
- Regenerate a new key at: https://makersuite.google.com/app/apikey
- Check no extra spaces in config.yaml

### Error: "google-generativeai not installed"
```bash
pip3 install google-generativeai
```

### Error: "Rate limit exceeded"
- Wait 1 minute
- Reduce analysis frequency in config.yaml
- Check you're not running multiple bots with same key

### Error: "Invalid JSON response"
- This is normal occasionally
- Bot will default to HOLD
- Check next analysis cycle

### No analysis happening:
```bash
# Check logs
tail -f bot.log

# Verify API key is configured
cat config.yaml | grep gemini_api_key
```

---

## 📈 Performance Comparison

### Response Times:
- **Gemini 1.5 Flash:** ~1-2 seconds ⚡
- **Gemini 1.5 Pro:** ~3-5 seconds
- **Claude CLI:** ~5-10 seconds

### Accuracy:
Both Gemini and Claude provide excellent trading analysis. Gemini 1.5 Flash is optimized for speed while maintaining quality.

---

## 🔄 Switching from Claude to Gemini

Already using Claude CLI? Easy switch:

1. **Get Gemini API key** (2 minutes)
2. **Update config.yaml:**
   ```yaml
   ai:
     method: gemini  # Changed from claude_cli
     gemini_api_key: "YOUR_KEY"
   ```
3. **Install package:**
   ```bash
   pip3 install google-generativeai
   ```
4. **Restart bot:**
   ```bash
   python3 main.py --demo
   ```

Done! ✅

---

## 📚 Additional Resources

- **API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://makersuite.google.com/app/apikey
- **Pricing:** https://ai.google.dev/pricing
- **Models:** https://ai.google.dev/models/gemini

---

## ✅ Quick Checklist

- [ ] Created Google account
- [ ] Got Gemini API key from Google AI Studio
- [ ] Updated config.yaml with API key
- [ ] Installed google-generativeai package
- [ ] Tested with --demo --once
- [ ] Bot running and getting AI signals
- [ ] Telegram notifications working

---

**Ready to trade with Gemini AI!** 🚀

Your bot will now use Google's Gemini for fast, accurate trading analysis - completely free!
