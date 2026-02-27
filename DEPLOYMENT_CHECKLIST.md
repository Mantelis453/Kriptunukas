# ✅ VPS Deployment Checklist

Use this checklist to ensure a smooth deployment to your VPS.

---

## 📦 Pre-Deployment (Local Machine)

### 1. Project Files
- [ ] All project files are up to date
- [ ] `config.yaml.example` exists
- [ ] `.gitignore` configured properly
- [ ] `Dockerfile` present
- [ ] `docker-compose.yml` present
- [ ] `.dockerignore` present
- [ ] Deployment scripts present (`deploy.sh`, `update.sh`, `backup.sh`)
- [ ] All helper scripts are executable (`chmod +x *.sh`)

### 2. API Keys Ready
- [ ] **Gemini API Key** obtained from https://makersuite.google.com/app/apikey
- [ ] **Binance Testnet API Key** from https://testnet.binancefuture.com/
- [ ] **Binance Testnet Secret** from https://testnet.binancefuture.com/
- [ ] **Telegram Bot Token** from @BotFather (optional)
- [ ] **Telegram Chat ID** from @userinfobot (optional)

### 3. Local Testing (Optional but Recommended)
- [ ] Tested locally with `python3 main.py --demo --once`
- [ ] Verified Gemini API connection works
- [ ] Verified Binance testnet connection works
- [ ] Verified Telegram notifications work (if enabled)
- [ ] No errors in logs

---

## 🖥️ VPS Setup

### 4. VPS Provider
- [ ] VPS created (minimum 1GB RAM, 1 CPU, 20GB disk)
- [ ] Ubuntu 20.04+ installed
- [ ] Root or sudo access available
- [ ] Public IP address noted
- [ ] SSH access working

### 5. Initial VPS Configuration
- [ ] Connected via SSH: `ssh root@YOUR_VPS_IP`
- [ ] System updated: `apt update && apt upgrade -y`
- [ ] Docker installed: `curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh`
- [ ] Docker Compose installed: `apt install docker-compose -y`
- [ ] Docker version verified: `docker --version`
- [ ] Docker Compose version verified: `docker-compose --version`

### 6. Security (Recommended)
- [ ] Non-root user created: `adduser trader`
- [ ] User added to docker group: `usermod -aG docker trader`
- [ ] User added to sudo group: `usermod -aG sudo trader`
- [ ] SSH keys configured (no password login)
- [ ] Firewall configured: `ufw allow 22/tcp && ufw enable`
- [ ] Root login disabled in SSH config

---

## 📤 Code Upload

### 7. Upload Method Selected

**Option A: Git (Recommended)**
- [ ] Repository pushed to GitHub/GitLab
- [ ] Repository cloned on VPS: `git clone REPO_URL crypto-bot`
- [ ] Changed to project directory: `cd crypto-bot`

**Option B: SCP**
- [ ] Code uploaded via SCP: `scp -r crypto-bot user@VPS_IP:~/`
- [ ] Changed to project directory: `cd ~/crypto-bot`

**Option C: Manual (SFTP)**
- [ ] Code uploaded via FileZilla/WinSCP
- [ ] Changed to project directory: `cd ~/crypto-bot`

---

## ⚙️ Configuration

### 8. Bot Configuration
- [ ] Config file created: `cp config.yaml.example config.yaml`
- [ ] Config file opened: `nano config.yaml`
- [ ] **Exchange section**:
  - [ ] `api_key` updated with Binance testnet key
  - [ ] `api_secret` updated with Binance testnet secret
  - [ ] `testnet: true` confirmed
- [ ] **AI section**:
  - [ ] `gemini_api_key` updated (NOT "YOUR_GEMINI_API_KEY")
  - [ ] Model set to `gemini-1.5-flash` (recommended)
- [ ] **Telegram section** (if enabled):
  - [ ] `bot_token` updated
  - [ ] `chat_id` updated
  - [ ] `enabled: true` set
- [ ] Config file saved (Ctrl+X, Y, Enter)
- [ ] Config validated: `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`

### 9. Environment Variables (Optional)
- [ ] `.env` file created if needed
- [ ] Environment variables configured
- [ ] `.env` added to `.gitignore`

---

## 🐳 Docker Deployment

### 10. Build and Deploy
- [ ] Deployment script made executable: `chmod +x deploy.sh`
- [ ] Bot deployed: `./deploy.sh`
- [ ] Build completed without errors
- [ ] Container started successfully
- [ ] Container running: `docker-compose ps` shows "Up"

### 11. Verify Deployment
- [ ] Container status checked: `docker ps`
- [ ] Container name is `crypto-trading-bot`
- [ ] Restart policy is `unless-stopped`
- [ ] Logs accessible: `docker-compose logs`
- [ ] No critical errors in logs

---

## 🧪 Testing

### 12. Functional Testing
- [ ] Logs show: "Bot is now running"
- [ ] Logs show: "Running initial analysis"
- [ ] AI analysis completing (check for "AI Signal for...")
- [ ] Database file created: `ls -lh bot.db`
- [ ] Log file created: `ls -lh bot.log`
- [ ] Exchange connection successful
- [ ] Gemini API responding (no API key errors)

### 13. Telegram Testing (if enabled)
- [ ] Telegram notifications received
- [ ] Test message sent: `docker exec -it crypto-trading-bot python3 test_telegram.py`
- [ ] Daily report time configured correctly

