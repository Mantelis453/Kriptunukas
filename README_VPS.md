# 🐳 Docker VPS Deployment - Complete Guide

Your crypto trading bot is **ready for VPS deployment**! This guide covers everything you need to deploy and run your bot 24/7 on a cloud server.

---

## 🎯 What You Have

Your project now includes **complete Docker support** for easy VPS deployment:

### ✅ Docker Files
- **Dockerfile** - Multi-stage build for optimized container
- **docker-compose.yml** - One-command deployment with auto-restart
- **.dockerignore** - Optimized builds (excludes unnecessary files)
- **.env.example** - Environment variables template

### ✅ Helper Scripts
- **deploy.sh** - Automated deployment script
- **update.sh** - Easy bot updates
- **backup.sh** - Automated database backups
- **config.yaml.example** - Configuration template

### ✅ Documentation
- **VPS_QUICKSTART.md** - Deploy in 5 minutes
- **VPS_DEPLOYMENT.md** - Detailed deployment guide
- **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist
- **GEMINI_SETUP.md** - Get your free AI API key
- **BINANCE_TESTNET_SETUP.md** - Exchange API keys
- **TELEGRAM_GUIDE.md** - Notification setup

---

## 🚀 Quick Deploy (3 Commands)

```bash
# 1. Configure
cp config.yaml.example config.yaml
nano config.yaml  # Add your API keys

# 2. Deploy
./deploy.sh

# 3. Monitor
docker-compose logs -f
```

**Done! Bot is running 24/7! 🎉**

---

## 📋 What You Need

### 1. VPS Server
**Minimum Requirements:**
- 1 CPU core
- 1GB RAM (512MB minimum)
- 20GB disk space
- Ubuntu 20.04+ (or any Linux with Docker support)

**Recommended Providers:**
- **DigitalOcean** - $6/month (Basic Droplet)
- **Vultr** - $6/month (Cloud Compute)
- **Linode** - $5/month (Nanode)
- **Hetzner** - €4.15/month (CX11)

**Free Tier Options:**
- Google Cloud - $300 credit (3 months)
- AWS - Free t2.micro (1 year)
- Oracle Cloud - Always free tier

### 2. API Keys (All Free!)

