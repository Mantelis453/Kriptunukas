#!/bin/bash
# Update Script for Crypto Trading Bot
# Usage: ./update.sh

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║     Crypto Trading Bot - Update Script        ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

echo "🛑 Stopping bot..."
docker-compose stop

echo "📦 Rebuilding Docker image..."
docker-compose build

echo "🚀 Starting updated bot..."
docker-compose up -d

echo ""
echo "✓ Bot updated and restarted successfully!"
echo ""
echo "📊 View logs: docker-compose logs -f"
