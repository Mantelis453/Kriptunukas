# 🔧 Docker Deployment Hotfix

## Issue Fixed

**Error:** `IsADirectoryError: [Errno 21] Is a directory: '/app/bot.log'`

**Cause:** Docker volume mounting created bot.log as a directory instead of a file

**Status:** ✅ FIXED

---

## What Was Changed

### 1. docker-compose.yml
**Before:**
```yaml
volumes:
  - ./bot.db:/app/bot.db
  - ./bot.log:/app/bot.log
```

**After:**
```yaml
volumes:
  - bot-data:/app/data  # Database and logs in named volume
```

### 2. config.yaml.example
**Before:**
```yaml
database:
  path: "./bot.db"
logging:
  file: "./bot.log"
```

**After:**
```yaml
database:
  path: "/app/data/bot.db"
logging:
  file: "/app/data/bot.log"
```

---

## How to Apply This Fix (On VPS)

If you already deployed and got the error, follow these steps:

### Step 1: Stop and Remove Old Container
```bash
cd ~/Kriptunukas
docker-compose down
```

### Step 2: Remove Old Volume Mounts
```bash
rm -rf bot.db bot.log  # Remove if they were created as directories
```

### Step 3: Pull Latest Changes
```bash
git pull origin main
```

### Step 4: Update Your config.yaml
```bash
nano config.yaml
```

Update these lines:
```yaml
database:
  path: "/app/data/bot.db"  # Changed from "./bot.db"

logging:
  file: "/app/data/bot.log"  # Changed from "./bot.log"
```

Save: `Ctrl+X`, `Y`, `Enter`

### Step 5: Redeploy
```bash
./deploy.sh
```

---

## Verify It's Working

```bash
# Check container is running
docker-compose ps

# View logs (should see no errors)
docker-compose logs -f
```

You should see:
- "Bot is now running"
- "Running initial analysis"
- No "IsADirectoryError"

---

## Where Are Files Now?

**Database and logs** are stored in Docker volume `kriptunukas_bot-data`:

### Access files:
```bash
# View logs
docker exec -it crypto-trading-bot cat /app/data/bot.log

# View database
docker exec -it crypto-trading-bot ls -lh /app/data/

# Backup database
docker cp crypto-trading-bot:/app/data/bot.db ./bot_backup.db
```

---

## Why This Fix?

Docker volume mounting works differently when:
- File doesn't exist on host → Docker creates it as **directory** (bad)
- Using named volume → Docker manages it properly (good)

Named volumes are better for:
- ✅ Cross-platform compatibility
- ✅ Automatic creation
- ✅ Proper permissions
- ✅ Data persistence

---

## Deprecation Warning (Non-Critical)

You may still see this warning:
```
FutureWarning: All support for the `google.generativeai` package has ended
```

**Impact:** None for now
**Action:** We'll update to `google-genai` in future version
**Current:** Bot works perfectly with current package

---

## Questions?

Check:
- `docker-compose logs` - View bot logs
- `docker-compose ps` - Check if running
- `VPS_QUICKSTART.md` - Deployment guide

---

**Fix applied: 2025-02-27**
