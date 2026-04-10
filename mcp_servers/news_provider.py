"""
News API Provider - No API Key Required

Provides news data via multiple free news sources.
This provider sources news from various outlets without requiring an API key.

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

# Using NewsAPI.org free tier (limited requests per day but no key required for basic usage)
# Alternative: Using RSS feeds or other free sources
NEWSAPI_URL = "https://newsapi.org/v2"

# For truly keyless solution, we can use these free endpoints:
GNEWS_API = "https://gnews.io/api/v4"  # Free tier available
CURRENTS_API = "https://api.currentsapi.services/v1"  # Free tier available


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
    Search for news articles using GNews API (free, no key required)
    
    Args:
        query: Search query (e.g., "artificial intelligence")
        language: Language code (en, fr, de, etc.)
        sort_by: Sort by 'publishedAt' or 'relevance'
        pages: Number of pages (max 3 per free tier)
        
    Returns:
        NewsSearchResult with articles
    """
    try:
        async with httpx.AsyncClient() as client:
            # Using GNews API which has a free tier
            response = await client.get(
                f"{GNEWS_API}/search",
                params={
                    "q": query,
                    "lang": language,
                    "sortby": sort_by,
                    "max": min(pages * 10, 30)
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    url=item.get("url", ""),
                    source=item.get("source", {}).get("name", "Unknown"),
                    published_at=item.get("publishedAt", ""),
                    image_url=item.get("image", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=len(articles),
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error searching news for '{query}': {e}")
        raise


async def get_top_headlines(
    category: str = "general",
    language: str = "en",
    country: Optional[str] = None,
    limit: int = 10
) -> NewsSearchResult:
    """
    Get top headlines for a category
    
    Args:
        category: News category (business, entertainment, general, health, science, sports, technology)
        language: Language code
        country: Country code (optional)
        limit: Number of articles to return
        
    Returns:
        NewsSearchResult with top headline articles
    """
    try:
        # Map categories to search terms for broader results
        category_queries = {
            "business": "business news",
            "entertainment": "entertainment news",
            "general": "news today",
            "health": "health news",
            "science": "science news",
            "sports": "sports news",
            "technology": "technology news"
        }
        
        query = category_queries.get(category, "news today")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GNEWS_API}/search",
                params={
                    "q": query,
                    "lang": language,
                    "max": limit,
                    "sortby": "publishedAt"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("articles", [])[:limit]:
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", ""),
                    url=item.get("url", ""),
                    source=item.get("source", {}).get("name", "Unknown"),
                    published_at=item.get("publishedAt", ""),
                    image_url=item.get("image", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=len(articles),
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error getting headlines for category '{category}': {e}")
        raise


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
