import httpx
import json
from datetime import datetime

# Test NewsData.io API directly
NEWSDATA_API = "https://newsdata.io/api/1"
NEWSDATA_API_KEY = "demo"

print("Testing NewsData.io API with demo key...")
print("=" * 60)

try:
    # Test 1: Without limit parameter
    print("\n--- Test 1: Without limit parameter ---")
    response = httpx.get(
        f"{NEWSDATA_API}/news",
        params={
            "q": "AI",
            "language": "en",
            "apikey": NEWSDATA_API_KEY
        },
        timeout=15.0
    )
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2)[:1500])
    
    # Test 2: With size parameter instead
    print("\n--- Test 2: With size parameter instead ---")
    response = httpx.get(
        f"{NEWSDATA_API}/news",
        params={
            "q": "AI",
            "language": "en",
            "apikey": NEWSDATA_API_KEY,
            "size": 10
        },
        timeout=15.0
    )
    
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2)[:1500])
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
