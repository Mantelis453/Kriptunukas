#!/bin/bash
# Stop the trading bot

echo "🛑 Stopping trading bot..."

# Find and kill the bot process
pkill -f "python3 main.py --demo"

if [ $? -eq 0 ]; then
    echo "✅ Bot stopped successfully!"
else
    echo "⚠️  No running bot found"
fi

# Show any remaining processes
echo ""
echo "Checking for remaining bot processes..."
ps aux | grep "python3 main.py" | grep -v grep
