"""
Weather & News Agent Orchestrator

Uses Microsoft Agent Framework to coordinate multiple agents:
- Weather Agent: Handles weather-related queries
- News Agent: Handles news-related queries
- Multi-Agent Orchestrator: Routes queries to appropriate agents

This agent can answer questions like:
- "What's the weather in New York?"
- "Tell me the latest news about AI"
- "Compare weather in London and Paris, and get tech news"
"""

import asyncio
import json
import logging
from typing import Optional, Any
from enum import Enum

# Import our data providers
from mcp_servers.weather_provider import (
    get_current_weather,
    get_weather_forecast,
    get_mcp_tools as get_weather_tools
)
from mcp_servers.news_provider import (
    search_news,
    get_top_headlines,
    get_mcp_tools as get_news_tools
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Types of agents in the system"""
    WEATHER = "weather"
    NEWS = "news"
    ORCHESTRATOR = "orchestrator"


class ToolCall:
    """Represents a tool call to be executed"""
    def __init__(self, tool_name: str, parameters: dict):
        self.tool_name = tool_name
        self.parameters = parameters
    
    def __repr__(self):
        return f"ToolCall({self.tool_name}, {self.parameters})"


class AgentResponse:
    """Structured response from an agent"""
    def __init__(
        self,
        agent_type: AgentType,
        message: str,
        tool_calls: Optional[list[ToolCall]] = None,
        execution_results: Optional[dict] = None
    ):
        self.agent_type = agent_type
        self.message = message
        self.tool_calls = tool_calls or []
        self.execution_results = execution_results or {}
    
    def to_dict(self) -> dict:
        return {
            "agent_type": self.agent_type.value,
            "message": self.message,
            "tool_calls": [
                {"tool_name": tc.tool_name, "parameters": tc.parameters}
                for tc in self.tool_calls
            ],
            "execution_results": self.execution_results
        }


class WeatherAgent:
    """
    Agent specialized for weather queries
    
    Capabilities:
    - Get current weather for a location
    - Get weather forecast
    - Answer questions about weather
    """
    
    def __init__(self):
        self.name = "WeatherAgent"
        self.tools = get_weather_tools()
        self.description = "Handles weather-related queries and provides current conditions and forecasts"
    
    async def process_query(self, query: str) -> AgentResponse:
        """
        Process a weather query
        
        Args:
            query: User's question about weather
            
        Returns:
            AgentResponse with weather information
        """
        logger.info(f"Weather Agent processing: {query}")
        
        # Extract location from query
        location = self._extract_location(query)
        
        if not location:
            return AgentResponse(
                agent_type=AgentType.WEATHER,
                message="Please specify a location for weather information (e.g., 'weather in New York')"
            )
        
        try:
            # Determine if forecast or current conditions
            is_forecast = any(word in query.lower() for word in ["forecast", "tomorrow", "next", "week", "days"])
            
            if is_forecast:
                # Get forecast
                forecast = await get_weather_forecast(location)
                message = self._format_forecast_message(forecast)
                
                return AgentResponse(
                    agent_type=AgentType.WEATHER,
                    message=message,
                    tool_calls=[ToolCall("get_weather_forecast", {"location": location})],
                    execution_results={"forecast": forecast.model_dump()}
                )
            else:
                # Get current weather
                weather = await get_current_weather(location)
                message = self._format_weather_message(weather)
                
                return AgentResponse(
                    agent_type=AgentType.WEATHER,
                    message=message,
                    tool_calls=[ToolCall("get_current_weather", {"location": location})],
                    execution_results={"weather": weather.model_dump()}
                )
        except Exception as e:
            logger.error(f"Error in WeatherAgent: {e}")
            return AgentResponse(
                agent_type=AgentType.WEATHER,
                message=f"Error retrieving weather information: {str(e)}"
            )
    
    def _extract_location(self, query: str) -> Optional[str]:
        """Extract location from query"""
        keywords = ["in ", "for ", "weather at ", "in the "]
        
        for keyword in keywords:
            if keyword in query.lower():
                # Extract text after keyword
                parts = query.lower().split(keyword)
                if len(parts) > 1:
                    location = parts[-1].split(" ")[0].strip("?,.")
                    if location and len(location) > 2:
                        return location
        
        return None
    
    def _format_weather_message(self, weather) -> str:
        """Format weather data into readable message"""
        return (
            f"🌤️ **Weather in {weather.location}**\n"
            f"Temperature: {weather.temperature}°F (feels like {weather.feels_like}°F)\n"
            f"Condition: {weather.weather_condition}\n"
            f"Humidity: {weather.humidity}%\n"
            f"Wind Speed: {weather.wind_speed} mph\n"
            f"Precipitation: {weather.precipitation} mm"
        )
    
    def _format_forecast_message(self, forecast) -> str:
        """Format forecast data into readable message"""
        message = f"📅 **7-Day Forecast for {forecast.location}**\n\n"
        
        for day in forecast.forecast_days[:7]:
            message += (
                f"**{day['date']}**\n"
                f"Condition: {day['condition']}\n"
                f"High: {day['max_temp']}°F | Low: {day['min_temp']}°F\n"
                f"Precipitation: {day['precipitation']} mm\n"
                f"Wind: {day['wind_speed']} mph\n\n"
            )
        
        return message


class NewsAgent:
    """
    Agent specialized for news queries
    
    Capabilities:
    - Search news by keyword
    - Get top headlines by category
    - Answer questions about current events
    """
    
    def __init__(self):
        self.name = "NewsAgent"
        self.tools = get_news_tools()
        self.description = "Handles news-related queries and provides latest news articles"
    
    async def process_query(self, query: str) -> AgentResponse:
        """
        Process a news query
        
        Args:
            query: User's question about news
            
        Returns:
            AgentResponse with news information
        """
        logger.info(f"News Agent processing: {query}")
        
        # Determine search strategy
        category = self._extract_category(query)
        search_term = self._extract_search_term(query)
        
        try:
            if category and not search_term:
                # Get headlines by category
                result = await get_top_headlines(category=category, limit=5)
                message = self._format_headlines_message(result, category)
                
                return AgentResponse(
                    agent_type=AgentType.NEWS,
                    message=message,
                    tool_calls=[ToolCall("get_top_headlines", {"category": category})],
                    execution_results={"news": result.model_dump()}
                )
            else:
                # Search for specific topic
                query_term = search_term or query.replace("latest", "").replace("news", "").strip()
                result = await search_news(query_term, pages=1)
                message = self._format_search_message(result, query_term)
                
                return AgentResponse(
                    agent_type=AgentType.NEWS,
                    message=message,
                    tool_calls=[ToolCall("search_news", {"query": query_term})],
                    execution_results={"news": result.model_dump()}
                )
        except Exception as e:
            logger.error(f"Error in NewsAgent: {e}")
            return AgentResponse(
                agent_type=AgentType.NEWS,
                message=f"Error retrieving news: {str(e)}"
            )
    
    def _extract_category(self, query: str) -> Optional[str]:
        """Extract news category from query"""
        categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        
        query_lower = query.lower()
        for category in categories:
            if category in query_lower:
                return category
        
        return None
    
    def _extract_search_term(self, query: str) -> Optional[str]:
        """Extract search term from query"""
        keywords = ["about ", "on ", "regarding ", "tell me about "]
        
        for keyword in keywords:
            if keyword in query.lower():
                parts = query.lower().split(keyword)
                if len(parts) > 1:
                    return parts[-1].strip("?,.").title()
        
        return None
    
    def _format_headlines_message(self, result, category: str) -> str:
        """Format headlines into readable message"""
        message = f"📰 **Top {category.title()} News**\n\n"
        
        for i, article in enumerate(result.articles[:5], 1):
            message += (
                f"**{i}. {article.title}**\n"
                f"Source: {article.source}\n"
                f"Published: {article.published_at}\n"
                f"{article.description}\n"
                f"[Read more]({article.url})\n\n"
            )
        
        return message
    
    def _format_search_message(self, result, search_term: str) -> str:
        """Format search results into readable message"""
        message = f"🔍 **News about {search_term}**\n\n"
        
        if not result.articles:
            return message + "No articles found for this search term."
        
        for i, article in enumerate(result.articles[:5], 1):
            message += (
                f"**{i}. {article.title}**\n"
                f"Source: {article.source}\n"
                f"Published: {article.published_at}\n"
                f"{article.description}\n"
                f"[Read more]({article.url})\n\n"
            )
        
        return message


class OrchestratorAgent:
    """
    Main orchestrator agent that routes queries to specialized agents
    
    Responsibilities:
    - Classify incoming queries
    - Route to appropriate specialized agents
    - Combine results from multiple agents if needed
    - Provide comprehensive responses
    """
    
    def __init__(self):
        self.name = "OrchestratorAgent"
        self.weather_agent = WeatherAgent()
        self.news_agent = NewsAgent()
        self.description = "Routes queries to specialized agents and combines results"
    
    async def process_query(self, query: str) -> dict:
        """
        Process a user query and route to appropriate agents
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with agent responses and final answer
        """
        logger.info(f"Orchestrator processing: {query}")
        
        # Classify the query
        query_type = self._classify_query(query)
        
        responses = []
        
        # Route query
        if query_type == "weather":
            response = await self.weather_agent.process_query(query)
            responses.append(response)
        
        elif query_type == "news":
            response = await self.news_agent.process_query(query)
            responses.append(response)
        
        elif query_type == "combined":
            # Process both types of queries
            weather_response = await self.weather_agent.process_query(query)
            news_response = await self.news_agent.process_query(query)
            responses.extend([weather_response, news_response])
        
        else:
            return {
                "agent": "OrchestratorAgent",
                "message": "I couldn't understand your query. Please ask about weather or news.",
                "responses": []
            }
        
        # Combine responses
        combined_message = self._combine_responses(responses)
        
        return {
            "agent": "OrchestratorAgent",
            "message": combined_message,
            "responses": [r.to_dict() for r in responses],
            "query_type": query_type
        }
    
    def _classify_query(self, query: str) -> str:
        """
        Classify query into types: weather, news, or combined
        """
        query_lower = query.lower()
        
        weather_keywords = ["weather", "temperature", "forecast", "rain", "snow", "wind", "cloudy", "hot", "cold"]
        news_keywords = ["news", "headlines", "article", "latest", "current events", "about"]
        
        has_weather = any(keyword in query_lower for keyword in weather_keywords)
        has_news = any(keyword in query_lower for keyword in news_keywords)
        
        if has_weather and has_news:
            return "combined"
        elif has_weather:
            return "weather"
        elif has_news:
            return "news"
        else:
            return "unknown"
    
    def _combine_responses(self, responses: list[AgentResponse]) -> str:
        """Combine responses from multiple agents"""
        if len(responses) == 1:
            return responses[0].message
        
        combined = "🤖 **Combined Report**\n\n"
        
        for i, response in enumerate(responses, 1):
            combined += f"**Agent {i}: {response.agent_type.value.title()}**\n"
            combined += response.message + "\n\n"
        
        return combined


# Main API for application integration
async def answer_question(question: str) -> dict:
    """
    Main entry point for answering questions about weather and news
    
    Args:
        question: User's question
        
    Returns:
        Dictionary with answer and metadata
    """
    orchestrator = OrchestratorAgent()
    result = await orchestrator.process_query(question)
    return result


if __name__ == "__main__":
    # Example usage
    async def main():
        # Test queries
        test_queries = [
            "What's the weather in New York?",
            "Tell me the latest technology news",
            "Weather forecast for London and top business news"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print(f"{'='*60}")
            
            result = await answer_question(query)
            print(result["message"])
    
    asyncio.run(main())
