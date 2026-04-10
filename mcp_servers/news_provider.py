"""
News API Provider - Using NewsAPI.org (Free Tier)

Provides news data from NewsAPI.org which offers a free tier with API key.
Register at https://newsapi.org/register to get your free API key.

Tools provided:
- search_news: Search for news articles by keyword
- get_top_headlines: Get top headlines for a specific country/category  
- get_news_by_category: Get news in a specific category
"""

import json
import logging
import os
from typing import Optional
from datetime import datetime
import httpx
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NewsAPI Configuration
NEWSAPI_BASE_URL = "https://newsapi.org/v2"
# Get API key from environment variable
# If not set, provide helpful error message
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

if not NEWSAPI_KEY:
    logger.warning(
        "⚠️ NEWSAPI_KEY environment variable not set!\n"
        "Register at https://newsapi.org/register to get a FREE API key\n"
        "Then set environment variable: NEWSAPI_KEY=your_api_key_here"
    )


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
    Search for news articles by keyword using NewsAPI
    
    Args:
        query: Search query (e.g., "artificial intelligence", "COVID-19")
        language: Language code (en, es, fr, de, etc.)
        sort_by: Sort by 'publishedAt', 'relevancy', or 'popularity'
        pages: Number of pages (max 5 per free tier)
        
    Returns:
        NewsSearchResult with articles
    """
    if not NEWSAPI_KEY:
        logger.error("NEWSAPI_KEY not configured")
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Map sort_by parameter to NewsAPI format
            sort_mapping = {
                "publishedAt": "publishedAt",
                "relevancy": "relevancy",
                "popularity": "popularity"
            }
            newsapi_sort = sort_mapping.get(sort_by, "publishedAt")
            
            # Calculate page number (1-indexed for NewsAPI)
            page_num = pages if pages >= 1 else 1
            
            response = await client.get(
                f"{NEWSAPI_BASE_URL}/everything",
                params={
                    "q": query,
                    "language": language,
                    "sortBy": newsapi_sort,
                    "page": page_num,
                    "pageSize": min(100, 20 * pages),  # Max 100 per request
                    "apiKey": NEWSAPI_KEY
                },
                timeout=15.0
            )
            
            # Handle API errors gracefully
            if response.status_code == 401:
                logger.error("Invalid NEWSAPI_KEY - please check your API key")
                return NewsSearchResult(
                    articles=[],
                    total_results=0,
                    timestamp=datetime.now().isoformat()
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors in response
            if data.get("status") == "error":
                logger.error(f"NewsAPI Error: {data.get('message', 'Unknown error')}")
                return NewsSearchResult(
                    articles=[],
                    total_results=0,
                    timestamp=datetime.now().isoformat()
                )
            
            articles = []
            for item in data.get("articles", []):
                # Skip articles with missing critical fields
                if not item.get("title") or not item.get("url"):
                    continue
                
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", "") or item.get("content", ""),
                    url=item.get("url", ""),
                    source=item.get("source", {}).get("name", "Unknown"),
                    published_at=item.get("publishedAt", ""),
                    image_url=item.get("urlToImage", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=data.get("totalResults", len(articles)),
                timestamp=datetime.now().isoformat()
            )
            
    except httpx.TimeoutException:
        logger.error(f"Timeout while searching news for '{query}'")
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error searching news for '{query}': {e}")
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
    Get top headlines for a category or country using NewsAPI
    
    Args:
        category: News category (business, entertainment, general, health, science, sports, technology)
        language: Language code (en, es, fr, de, etc.)
        country: Country code (us, gb, ca, au, etc.) - optional
        limit: Number of articles to return (max 100)
        
    Returns:
        NewsSearchResult with top headline articles
    """
    if not NEWSAPI_KEY:
        logger.error("NEWSAPI_KEY not configured")
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Validate category
            valid_categories = [
                "business", "entertainment", "general", "health", 
                "science", "sports", "technology"
            ]
            category_lower = category.lower()
            if category_lower not in valid_categories:
                category_lower = "general"
            
            # Use top-headlines endpoint
            params = {
                "category": category_lower,
                "pageSize": min(limit, 100),
                "apiKey": NEWSAPI_KEY
            }
            
            # Add country if provided
            if country:
                params["country"] = country
            else:
                # Default to US if no country specified
                params["country"] = "us"
            
            response = await client.get(
                f"{NEWSAPI_BASE_URL}/top-headlines",
                params=params,
                timeout=15.0
            )
            
            # Handle API errors
            if response.status_code == 401:
                logger.error("Invalid NEWSAPI_KEY - please check your API key")
                return NewsSearchResult(
                    articles=[],
                    total_results=0,
                    timestamp=datetime.now().isoformat()
                )
            
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors in response
            if data.get("status") == "error":
                logger.error(f"NewsAPI Error: {data.get('message', 'Unknown error')}")
                return NewsSearchResult(
                    articles=[],
                    total_results=0,
                    timestamp=datetime.now().isoformat()
                )
            
            articles = []
            for item in data.get("articles", [])[:limit]:
                # Skip articles with missing critical fields
                if not item.get("title") or not item.get("url"):
                    continue
                
                articles.append(NewsArticle(
                    title=item.get("title", ""),
                    description=item.get("description", "") or item.get("content", ""),
                    url=item.get("url", ""),
                    source=item.get("source", {}).get("name", "Unknown"),
                    published_at=item.get("publishedAt", ""),
                    image_url=item.get("urlToImage", ""),
                    content=item.get("content", "")
                ))
            
            return NewsSearchResult(
                articles=articles,
                total_results=data.get("totalResults", len(articles)),
                timestamp=datetime.now().isoformat()
            )
            
    except httpx.TimeoutException:
        logger.error(f"Timeout while getting headlines for category '{category}'")
        return NewsSearchResult(
            articles=[],
            total_results=0,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting headlines for category '{category}': {e}")
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
    Get news articles by category (alias for get_top_headlines)
    
    Args:
        category: News category (business, entertainment, general, health, science, sports, technology)
        language: Language code (en, es, fr, etc.)
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
                "description": "Search for news articles by keyword using NewsAPI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (e.g., 'artificial intelligence', 'climate change', 'COVID-19')"
                        },
                        "language": {
                            "type": "string",
                            "description": "Language code (en, es, fr, de, etc. - default: 'en')",
                            "default": "en"
                        },
                        "sort_by": {
                            "type": "string",
                            "description": "Sort by 'publishedAt', 'relevancy', or 'popularity' (default: 'publishedAt')",
                            "default": "publishedAt"
                        },
                        "pages": {
                            "type": "integer",
                            "description": "Page number (1-5, default 1)",
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
                "description": "Get top news headlines for a specific category (using NewsAPI)",
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
                        "country": {
                            "type": "string",
                            "description": "Country code (us, gb, ca, au, etc. - default: 'us')",
                            "default": "us"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of articles (default: 10, max: 100)",
                            "default": 10
                        }
                    },
                    "required": ["category"]
                }
            }
        }
    ]
