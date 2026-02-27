# 🚀 Deploy to Your VPS: 72.60.16.8

Quick deployment guide for your specific VPS.

---

## Step 1: Connect to VPS

```bash
ssh root@72.60.16.8
```

When prompted about the fingerprint, type `yes` to accept.

---

## Step 2: Install Docker

Once connected to your VPS, run:

```bash
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

---

## Step 3: Upload Bot Code

**From your local machine** (open a new terminal, don't close the SSH session):

```bash
cd ~/Documents/tradingbot
scp -r crypto-bot root@72.60.16.8:~/
```

---

## Step 4: Configure Bot

**Back on your VPS SSH session:**

```bash
cd ~/crypto-bot

# Create config from template
cp config.yaml.example config.yaml

# Edit config
nano config.yaml
```

**Update these values:**

```yaml
# Line 6-7: Binance API keys
api_key: "YOUR_BINANCE_TESTNET_KEY"
api_secret: "YOUR_BINANCE_TESTNET_SECRET"

# Line 20: Gemini API key
gemini_api_key: "YOUR_GEMINI_API_KEY"

# Line 36-37: Telegram (optional)
bot_token: "YOUR_TELEGRAM_TOKEN"
chat_id: "YOUR_CHAT_ID"
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

---

## Step 5: Deploy!

```bash
# Make scripts executable
chmod +x *.sh

# Deploy the bot
./deploy.sh
```

**That's it!** Your bot will now build and start running!

---

## Step 6: Verify Deployment

```bash
# Check if container is running
docker-compose ps

# View live logs
docker-compose logs -f
```

You should see:
- "Bot is now running"
- "Running initial analysis"
- AI signals for BTC and ETH

Press `Ctrl+C` to exit logs (bot keeps running).

---

## 📊 Manage Your Bot

### View Logs
```bash
docker-compose logs -f
```

### Check Status
```bash
docker-compose ps
```

### Restart Bot
```bash
docker-compose restart
```

### Stop Bot
```bash
docker-compose stop
```

### Update Bot
```bash
./update.sh
```

### Backup Database
```bash
./backup.sh
```

---

## 🔒 Security (Recommended)

After deployment, secure your VPS:

```bash
# Create non-root user
adduser trader
usermod -aG docker trader
usermod -aG sudo trader

# Setup firewall
ufw allow 22/tcp
ufw enable

# Switch to new user
su - trader
cd ~/crypto-bot
```

---

## 🆘 Troubleshooting

### Bot won't start?
```bash
docker-compose logs
```

### Can't connect to exchange?
```bash
docker exec -it crypto-trading-bot python3 test_connection.py
```

### Gemini API errors?
```bash
grep gemini_api_key config.yaml
# Should NOT show: YOUR_GEMINI_API_KEY
```

---

## ✅ What to Check

- [ ] Connected to VPS: `ssh root@72.60.16.8`
- [ ] Docker installed: `docker --version`
- [ ] Code uploaded to VPS
- [ ] config.yaml created with your API keys
- [ ] Bot deployed: `./deploy.sh`
- [ ] Container running: `docker-compose ps`
- [ ] Logs showing analysis: `docker-compose logs`
- [ ] Telegram notifications working (if configured)

---

**Your bot should now be running 24/7 on VPS 72.60.16.8! 🎉**

Check Telegram for notifications and monitor logs regularly.
