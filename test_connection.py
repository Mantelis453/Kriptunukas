"""
Diagnostic script to test Bybit testnet connection
"""
import ccxt
import yaml
import sys

print("=" * 60)
print("BYBIT TESTNET CONNECTION DIAGNOSTIC")
print("=" * 60)

# Load config
try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print("✓ Config loaded successfully")
except Exception as e:
    print(f"✗ Failed to load config: {e}")
    sys.exit(1)

# Get credentials
api_key = config['exchange']['api_key']
api_secret = config['exchange']['api_secret']

print(f"\nAPI Key length: {len(api_key)} characters")
print(f"API Secret length: {len(api_secret)} characters")
print(f"API Key (first 5 chars): {api_key[:5]}...")
print(f"API Secret (first 5 chars): {api_secret[:5]}...")

# Test 1: Public endpoint (no auth)
print("\n" + "=" * 60)
print("TEST 1: Public Endpoint (No Authentication)")
print("=" * 60)

try:
    exchange = ccxt.bybit({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'linear',  # Try linear instead of future
            'testnet': True
        }
    })

    ticker = exchange.fetch_ticker('BTC/USDT:USDT')
    print(f"✓ Public API works - BTC/USDT price: ${ticker['last']}")
except Exception as e:
    print(f"✗ Public API failed: {e}")

# Test 2: Authentication with different configurations
print("\n" + "=" * 60)
print("TEST 2: Authentication Test")
print("=" * 60)

configs_to_try = [
    {
        'name': 'Linear Testnet',
        'config': {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'linear',
                'testnet': True
            }
        }
    },
    {
        'name': 'Future Testnet',
        'config': {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'testnet': True
            }
        }
    },
    {
        'name': 'Swap Testnet',
        'config': {
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'swap',
                'testnet': True
            }
        }
    }
]

for test_config in configs_to_try:
    print(f"\nTrying: {test_config['name']}")
    try:
        exchange = ccxt.bybit(test_config['config'])
        balance = exchange.fetch_balance()
        print(f"✓ SUCCESS with {test_config['name']}")
        print(f"  USDT Balance: {balance.get('USDT', {}).get('free', 0)}")
        print(f"  Total Balance: {balance.get('USDT', {}).get('total', 0)}")
        print(f"\n  >>> USE THIS CONFIGURATION! <<<")
        break
    except Exception as e:
        error_msg = str(e)
        print(f"✗ Failed: {error_msg[:100]}")

# Test 3: Check API key format
print("\n" + "=" * 60)
print("TEST 3: API Key Format Check")
print("=" * 60)

issues = []

if len(api_key) < 15:
    issues.append(f"API key seems too short ({len(api_key)} chars). Usually 20-30+ chars.")

if len(api_secret) < 30:
    issues.append(f"API secret seems too short ({len(api_secret)} chars). Usually 30-40+ chars.")

if ' ' in api_key or ' ' in api_secret:
    issues.append("Found spaces in credentials - remove them!")

if api_key.startswith('"') or api_key.endswith('"'):
    issues.append("API key has extra quotes - they should be: api_key: \"value\" not \"\\\"value\\\"\"")

if issues:
    print("\n⚠️  Potential issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✓ Credentials format looks OK")

# Test 4: Alternative - Check if testnet is accessible
print("\n" + "=" * 60)
print("TEST 4: Testnet Accessibility")
print("=" * 60)

try:
    import requests
    response = requests.get('https://api-testnet.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT', timeout=10)
    if response.status_code == 200:
        print("✓ Bybit testnet API is accessible")
        data = response.json()
        if data.get('retCode') == 0:
            print("✓ Testnet API responding correctly")
    else:
        print(f"✗ Testnet returned status code: {response.status_code}")
except Exception as e:
    print(f"✗ Cannot reach testnet: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nNext Steps:")
print("1. If TEST 2 succeeded, update data/collector.py with that config")
print("2. If all tests failed, verify your API keys at https://testnet.bybit.com")
print("3. Make sure API key has 'Contract Trading' permission enabled")
print("4. Check if there's an IP whitelist restriction on your API key")