| Service | Purpose | Get It Here | Required |
|---------|---------|-------------|----------|
| **Gemini AI** | Trading analysis | [Get Free Key](https://makersuite.google.com/app/apikey) | ✅ Yes |
| **Binance Testnet** | Paper trading | [Testnet](https://testnet.binancefuture.com/) | ✅ Yes |
| **Telegram Bot** | Notifications | [@BotFather](https://t.me/botfather) | ⚠️ Optional |

---

## 🎬 Deployment Steps

### Step 1: Setup Your VPS

```bash
# Connect to your VPS
ssh root@YOUR_VPS_IP

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Upload Bot Code

**Option A: Git (Recommended)**
```bash
# On VPS
cd ~
git clone YOUR_REPO_URL crypto-bot
cd crypto-bot
```

**Option B: SCP**
```bash
# From your local machine
scp -r crypto-bot root@YOUR_VPS_IP:~/
```

**Option C: Manual**
- Use FileZilla/WinSCP to upload the folder

### Step 3: Configure API Keys

```bash
# On VPS, in crypto-bot directory
cp config.yaml.example config.yaml
nano config.yaml
```

**Update these values:**
```yaml
exchange:
  api_key: "YOUR_BINANCE_TESTNET_KEY"
  api_secret: "YOUR_BINANCE_TESTNET_SECRET"

ai:
  gemini_api_key: "YOUR_GEMINI_API_KEY"

telegram:
  bot_token: "YOUR_TELEGRAM_TOKEN"
  chat_id: "YOUR_CHAT_ID"
```

Save with: `Ctrl+X`, then `Y`, then `Enter`

### Step 4: Deploy!

```bash
# Make scripts executable
chmod +x *.sh

# Deploy the bot
./deploy.sh
```

**That's it!** Your bot is now running 24/7! 🚀

---

## 📊 Managing Your Bot

### View Live Logs
```bash
docker-compose logs -f
```
Press `Ctrl+C` to exit (bot keeps running)

### Check Status
```bash
docker-compose ps
```

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
git pull  # if using git
./update.sh
```

### Backup Database
```bash
./backup.sh
```

### View Resource Usage
```bash
docker stats crypto-trading-bot
```

### Access Container Shell
```bash
docker exec -it crypto-trading-bot /bin/bash
```

---

## 🔍 Monitoring & Debugging

### Check Recent Signals
```bash
docker exec -it crypto-trading-bot sqlite3 bot.db \
  "SELECT symbol, action, confidence, created_at FROM signals ORDER BY created_at DESC LIMIT 10;"
```

### Check Trades
```bash
docker exec -it crypto-trading-bot sqlite3 bot.db \
  "SELECT * FROM trades ORDER BY created_at DESC LIMIT 5;"
```

### View Errors Only
```bash
docker-compose logs | grep ERROR
```

### Check Container Health
```bash
docker inspect crypto-trading-bot | grep -A 10 Health
```

---

## 🛠️ Troubleshooting

### Bot Won't Start
```bash
# Check logs for errors
docker-compose logs

# Rebuild container
docker-compose down
docker-compose up -d --build
```

### Gemini API Errors
```bash
# Verify API key is configured
grep gemini_api_key config.yaml

# Should NOT show: YOUR_GEMINI_API_KEY
```

### Exchange Connection Failed
```bash
# Test connection
docker exec -it crypto-trading-bot python3 test_connection.py
```

### High Memory Usage
```bash
# Edit config to reduce frequency
nano config.yaml
# Change: analysis_interval_minutes: 120  # Every 2 hours
docker-compose restart
```

### Database Locked
```bash
docker-compose stop
cp bot.db bot.db.backup
docker-compose start
```

---

## 🔒 Security Best Practices

### 1. Create Non-Root User
```bash
adduser trader
usermod -aG docker trader
usermod -aG sudo trader
su - trader
```

### 2. Setup SSH Keys (Disable Password Login)
```bash
# On local machine
ssh-copy-id trader@YOUR_VPS_IP

# On VPS
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### 3. Configure Firewall
```bash
ufw allow 22/tcp
ufw enable
```

### 4. Keep API Keys Secure
```bash
# Ensure config.yaml is in .gitignore
echo "config.yaml" >> .gitignore

# Set proper permissions
chmod 600 config.yaml
```

---

## 💾 Backup Strategy

### Manual Backup
```bash
./backup.sh
```

### Automated Daily Backups
```bash
# Add to crontab
crontab -e

# Add this line (runs at 2 AM daily):
0 2 * * * ~/crypto-bot/backup.sh
```

### Restore from Backup
```bash
cd ~/crypto-bot
docker-compose stop

# Extract backup
tar -xzf ~/bot-backups/bot_backup_YYYYMMDD_HHMMSS.tar.gz

docker-compose start
```

---

## 📈 Performance Expectations

### Resource Usage
- **CPU**: 5-10% during analysis, <1% idle
- **RAM**: 200-300MB
- **Disk**: ~1MB/day database growth
- **Network**: Minimal (API calls only)

### Response Times
- Market data fetch: ~0.5s
- Technical indicators: ~0.2s
- Gemini AI analysis: ~1-2s
- **Total per symbol**: ~2-3s ⚡

### Costs
- **VPS**: $5-6/month
- **Gemini API**: $0 (free tier)
- **Binance Testnet**: $0 (paper trading)
- **Total**: **$5-6/month for 24/7 trading!** 💰

---

## 🎯 What Happens After Deployment

### Immediate
1. Container builds and starts
2. Bot initializes modules
3. Connects to Binance testnet
4. Runs initial analysis on all symbols
5. Sends Telegram notification (if configured)

### Scheduled Operations
- **Analysis**: Every 60 minutes (configurable)
- **Position Monitoring**: Every 5 minutes (configurable)
- **Daily Report**: At 23:55 UTC (configurable)

### Data Storage
- **Database**: `bot.db` (SQLite)
- **Logs**: `bot.log` (rotated automatically)
- **Config**: `config.yaml` (read-only in container)

---

## 📚 Project Structure

```
crypto-bot/
├── 🐳 Docker Files
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── .env.example
│
├── 🛠️ Helper Scripts
│   ├── deploy.sh           # One-command deployment
│   ├── update.sh           # Easy updates
│   └── backup.sh           # Database backups
│
├── 📚 Documentation
│   ├── README.md
│   ├── README_VPS.md       # This file
│   ├── VPS_QUICKSTART.md
│   ├── VPS_DEPLOYMENT.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   ├── GEMINI_SETUP.md
│   ├── BINANCE_TESTNET_SETUP.md
│   └── TELEGRAM_GUIDE.md
│
├── 🤖 Application Code
│   ├── main.py
│   ├── config.yaml.example
│   ├── requirements.txt
│   ├── data/
│   ├── ai/
│   ├── trading/
│   ├── db/
│   ├── notifications/
│   └── utils/
│
└── 🧪 Test Scripts
    ├── test_connection.py
    └── test_telegram.py
```

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] VPS server with Docker installed
- [ ] Gemini API key obtained
- [ ] Binance testnet API keys obtained
- [ ] Telegram bot configured (optional)
- [ ] `config.yaml` created with your API keys
- [ ] All scripts executable (`chmod +x *.sh`)
- [ ] Read the deployment documentation

---

## 🎓 Learning Resources

### Documentation Files
1. **VPS_QUICKSTART.md** - Quick 5-minute deploy
2. **VPS_DEPLOYMENT.md** - Detailed step-by-step
3. **DEPLOYMENT_CHECKLIST.md** - Complete checklist
4. **GEMINI_SETUP.md** - Get AI API key
5. **BINANCE_TESTNET_SETUP.md** - Get exchange keys
6. **TELEGRAM_GUIDE.md** - Setup notifications

### External Resources
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Binance API Docs](https://binance-docs.github.io/apidocs/futures/en/)

---

## 🆘 Getting Help

### Diagnostic Commands
```bash
# View full logs
docker-compose logs

# Test exchange connection
docker exec -it crypto-trading-bot python3 test_connection.py

# Test Telegram
docker exec -it crypto-trading-bot python3 test_telegram.py

# Check database
docker exec -it crypto-trading-bot sqlite3 bot.db ".tables"

# View configuration
cat config.yaml
```

### Common Issues

**Bot not analyzing?**
- Check Gemini API key in config.yaml
- View logs: `docker-compose logs | grep ERROR`

**No Telegram notifications?**
- Verify bot token and chat ID
- Test: `docker exec -it crypto-trading-bot python3 test_telegram.py`

**Container keeps restarting?**
- Check logs: `docker-compose logs`
- Verify config syntax: `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`

---

## 🔄 Updates & Maintenance

### Regular Updates
```bash
# Weekly: Pull latest code
cd ~/crypto-bot
git pull
./update.sh

# Monthly: Update VPS system
sudo apt update && sudo apt upgrade -y
docker system prune -f
```

### Monitoring Schedule
- **Daily**: Check logs for errors
- **Weekly**: Review performance and signals
- **Monthly**: Analyze trading results, adjust parameters

---

## 🎉 Congratulations!

Your crypto trading bot is now **production-ready** for VPS deployment!

### What You've Accomplished:
✅ Complete Docker containerization
✅ Auto-restart on failure
✅ Data persistence (database, logs)
✅ Resource management (CPU/RAM limits)
✅ Automated deployment scripts
✅ Backup system
✅ Comprehensive documentation

### Next Steps:
1. **Deploy**: Follow VPS_QUICKSTART.md
2. **Monitor**: Check logs and Telegram
3. **Optimize**: Adjust config based on performance
4. **Scale**: Add more symbols or strategies

---

## 💬 Questions?

Check these guides:
- **Quick start**: VPS_QUICKSTART.md
- **Detailed deployment**: VPS_DEPLOYMENT.md
- **Step-by-step**: DEPLOYMENT_CHECKLIST.md
- **Troubleshooting**: Each guide has a troubleshooting section

---

**Ready to deploy?** 🚀

```bash
./deploy.sh
```

**Happy Trading!** 📈