### 14. Database Testing
- [ ] Database accessible: `sqlite3 bot.db ".tables"`
- [ ] Tables created: candles, signals, trades, portfolio_snapshots, ai_logs
- [ ] Signals being recorded: `docker exec -it crypto-trading-bot sqlite3 bot.db "SELECT COUNT(*) FROM signals;"`

---

## 📊 Monitoring Setup

### 15. Monitoring Tools
- [ ] Log monitoring configured
- [ ] Know how to view logs: `docker-compose logs -f`
- [ ] Know how to view last 50 lines: `docker-compose logs --tail=50`
- [ ] Know how to filter errors: `docker-compose logs | grep ERROR`
- [ ] Resource monitoring: `docker stats crypto-trading-bot`

### 16. Auto-Restart Verification
- [ ] Container restart policy verified: `docker inspect crypto-trading-bot | grep RestartPolicy`
- [ ] Test auto-restart: `docker-compose restart`
- [ ] Container comes back up automatically
- [ ] Bot resumes operation after restart

---

## 💾 Backup Setup

### 17. Backup Configuration
- [ ] Backup script made executable: `chmod +x backup.sh`
- [ ] Backup directory created: `mkdir -p ~/bot-backups`
- [ ] Manual backup tested: `./backup.sh`
- [ ] Backup file created in `~/bot-backups/`
- [ ] Backup contains: bot.db, config.yaml, bot.log

### 18. Automated Backups (Optional)
- [ ] Cron job created for daily backups
- [ ] Cron schedule set: `0 2 * * * ~/crypto-bot/backup.sh`
- [ ] Cron job verified: `crontab -l`

---

## 🔄 Update Procedure

### 19. Update Testing
- [ ] Update script made executable: `chmod +x update.sh`
- [ ] Update procedure documented
- [ ] Know how to pull new code: `git pull` (if using Git)
- [ ] Know how to update: `./update.sh`

---

## 📈 Performance Monitoring

### 20. Performance Baselines
- [ ] Initial CPU usage noted: ~5-10% during analysis
- [ ] Initial RAM usage noted: ~200-300MB
- [ ] Disk usage noted: ~1MB/day growth
- [ ] Analysis timing noted: ~2-3s per symbol
- [ ] Position monitoring frequency: every 5 minutes

---

## 🚨 Troubleshooting Prepared

### 21. Common Issues Documented
- [ ] Know where to find logs: `bot.log` or `docker-compose logs`
- [ ] Know how to restart: `docker-compose restart`
- [ ] Know how to rebuild: `docker-compose down && docker-compose up -d --build`
- [ ] Know how to access container: `docker exec -it crypto-trading-bot /bin/bash`
- [ ] Have troubleshooting guides bookmarked

### 22. Emergency Contacts
- [ ] VPS provider support contact saved
- [ ] Documentation URLs saved
- [ ] API provider documentation bookmarked

---

## 📱 Notifications Configured

### 23. Alert Channels
- [ ] Telegram working (if enabled)
- [ ] Error notifications configured
- [ ] Daily reports scheduled (23:55 UTC)
- [ ] Trade signal alerts working

---

## 🎯 Post-Deployment

### 24. First 24 Hours
- [ ] Monitor logs frequently
- [ ] Verify hourly analysis is running
- [ ] Check position monitoring (every 5 min)
- [ ] Verify daily report (next day at 23:55)
- [ ] Review any errors or warnings
- [ ] Check database growth: `ls -lh bot.db`

### 25. First Week
- [ ] Review AI signals in database
- [ ] Analyze bot performance
- [ ] Adjust risk parameters if needed
- [ ] Fine-tune analysis frequency
- [ ] Review resource usage
- [ ] Ensure backups are working

### 26. Ongoing Maintenance
- [ ] Weekly log review scheduled
- [ ] Monthly VPS updates: `apt update && apt upgrade -y`
- [ ] Database backup verification
- [ ] Performance monitoring
- [ ] Configuration tuning as needed

---

## 📚 Documentation Review

### 27. Read All Guides
- [ ] `README.md` - Main documentation
- [ ] `VPS_QUICKSTART.md` - Quick deployment guide
- [ ] `VPS_DEPLOYMENT.md` - Detailed deployment guide
- [ ] `GEMINI_SETUP.md` - Gemini API setup
- [ ] `BINANCE_TESTNET_SETUP.md` - Exchange setup
- [ ] `TELEGRAM_GUIDE.md` - Telegram bot setup
- [ ] `BOT_CONTROLS.md` - Management commands
- [ ] `PROJECT_SUMMARY.md` - Project overview

---

## ✅ Final Verification

### 28. All Systems Go
- [ ] Bot running: `docker-compose ps`
- [ ] Logs clean: `docker-compose logs --tail=50`
- [ ] Database growing: `ls -lh bot.db`
- [ ] AI analyzing: Check logs for "AI Signal"
- [ ] Telegram working: Messages received
- [ ] Backups configured: `./backup.sh` works
- [ ] Update procedure tested: `./update.sh` works
- [ ] Documentation bookmarked
- [ ] Emergency procedures documented

---

## 🎉 Deployment Complete!

**Congratulations!** Your crypto trading bot is now running 24/7 on your VPS!

### Quick Reference Commands:
```bash
# View logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart bot
docker-compose restart

# Stop bot
docker-compose stop

# Update bot
./update.sh

# Backup data
./backup.sh

# View recent signals
docker exec -it crypto-trading-bot sqlite3 bot.db "SELECT * FROM signals ORDER BY created_at DESC LIMIT 5;"
```

---

**Happy Trading! 🚀**
