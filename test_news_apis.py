import httpx
import json

print("Testing NewsAPI endpoints...")
print("=" * 60)

# Test 1: NewsAPI general endpoint without key
try:
    print("\n--- Test 1: NewsAPI without API key ---")
    response = httpx.get(
        "https://newsapi.org/v2/top-headlines",
        params={
            "country": "us",
            "sortBy": "publishedAt"
        },
        timeout=10.0
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2)[:500])
except Exception as e:
    print(f"Error: {e}")

# Test 2: GNews without key
try:
    print("\n--- Test 2: GNews without API key ---")
    response = httpx.get(
        "https://gnews.io/api/v4/search",
        params={
            "q": "technology"
        },
        timeout=10.0
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2)[:500])
except Exception as e:
    print(f"Error: {e}")

# Test 3: Check if NewsAPI has free tier info
try:
    print("\n--- Test 3: NewsAPI free tier endpoint ---")
    response = httpx.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": "AI",
            "sortBy": "publishedAt",
            "language": "en"
        },
        timeout=10.0
    )
    print(f"Status: {response.status_code}")
    data = response.json()
    print(json.dumps(data, indent=2)[:500])
except Exception as e:
    print(f"Error: {e}")
