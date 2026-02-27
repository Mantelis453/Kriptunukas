# 🚀 VPS Quick Start - 5 Minutes to Deploy!

This guide gets your trading bot running on a VPS in 5 minutes.

---

## 📋 Prerequisites

1. **VPS Server** with Ubuntu 20.04+ (Minimum: 1GB RAM, 1 CPU)
   - Recommended providers: DigitalOcean ($6/mo), Vultr ($6/mo), Linode ($5/mo)
2. **API Keys** ready:
   - Gemini AI (free): https://makersuite.google.com/app/apikey
   - Binance Testnet: https://testnet.binancefuture.com/
   - Telegram Bot (optional): @BotFather

---

## ⚡ Quick Deploy (3 Steps)

### Step 1: Setup VPS

SSH into your VPS and install Docker:

```bash
# Connect to VPS
ssh root@YOUR_VPS_IP

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Upload Bot Code

**Option A: Using Git (Recommended)**
```bash
cd ~
git clone YOUR_REPO_URL crypto-bot
cd crypto-bot
```

**Option B: Using SCP (from your local machine)**
```bash
# From your local machine
scp -r crypto-bot root@YOUR_VPS_IP:~/
```

**Option C: Manual Upload**
Use FileZilla or WinSCP to upload the `crypto-bot` folder.

### Step 3: Configure and Deploy

```bash
cd ~/crypto-bot

# Copy example config
cp config.yaml.example config.yaml

# Edit config with your API keys
nano config.yaml

# Update these lines:
# - Line 6: api_key: "YOUR_BINANCE_KEY"
# - Line 7: api_secret: "YOUR_BINANCE_SECRET"
# - Line 20: gemini_api_key: "YOUR_GEMINI_KEY"
# - Line 36: bot_token: "YOUR_TELEGRAM_TOKEN"
# - Line 37: chat_id: "YOUR_CHAT_ID"

# Save: Ctrl+X, then Y, then Enter

# Deploy! (One command)
./deploy.sh
```

**That's it! Your bot is running! 🎉**

---

## 📊 Monitor Your Bot

### View Live Logs
```bash
docker-compose logs -f
```
Press `Ctrl+C` to exit (bot keeps running).

### Check Bot Status
```bash
docker-compose ps
```

### View Resource Usage
```bash
docker stats crypto-trading-bot
```

### View Recent Signals
```bash
docker exec -it crypto-trading-bot sqlite3 bot.db "SELECT symbol, action, confidence, created_at FROM signals ORDER BY created_at DESC LIMIT 10;"
```

---

## 🛠️ Manage Your Bot

### Stop Bot
```bash
docker-compose stop
```

### Start Bot
```bash
docker-compose start
```

### Restart Bot
```bash
docker-compose restart
```

### Update Bot
```bash
# Pull latest code (if using git)
git pull

# Run update script
./update.sh
```

### Backup Database
```bash
./backup.sh
```

### View All Commands
```bash
# Stop and remove container
docker-compose down

# Rebuild from scratch
docker-compose up -d --build

# Check logs (last 50 lines)
docker-compose logs --tail=50

# Access container shell
docker exec -it crypto-trading-bot /bin/bash
```

---

## 📱 Verify Telegram Notifications

After deployment, you should receive a notification on Telegram. If not:

```bash
# Check Telegram config
docker exec -it crypto-trading-bot python3 test_telegram.py
```

---

## 🔒 Security Tips

### 1. Create Non-Root User
```bash
adduser trader
usermod -aG docker trader
usermod -aG sudo trader
su - trader
```

### 2. Setup Firewall
```bash
ufw allow 22/tcp
ufw enable
```

### 3. Use SSH Keys (No Password Login)
```bash
# On your local machine
ssh-copy-id trader@YOUR_VPS_IP

# On VPS, disable password auth
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

---

## 🐛 Troubleshooting

### Bot Not Starting?
```bash
# Check logs for errors
docker-compose logs

# Verify config syntax
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Rebuild from scratch
docker-compose down
docker-compose up -d --build
```

### Can't Connect to Exchange?
```bash
# Test from container
docker exec -it crypto-trading-bot python3 test_connection.py
```

### Gemini API Not Working?
```bash
# Check if key is configured
grep gemini_api_key config.yaml

# Should not show: YOUR_GEMINI_API_KEY
```

### High Memory Usage?
```bash
# Edit config to reduce frequency
nano config.yaml
# Change: analysis_interval_minutes: 120  # Every 2 hours

# Restart bot
docker-compose restart
```

---

## 📈 What Happens After Deployment?

1. **Initial Analysis**: Bot analyzes all symbols immediately
2. **Scheduled Analysis**: Every hour (configurable)
3. **Position Monitoring**: Every 5 minutes (configurable)
4. **Daily Report**: Sent at 23:55 UTC (configurable)
5. **Telegram Alerts**: Real-time trade signals and errors

---

## 💰 Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| **VPS** | $5-6/mo | DigitalOcean, Vultr, Linode |
| **Gemini API** | $0 | Free tier (plenty for this bot) |
| **Binance Testnet** | $0 | Paper trading (no real money) |
| **Telegram** | $0 | Free |
| **Total** | **$5-6/mo** | For 24/7 automated trading! |

---

## ✅ Deployment Checklist

- [ ] VPS created and accessible via SSH
- [ ] Docker and Docker Compose installed
- [ ] Bot code uploaded to VPS
- [ ] `config.yaml` created from `config.yaml.example`
- [ ] Gemini API key added to config
- [ ] Binance API keys added to config
- [ ] Telegram bot token and chat ID added
- [ ] `./deploy.sh` executed successfully
- [ ] Bot running: `docker-compose ps`
- [ ] Logs showing analysis: `docker-compose logs`
- [ ] Telegram notifications received
- [ ] Database being created: `ls -lh bot.db`

---

## 🎯 Next Steps

1. **Monitor for 24 hours**: Check logs, Telegram notifications
2. **Review signals**: Check if AI is analyzing correctly
3. **Adjust config**: Tune risk parameters, analysis frequency
4. **Setup backups**: Run `./backup.sh` daily (add to cron)
5. **Track performance**: Review database for trade history

---

## 📚 More Documentation

- **Full VPS Guide**: See `VPS_DEPLOYMENT.md` for detailed info
- **Gemini Setup**: See `GEMINI_SETUP.md` for API key setup
- **Bot Controls**: See `BOT_CONTROLS.md` for management commands
- **Binance Setup**: See `BINANCE_TESTNET_SETUP.md` for testnet keys
- **Telegram Setup**: See `TELEGRAM_GUIDE.md` for bot creation

---

## 🆘 Need Help?

1. **Check logs**: `docker-compose logs -f`
2. **Check bot.log**: `tail -50 bot.log`
3. **Test connections**: `python3 test_connection.py`
4. **Test Telegram**: `python3 test_telegram.py`
5. **Review docs**: Check the guides above

---

**Your bot is now trading 24/7 on autopilot! 🚀**

Check Telegram for updates and monitor logs regularly.
