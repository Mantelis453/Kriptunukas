# 🚀 VPS Deployment Guide - Docker Container

Complete guide to deploy the crypto trading bot on a VPS using Docker.

## 📋 Prerequisites

### What You Need:
1. **VPS Server** (Ubuntu 20.04+ recommended)
   - Minimum: 1 CPU, 512MB RAM, 10GB disk
   - Recommended: 1 CPU, 1GB RAM, 20GB disk
   - Providers: DigitalOcean, Linode, Vultr, AWS, Google Cloud

2. **API Keys:**
   - Binance Testnet API key (get at: https://testnet.binancefuture.com/)
   - Gemini AI API key (free at: https://makersuite.google.com/app/apikey)
   - Telegram Bot token (optional, from @BotFather)

3. **Local Tools:**
   - SSH client
   - Git (to clone/upload code)

---

## 🖥️ Step 1: Set Up Your VPS

### Connect to VPS:
```bash
ssh root@your_vps_ip
```

### Update System:
```bash
apt update && apt upgrade -y
```

### Install Docker:
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### Create Non-Root User (Recommended):
```bash
adduser trader
usermod -aG docker trader
usermod -aG sudo trader
su - trader
```

---

## 📦 Step 2: Upload Bot Code to VPS

### Option A: Using Git (Recommended)
```bash
# On VPS
cd ~
git clone <your-repo-url> crypto-bot
cd crypto-bot
```

### Option B: Using SCP (from your local machine)
```bash
# From your local machine
cd ~/Documents/tradingbot
scp -r crypto-bot trader@your_vps_ip:~/
```

### Option C: Manual Upload
Use FileZilla or similar SFTP client to upload the `crypto-bot` folder.

---

## ⚙️ Step 3: Configure the Bot

### Edit config.yaml:
```bash
cd ~/crypto-bot
nano config.yaml
```

Update these values:
```yaml
exchange:
  name: binance
  testnet: true
  api_key: "YOUR_BINANCE_TESTNET_API_KEY"
  api_secret: "YOUR_BINANCE_TESTNET_SECRET"

ai:
  method: gemini
  model: gemini-1.5-flash
  gemini_api_key: "YOUR_GEMINI_API_KEY"

telegram:
  bot_token: "YOUR_TELEGRAM_BOT_TOKEN"
  chat_id: "YOUR_TELEGRAM_CHAT_ID"
  enabled: true
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## 🐳 Step 4: Build and Run Docker Container

### Build the Docker Image:
```bash
docker-compose build
```

This will:
- Download Python 3.11
- Install all dependencies
- Create optimized container

### Start the Bot:
```bash
docker-compose up -d
```

The `-d` flag runs it in detached mode (background).

### Verify It's Running:
```bash
docker-compose ps
```

You should see:
```
NAME                  STATUS
crypto-trading-bot    Up X seconds
```

---

## 📊 Step 5: Monitor the Bot

### View Live Logs:
```bash
docker-compose logs -f
```

Press `Ctrl+C` to exit log view (bot keeps running).

### View Last 50 Log Lines:
```bash
docker-compose logs --tail=50
```

### Check Container Status:
```bash
docker ps
```

### Check Resource Usage:
```bash
docker stats crypto-trading-bot
```

---

## 🛠️ Management Commands

### Stop the Bot:
```bash
docker-compose stop
```

### Start the Bot:
```bash
docker-compose start
```

### Restart the Bot:
```bash
docker-compose restart
```

### Stop and Remove Container:
```bash
docker-compose down
```

### View Database:
```bash
docker exec -it crypto-trading-bot sqlite3 bot.db "SELECT * FROM signals ORDER BY created_at DESC LIMIT 5;"
```

### Access Container Shell:
```bash
docker exec -it crypto-trading-bot /bin/bash
```

---

## 🔄 Updating the Bot

### Method 1: Pull New Code
```bash
cd ~/crypto-bot
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Method 2: Upload New Files
```bash
# Upload files via SCP or SFTP
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📁 Data Persistence

Bot data is persisted in these locations:

| File | Location | Purpose |
|------|----------|---------|
| `bot.db` | `./bot.db` | Trading history, signals |
| `bot.log` | `./bot.log` | Application logs |
| `config.yaml` | `./config.yaml` | Configuration |

**Backup Important Data:**
```bash
# On VPS
cd ~/crypto-bot
cp bot.db bot_backup_$(date +%Y%m%d).db
cp config.yaml config_backup.yaml
```

---

## 🔒 Security Best Practices

### 1. Use Firewall:
```bash
# Allow SSH
ufw allow 22/tcp

# Allow only necessary ports
ufw enable
```

### 2. Set Up SSH Keys (No Password Login):
```bash
# On your local machine
ssh-copy-id trader@your_vps_ip

# On VPS, disable password auth
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

### 3. Regular Updates:
```bash
# Weekly
apt update && apt upgrade -y
docker system prune -f
```

### 4. Monitor Logs:
```bash
# Check for errors daily
docker-compose logs | grep ERROR
```

---

## 🚨 Troubleshooting

### Bot Not Starting:
```bash
# Check logs
docker-compose logs

# Check config syntax
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Rebuild from scratch
docker-compose down
docker system prune -a -f
docker-compose up --build -d
```

### High Memory Usage:
```bash
# Check resource limits in docker-compose.yml
# Reduce analysis frequency in config.yaml
nano config.yaml
# Change: analysis_interval_minutes: 120  # Every 2 hours
```

### Can't Connect to Exchange:
```bash
# Test from container
docker exec -it crypto-trading-bot python3 test_connection.py
```

### Database Locked:
```bash
# Stop bot, backup, restart
docker-compose stop
cp bot.db bot_backup.db
docker-compose start
```

---

## 📈 Auto-Start on Boot

Docker Compose with `restart: unless-stopped` will automatically start the bot on VPS reboot.

### Verify:
```bash
# Reboot VPS
sudo reboot

# After reboot, SSH back in and check
docker ps
```

Bot should be running automatically!

---

## 💰 Cost Estimates

### VPS Providers (Monthly):

| Provider | Plan | Price | Specs |
|----------|------|-------|-------|
| **DigitalOcean** | Basic Droplet | $6/mo | 1 CPU, 1GB RAM, 25GB SSD |
| **Vultr** | Cloud Compute | $6/mo | 1 CPU, 1GB RAM, 25GB SSD |
| **Linode** | Nanode | $5/mo | 1 CPU, 1GB RAM, 25GB SSD |
| **Hetzner** | CX11 | €4.15/mo | 1 CPU, 2GB RAM, 20GB SSD |

### Free Tier Options:
- **Google Cloud**: $300 credit (3 months)
- **AWS**: Free t2.micro (1 year)
- **Oracle Cloud**: Always free tier (2 CPUs, 1GB RAM)

---

## 📞 Quick Reference Commands

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop bot
docker-compose stop

# Restart bot
docker-compose restart

# Update bot
git pull && docker-compose up -d --build

# Backup database
cp bot.db bot_backup_$(date +%Y%m%d).db

# Check status
docker ps

# View recent signals
docker exec -it crypto-trading-bot sqlite3 bot.db "SELECT symbol, action, confidence FROM signals ORDER BY created_at DESC LIMIT 10;"
```

---

## 🎯 Next Steps After Deployment

1. **Monitor First 24 Hours**
   - Check logs regularly
   - Verify Telegram notifications
   - Ensure AI analysis is working

2. **Set Up Monitoring** (Optional)
   - Install monitoring tools (Netdata, Grafana)
   - Set up uptime monitoring (UptimeRobot)

3. **Create Backup Script**
   ```bash
   # Create backup script
   nano ~/backup.sh
   ```

   Add:
   ```bash
   #!/bin/bash
   cd ~/crypto-bot
   tar -czf ~/backups/bot_$(date +%Y%m%d).tar.gz bot.db config.yaml
   # Keep only last 7 backups
   ls -t ~/backups/bot_*.tar.gz | tail -n +8 | xargs rm -f
   ```

   Make executable and schedule:
   ```bash
   chmod +x ~/backup.sh
   crontab -e
   # Add: 0 2 * * * ~/backup.sh  # Daily at 2 AM
   ```

---

## ✅ Deployment Checklist

- [ ] VPS set up with Docker installed
- [ ] Bot code uploaded to VPS
- [ ] `config.yaml` updated with API keys
- [ ] Gemini API key configured
- [ ] Telegram bot configured
- [ ] Docker container built successfully
- [ ] Bot running in background
- [ ] Logs showing successful analysis
- [ ] Telegram receiving notifications
- [ ] Database being created/updated
- [ ] Auto-restart on reboot verified
- [ ] Backup strategy in place

---

**Your bot is now running 24/7 on a VPS!** 🎉

Check your Telegram for updates and monitor logs daily.

**Support:** Check `README.md` or review logs for troubleshooting.
