#!/usr/bin/env python
"""
Quick test script to verify NewsAPI integration
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp_servers.news_provider import search_news, get_top_headlines

# Load environment variables
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

if not NEWSAPI_KEY:
    print("❌ ERROR: NEWSAPI_KEY not found in .env file")
    print("\nPlease:")
    print("1. Edit .env file and add your API key: NEWSAPI_KEY=your_key_here")
    print("2. Get your free key at: https://newsapi.org/register")
    exit(1)

print(f"✅ NEWSAPI_KEY found: {NEWSAPI_KEY[:10]}...{NEWSAPI_KEY[-10:]}")
print("\n" + "="*60)

async def test_news_api():
    """Test the news API implementation"""
    
    print("\n📰 Test 1: Search for 'AI news'")
    print("-" * 60)
    try:
        result = await search_news("AI news", language="en")
        print(f"✅ Found {len(result.articles)} articles")
        if result.articles:
            print(f"\nTop result:")
            article = result.articles[0]
            print(f"  Title: {article.title[:80]}")
            print(f"  Source: {article.source}")
            print(f"  URL: {article.url}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("\n📰 Test 2: Get top technology headlines")
    print("-" * 60)
    try:
        result = await get_top_headlines(category="technology", country="us", limit=5)
        print(f"✅ Found {len(result.articles)} articles")
        if result.articles:
            print(f"\nTop results:")
            for i, article in enumerate(result.articles[:3], 1):
                print(f"\n{i}. {article.title[:70]}")
                print(f"   Source: {article.source}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("\n📰 Test 3: Search for 'weather updates'")
    print("-" * 60)
    try:
        result = await search_news("weather updates", language="en")
        print(f"✅ Found {len(result.articles)} articles")
        if result.articles:
            print(f"\nTop result:")
            article = result.articles[0]
            print(f"  Title: {article.title[:80]}")
            print(f"  Published: {article.published_at[:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("\n✅ All tests completed!")
    print("\n🚀 Next step: Run the app with: streamlit run app.py")

if __name__ == "__main__":
    asyncio.run(test_news_api())
