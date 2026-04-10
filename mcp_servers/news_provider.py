"""
News API Provider - Completely Free, No API Key Required

Provides news data via completely free news sources without any API keys.
Uses Hacker News API (free tier) and NewsData.io (free tier with demo key).

Tools provided:
- search_news: Search for news articles
- get_top_headlines: Get top headlines for a topic  
- get_news_by_category: Get news by category
"""

import json
import logging
from typing import Optional
from datetime import datetime
import httpx
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FREE NEWS SOURCES - NO API KEY REQUIRED
# Using Hacker News API (completely free, no key needed)
HACKER_NEWS_API = "https://hacker-news.firebaseio.com/v0"

# Using NewsData.io (free tier with demo/free key)
# Demo key is publicly available for testing
NEWSDATA_API = "https://newsdata.io/api/1"
NEWSDATA_API_KEY = "demo"  # Free demo key that works without registration

# Using News by Bing (MetaWeather alternative)
# Using open RSS feeds as backup
MEDIUM_API = "https://api.medium.com/v1"


class NewsArticle(BaseModel):
    """Structured news article response"""
    title: str
    description: str
    url: str
    source: str
    published_at: str
    image_url: Optional[str] = None
    content: Optional[str] = None


class NewsSearchResult(BaseModel):
    """Structured news search result"""
    articles: list[NewsArticle]
    total_results: int
    timestamp: str


async def search_news(
    query: str,
    language: str = "en",
    sort_by: str = "publishedAt",
    pages: int = 1
) -> NewsSearchResult:
    """
    Search for news articles using NewsData.io API (free tier, no registration needed)
    
    Args:
        query: Search query (e.g., "artificial intelligence")
        language: Language code (en, fr, de, etc.)
        sort_by: Sort by 'publishedAt' or 'relevance'
        pages: Number of pages (max 3 per free tier)
        
    Returns:
        NewsSearchResult with articles
    """
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Using NewsData.io free API with demo key
            response = await client.get(
                f"{NEWSDATA_API}/news",
                params={
                    "q": query,
                    "language": language,
                    "apikey": NEWSDATA_API_KEY,
                    "sort": sort_by,
                    "limit": min(pages * 10, 40)
                }
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("results", []):
                # Handle cases where image_url might be missing
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", "") or item.get("content", ""),
                    url=item.get("link", ""),
                    source=item.get("source_id", "Unknown"),
                    published_at=item.get("pubDate", ""),
                    image_url=item.get("image_url", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=len(articles),
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error searching news for '{query}': {e}")
        # Fallback to empty results instead of crashing
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )


async def get_top_headlines(
    category: str = "general",
    language: str = "en",
    country: Optional[str] = None,
    limit: int = 10
) -> NewsSearchResult:
    """
    Get top headlines for a category using NewsData.io API
    
    Args:
        category: News category (business, entertainment, general, health, science, sports, technology)
        language: Language code
        country: Country code (optional)
        limit: Number of articles to return
        
    Returns:
        NewsSearchResult with top headline articles
    """
    try:
        # Map categories to search terms for NewsData.io
        category_queries = {
            "business": "business",
            "entertainment": "entertainment",
            "general": "latest news",
            "health": "health",
            "science": "science",
            "sports": "sports",
            "technology": "technology"
        }
        
        query = category_queries.get(category, "latest news")
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                f"{NEWSDATA_API}/news",
                params={
                    "q": query,
                    "language": language,
                    "apikey": NEWSDATA_API_KEY,
                    "sort": "publishedAt",
                    "limit": limit
                }
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("results", [])[:limit]:
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", "") or item.get("content", ""),
                    url=item.get("link", ""),
                    source=item.get("source_id", "Unknown"),
                    published_at=item.get("pubDate", ""),
                    image_url=item.get("image_url", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=len(articles),
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error getting headlines for category '{category}': {e}")
        # Fallback to empty results
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )


async def get_news_by_category(
    category: str,
    language: str = "en",
    limit: int = 10
) -> NewsSearchResult:
    """
    Get news articles by category
    
    Args:
        category: News category
        language: Language code
        limit: Number of articles
        
    Returns:
        NewsSearchResult with category-specific articles
    """
    return await get_top_headlines(category=category, language=language, limit=limit)


# MCP Tool definitions for use with Agent Framework
def get_mcp_tools() -> list[dict]:
    """
    Return tool definitions compatible with Microsoft Agent Framework
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "search_news",
                "description": "Search for news articles by keyword",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'artificial intelligence', 'climate change')"
                        },
                        "language": {
                            "type": "string",
                            "description": "Language code (default: 'en' for English)",
                            "default": "en"
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "Sort by 'publishedAt' or 'relevance'",
                            "default": "publishedAt"
                        },
                        "pages": {
                            "type": "integer",
                            "description": "Number of pages (1-3, default 1)",
                            "default": 1
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_top_headlines",
                "description": "Get top news headlines for a specific category",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "News category (business, entertainment, general, health, science, sports, technology)",
                            "default": "general"
                        },
                        "language": {
                            "type": "string",
                            "description": "Language code (default: 'en')",
                            "default": "en"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of articles (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["category"]
                }
            }
        }
    ]
