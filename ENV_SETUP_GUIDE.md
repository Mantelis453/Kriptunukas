# 🔑 Environment Variables Setup Guide

## Why Use Environment Variables?

✅ **Easier for Docker** - No need to mount config.yaml
✅ **More Secure** - API keys not in config files
✅ **Simpler Updates** - Just edit .env file and restart
✅ **No Rebuild Needed** - Change keys without rebuilding container

---

## 🚀 Quick Setup (VPS)

### Step 1: Create .env File

On your VPS:
```bash
cd ~/Kriptunukas
cp .env.example .env
nano .env
```

### Step 2: Add Your API Keys

Update these lines in .env:
```bash
# Gemini AI (Get free at: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=AIzaSy...your-actual-key-here

# Binance Testnet (Get at: https://testnet.binancefuture.com/)
BINANCE_API_KEY=your-binance-key
BINANCE_API_SECRET=your-binance-secret

# Telegram (Optional - from @BotFather)
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=123456789
```

**Save:** `Ctrl+X`, `Y`, `Enter`

### Step 3: Restart Bot

```bash
docker-compose down
docker-compose up -d
docker-compose logs -f
```

**Done!** ✅

---

## 🔍 How It Works

Environment variables **override** config.yaml values:

**Priority (highest to lowest):**
1. Environment variables (.env file)
2. config.yaml file
3. Default values

---

## 📋 All Available Environment Variables

```bash
# Timezone
TZ=UTC

# Gemini AI
GEMINI_API_KEY=your_key

# Binance API
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret

# Telegram
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Logging (optional)
LOG_LEVEL=INFO
```

---

## ✅ Verify Environment Variables

Check if env vars are loaded:

```bash
# Check what env vars the container has
docker exec -it crypto-trading-bot env | grep -E "GEMINI|BINANCE|TELEGRAM"
```

Should show:
```
GEMINI_API_KEY=AIzaSy...
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=123456789
```

---

## 🔒 Security Best Practices

### DO:
✅ Keep .env file private (already in .gitignore)
✅ Use different API keys for different projects
✅ Rotate keys regularly
✅ Set proper file permissions: `chmod 600 .env`

### DON'T:
❌ Commit .env file to Git
❌ Share API keys in public channels
❌ Use production keys in testnet bot

---

## 🐛 Troubleshooting

### Bot not using environment variables?

**Check if .env file exists:**
```bash
ls -la .env
```

**Check if docker-compose is reading it:**
```bash
docker-compose config | grep -A 5 environment
```

**Restart container to load new values:**
```bash
docker-compose restart
```

### Still using config.yaml values?

Environment variables have `-` (dash) in docker-compose, which means "use env var if available, otherwise empty string".

Check the actual values:
```bash
docker exec -it crypto-trading-bot env | grep API
```

---

## 📝 Example .env File

```bash
# Working example
TZ=UTC
GEMINI_API_KEY=AIzaSyABC123def456GHI789jkl012MNO345pqr
BINANCE_API_KEY=2ua8lTZjqIKkSSmTB5CctQt9lOwvcV7P8nwHJ3jKefJTQvNil8pjZjejf5qEDWQo
BINANCE_API_SECRET=4F3OP3XiU6WdDmPOkAk0jzq0KPjwSc7pS3iLQyqJpy6BHHCa1BWiqRnQJuiAQaYo
TELEGRAM_BOT_TOKEN=8640047183:AAF6aG2L95UdK9aEGw6a50Z1_7J46hdOQhw
TELEGRAM_CHAT_ID=2053988717
```

---

## 🎯 Quick Commands

```bash
# Create .env from template
cp .env.example .env

# Edit .env
nano .env

# Restart to apply changes
docker-compose restart

# View logs
docker-compose logs -f

# Check environment variables
docker exec -it crypto-trading-bot env | grep -E "GEMINI|BINANCE"
```

---

## 🔄 Switching from config.yaml to .env

If you're currently using config.yaml:

1. Create .env file from template
2. Copy your API keys from config.yaml to .env
3. Restart container
4. Environment variables will override config.yaml
5. (Optional) Remove API keys from config.yaml for security

**Both can coexist!** Env vars take priority.

---

**Environment variables are the recommended way to configure the bot in Docker!** 🚀
