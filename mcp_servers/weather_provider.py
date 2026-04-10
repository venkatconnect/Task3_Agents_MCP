"""
Open-Meteo Weather MCP Server

Provides weather data via the free Open-Meteo API.
API Docs: https://open-meteo.com/en/docs

Tools provided:
- get_current_weather: Get current weather for a location
- get_weather_forecast: Get 7-day weather forecast for a location
- get_air_quality: Get air quality data for a location
"""

import json
import logging
from typing import Any, Optional
import httpx
from datetime import datetime
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
OPEN_METEO_API = "https://api.open-meteo.com/v1"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1"


class WeatherData(BaseModel):
    """Structured weather data response"""
    location: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    weather_condition: str
    wind_speed: float
    precipitation: float
    timestamp: str


class WeatherForecast(BaseModel):
    """Structured weather forecast response"""
    location: str
    forecast_days: list
    timestamp: str


async def get_coordinates(location: str) -> tuple[float, float]:
    """
    Get latitude and longitude for a location using Open-Meteo Geocoding API
    
    Args:
        location: City name or address
        
    Returns:
        Tuple of (latitude, longitude)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GEOCODING_API}/search",
                params={
                    "name": location,
                    "count": 1,
                    "language": "en",
                    "format": "json"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                raise ValueError(f"Location '{location}' not found")
            
            result = data["results"][0]
            return result["latitude"], result["longitude"]
    except Exception as e:
        logger.error(f"Error fetching coordinates for {location}: {e}")
        raise


async def get_current_weather(location: str) -> WeatherData:
    """
    Get current weather for a location
    
    Args:
        location: City name (e.g., "New York", "London")
        
    Returns:
        WeatherData object with current conditions
    """
    try:
        # Get coordinates
        latitude, longitude = await get_coordinates(location)
        
        # Fetch current weather
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPEN_METEO_API}/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
                    "temperature_unit": "fahrenheit",
                    "wind_speed_unit": "mph",
                    "timezone": "auto"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            
            # Map weather codes to descriptions
            weather_description = _get_weather_description(current.get("weather_code", 0))
            
            return WeatherData(
                location=location,
                latitude=latitude,
                longitude=longitude,
                temperature=current.get("temperature_2m", 0),
                feels_like=current.get("apparent_temperature", 0),
                humidity=current.get("relative_humidity_2m", 0),
                weather_condition=weather_description,
                wind_speed=current.get("wind_speed_10m", 0),
                precipitation=current.get("precipitation", 0),
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error getting weather for {location}: {e}")
        raise


async def get_weather_forecast(location: str, days: int = 7) -> WeatherForecast:
    """
    Get weather forecast for a location
    
    Args:
        location: City name
        days: Number of days to forecast (1-16)
        
    Returns:
        WeatherForecast object with forecast data
    """
    try:
        # Get coordinates
        latitude, longitude = await get_coordinates(location)
        
        # Fetch forecast
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{OPEN_METEO_API}/forecast",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
                    "temperature_unit": "fahrenheit",
                    "wind_speed_unit": "mph",
                    "timezone": "auto",
                    "forecast_days": min(days, 16)
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            daily = data.get("daily", {})
            times = daily.get("time", [])
            
            forecast_list = []
            for i, time_str in enumerate(times):
                weather_code = daily.get("weather_code", [])[i] if i < len(daily.get("weather_code", [])) else 0
                forecast_list.append({
                    "date": time_str,
                    "condition": _get_weather_description(weather_code),
                    "max_temp": daily.get("temperature_2m_max", [])[i] if i < len(daily.get("temperature_2m_max", [])) else 0,
                    "min_temp": daily.get("temperature_2m_min", [])[i] if i < len(daily.get("temperature_2m_min", [])) else 0,
                    "precipitation": daily.get("precipitation_sum", [])[i] if i < len(daily.get("precipitation_sum", [])) else 0,
                    "wind_speed": daily.get("wind_speed_10m_max", [])[i] if i < len(daily.get("wind_speed_10m_max", [])) else 0
                })
            
            return WeatherForecast(
                location=location,
                forecast_days=forecast_list[:days],
                timestamp=datetime.now().isoformat()
            )
    except Exception as e:
        logger.error(f"Error getting forecast for {location}: {e}")
        raise


def _get_weather_description(code: int) -> str:
    """
    Map WMO weather codes to descriptions
    Reference: https://www.weatherapi.com/docs/weather_codes.asp
    """
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, f"Unknown condition (code: {code})")


# MCP Tool definitions for use with Agent Framework
def get_mcp_tools() -> list[dict]:
    """
    Return tool definitions compatible with Microsoft Agent Framework
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get current weather conditions for a specified location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name (e.g., 'New York', 'London', 'Tokyo')"
                        }
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a location for the next 7 days",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days to forecast (1-16, default 7)",
                            "default": 7
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]
