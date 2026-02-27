#!/bin/bash
# VPS Deployment Script for Crypto Trading Bot
# Usage: ./deploy.sh

set -e  # Exit on error

echo "╔════════════════════════════════════════════════╗"
echo "║  Crypto Trading Bot - VPS Deployment Script   ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Install Docker first: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Install Docker Compose: apt install docker-compose -y"
    exit 1
fi

echo "✓ Docker installed"
echo "✓ Docker Compose installed"
echo ""

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml not found!"
    echo "Please create config.yaml from config.yaml.example"
    exit 1
fi

# Check if Gemini API key is configured
if grep -q "YOUR_GEMINI_API_KEY" config.yaml; then
    echo "⚠️  WARNING: Gemini API key not configured in config.yaml"
    echo "Please update config.yaml with your Gemini API key"
    echo "Get free key at: https://makersuite.google.com/app/apikey"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting bot container..."
docker-compose up -d

echo ""
echo "✓ Bot deployed successfully!"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "📈 Check status: docker-compose ps"
echo "🛑 Stop bot: docker-compose stop"
echo "🔄 Restart bot: docker-compose restart"
echo ""
echo "Bot is now running in the background! 🎉"
