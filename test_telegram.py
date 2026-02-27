"""
Test Telegram bot connection and get chat ID
"""
import requests
import yaml
import sys

print("=" * 60)
print("TELEGRAM BOT SETUP & TEST")
print("=" * 60)

# Load config
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']
    print(f"\n✓ Config loaded")
    print(f"  Bot Token: {bot_token[:20]}...{bot_token[-5:]}")
    print(f"  Chat ID: {chat_id}")
except Exception as e:
    print(f"\n✗ Failed to load config: {e}")
    sys.exit(1)

# Test 1: Check if bot is valid
print("\n" + "=" * 60)
print("TEST 1: Validate Bot Token")
print("=" * 60)

try:
    url = f"https://api.telegram.org/bot{bot_token}/getMe"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"\n✓ Bot is VALID!")
            print(f"  Bot Name: @{bot_info.get('username')}")
            print(f"  Bot ID: {bot_info.get('id')}")
            print(f"  First Name: {bot_info.get('first_name')}")
        else:
            print(f"\n✗ Bot token is invalid!")
            print(f"  Error: {data}")
            sys.exit(1)
    else:
        print(f"\n✗ Failed to validate bot token")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")
        sys.exit(1)

except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)

# Test 2: Get updates to find chat ID
print("\n" + "=" * 60)
print("TEST 2: Get Recent Messages (to find your Chat ID)")
print("=" * 60)

try:
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        if data.get('ok') and data.get('result'):
            updates = data['result']
            print(f"\n✓ Found {len(updates)} recent message(s)")

            chat_ids = set()
            for update in updates:
                if 'message' in update:
                    msg = update['message']
                    from_user = msg.get('from', {})
                    chat = msg.get('chat', {})

                    chat_id_found = chat.get('id')
                    chat_ids.add(str(chat_id_found))

                    print(f"\n  Message from: {from_user.get('first_name')} (@{from_user.get('username')})")
                    print(f"  Chat ID: {chat_id_found}")
                    print(f"  Text: {msg.get('text', 'N/A')[:50]}")

            if chat_ids:
                print(f"\n📝 Available Chat IDs: {', '.join(chat_ids)}")

                if chat_id in chat_ids:
                    print(f"\n✓ Your configured chat_id ({chat_id}) is CORRECT!")
                else:
                    print(f"\n⚠️  Your configured chat_id ({chat_id}) doesn't match!")
                    print(f"   Update config.yaml with one of: {', '.join(chat_ids)}")

        else:
            print(f"\n⚠️  No recent messages found!")
            print(f"\n📱 ACTION REQUIRED:")
            print(f"   1. Open Telegram app")
            print(f"   2. Search for: @{bot_info.get('username')}")
            print(f"   3. Click 'START' or send any message")
            print(f"   4. Run this script again")

    else:
        print(f"\n✗ Failed to get updates")
        print(f"  Status: {response.status_code}")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Test 3: Send test message
print("\n" + "=" * 60)
print("TEST 3: Send Test Message")
print("=" * 60)

try:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': '🤖 <b>Telegram Setup Test</b>\n\n✅ Your crypto trading bot is connected!\n\nThis is a test message from the setup script.',
        'parse_mode': 'HTML'
    }

    response = requests.post(url, json=payload, timeout=10)

    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            print(f"\n✅ SUCCESS! Test message sent!")
            print(f"\n   Check your Telegram app - you should see the message!")
        else:
            print(f"\n✗ Failed to send message")
            print(f"  Error: {data}")
    else:
        print(f"\n✗ Failed to send message")
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text}")

        if response.status_code == 400:
            print(f"\n💡 TIP: Bad Request usually means:")
            print(f"   - Wrong chat_id")
            print(f"   - You haven't started the bot yet")
            print(f"   - Bot was blocked by user")

except Exception as e:
    print(f"\n✗ Error: {e}")

print("\n" + "=" * 60)
print("SETUP COMPLETE")
print("=" * 60)

print("\n📋 Summary:")
print("  1. If test message sent successfully → Telegram is ready!")
print("  2. If no messages found → Start your bot in Telegram first")
print("  3. If wrong chat_id → Update config.yaml with correct one")

print("\n🚀 Next Step:")
print("  Run the trading bot: python3 main.py --demo --once")
