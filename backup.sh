#!/bin/bash
# Backup Script for Crypto Trading Bot
# Usage: ./backup.sh

set -e

BACKUP_DIR="$HOME/bot-backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="bot_backup_$DATE.tar.gz"

echo "╔════════════════════════════════════════════════╗"
echo "║     Crypto Trading Bot - Backup Script        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup..."

# Backup database and config
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    bot.db \
    config.yaml \
    bot.log 2>/dev/null || true

echo "✓ Backup created: $BACKUP_DIR/$BACKUP_FILE"
echo ""

# Keep only last 7 backups
echo "🧹 Cleaning old backups (keeping last 7)..."
cd "$BACKUP_DIR"
ls -t bot_backup_*.tar.gz | tail -n +8 | xargs rm -f 2>/dev/null || true

echo "✓ Backup complete!"
echo ""
echo "Backups location: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
