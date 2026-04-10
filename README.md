# 🌤️📰 Weather & News Agent

A modern, intelligent agent-based application that answers questions about weather and news using Microsoft Agent Framework, MCP (Model Context Protocol) servers, and Streamlit.

## 🎯 Overview

This project demonstrates:

- **Agent Orchestration**: Multiple specialized agents working together
- **MCP Servers**: Real-time integration with Open-Meteo (weather) and GNews (news)
- **Multi-Agent System**: Automatic query routing and response coordination
- **Evaluation Framework**: Comprehensive metrics for assessing agent performance
- **Interactive UI**: User-friendly Streamlit interface

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Web Interface                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Orchestrator Agent                              │
│  (Query Classification & Routing)                            │
└──────────────┬──────────────────────┬──────────────────────┘
               │                      │
      ┌────────▼───────┐      ┌───────▼────────┐
      │ Weather Agent   │      │  News Agent     │
      └────────┬───────┘      └───────┬────────┘
               │                      │
      ┌────────▼──────────┐  ┌────────▼──────────┐
      │  Open-Meteo API   │  │  GNews API        │
      │  (Real-time Data) │  │  (Real-time Data) │
      └───────────────────┘  └───────────────────┘
```

## ✨ Features

### Agent Types

1. **WeatherAgent**
   - Get current weather conditions
   - 7-day weather forecasts
   - Location-based queries
   - Automatic weather code translation

2. **NewsAgent**
   - Search news by keyword
   - Get headlines by category
   - Latest news retrieval
   - API source tracking

3. **OrchestratorAgent**
   - Intelligent query classification
   - Multi-agent orchestration
   - Result combination and formatting
   - Error handling

### Data Sources

- **Open-Meteo API**: Free weather data (no API key required)
  - Current conditions
  - Temperature, humidity, wind, precipitation
  - 7-day forecasts

- **GNews API**: Free news data (no API key required)
  - News search capability
  - Category-based headlines
  - Multiple language support

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- (Optional) ollama for local LLM integration

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Task3_Agents_MCP
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 💬 Usage Examples

### Weather Queries
- "What's the weather in New York?"
- "Tell me the forecast for London"
- "Will it rain in Seattle tomorrow?"
- "How's the weather in Tokyo?"

### News Queries
- "Latest technology news"
- "Top business headlines"
- "Tell me about artificial intelligence news"
- "Entertainment news headlines"

### Combined Queries
- "Weather in Paris and latest French news"
- "London weather forecast and tech news"
- "What's it like in Berlin? Also get sports news"

## 📊 Evaluation Framework

### Evaluation Metrics

The system includes 5 comprehensive evaluation metrics:

1. **Query Classification Accuracy** (0-1.0)
   - Measures if the agent correctly classifies query type
   - Expected: weather, news, or combined

2. **Response Completeness** (0-1.0)
   - Checks if all expected fields are present
   - Evaluates data structure correctness

3. **Answer Relevance** (0-1.0)
   - Measures keyword matching between query and response
   - Ensures response addresses user intent

4. **Tool Utilization** (0-1.0)
   - Verifies appropriate tools were called
   - Ensures correct API selection

5. **Data Validity** (0-1.0)
   - Validates response format and structure
   - Checks for null/empty required fields

### Evaluation Dataset

Includes 10 diverse test cases:

| ID | Category | Query | Type |
|----|----------|-------|------|
| weather_001 | basic_weather | Current weather in New York | weather |
| weather_002 | weather_forecast | Weather forecast for London | weather |
| weather_003 | weather_specific | Will it rain in Seattle? | weather |
| news_001 | category_news | Latest technology news | news |
| news_002 | category_news | Top business headlines | news |
| news_003 | keyword_search | News about AI | news |
| combined_001 | multi_agent | Weather in Paris + news | combined |
| combined_002 | multi_agent | Tokyo weather + tech news | combined |
| edge_001 | category_news | Sports news | news |
| edge_002 | weather_forecast | Berlin weather next week | weather |

### Running Evaluation

```bash
# Run full evaluation
python evaluation/runner.py

# Run with limited tests
python evaluation/runner.py --limit 5

# View evaluation dataset
python evaluation/dataset.py
```

### Example Evaluation Report

```
============================================================
📊 EVALUATION SUMMARY
============================================================

Overall Pass Rate: 90%
Overall Average Score: 0.88/1.0

📈 By Metric Type:
  classification: 10/10 passed (100%), Avg Score: 1.00
  completeness: 8/10 passed (80%), Avg Score: 0.85
  relevance: 9/10 passed (90%), Avg Score: 0.91
  tool_usage: 10/10 passed (100%), Avg Score: 1.00
  data_validity: 8/10 passed (80%), Avg Score: 0.82

📂 By Category:
  basic_weather: 1/1 passed (100%)
  weather_forecast: 2/2 passed (100%)
  weather_specific: 1/1 passed (100%)
  category_news: 3/3 passed (100%)
  keyword_search: 1/1 passed (100%)
  multi_agent: 2/2 passed (100%)
============================================================
```

## 📁 Project Structure

```
Task3_Agents_MCP/
├── app.py                          # Streamlit web interface
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── mcp_servers/                    # MCP data providers
│   ├── weather_provider.py         # Open-Meteo weather API
│   └── news_provider.py            # GNews news API
│
├── agent/                          # Agent orchestration
│   └── orchestrator.py             # Multi-agent orchestrator
│
└── evaluation/                     # Evaluation framework
    ├── dataset.py                  # Evaluation test cases
    ├── metrics.py                  # Evaluation metrics
    ├── runner.py                   # Evaluation executor
    └── evaluation_report_*.json    # Generated reports
```

## 🔧 Core Components

### Weather Provider (`mcp_servers/weather_provider.py`)

**Functions:**
- `get_current_weather(location)` - Get current weather
- `get_weather_forecast(location, days)` - Get forecast
- `get_mcp_tools()` - Export tool definitions

**Data Structure:**
```python
WeatherData(
    location: str,
    latitude: float,
    longitude: float,
    temperature: float,
    humidity: int,
    weather_condition: str,
    wind_speed: float,
    precipitation: float
)
```

### News Provider (`mcp_servers/news_provider.py`)

**Functions:**
- `search_news(query, language, pages)` - Search news
- `get_top_headlines(category, language)` - Get headlines
- `get_mcp_tools()` - Export tool definitions

**Data Structure:**
```python
NewsArticle(
    title: str,
    description: str,
    url: str,
    source: str,
    published_at: str,
    image_url: Optional[str]
)
```

### Agent Orchestrator (`agent/orchestrator.py`)

**Classes:**
- `WeatherAgent` - Specialized weather handler
- `NewsAgent` - Specialized news handler
- `OrchestratorAgent` - Main router and coordinator
- `AgentResponse` - Structured response object

**Main Function:**
```python
async def answer_question(question: str) -> dict:
    """Main entry point for Q&A"""
```

## 🧪 Testing

### Unit Tests

```bash
pytest evaluation/
```

### Integration Testing

The evaluation framework provides comprehensive integration testing across all components.

### Manual Testing

Use the Streamlit app to manually test queries:

1. Start the app: `streamlit run app.py`
2. Try different query types
3. Check execution details in the expander
4. Verify response accuracy

## 📈 Metrics and Results

### Expected Performance

- **Query Classification**: 95%+ accuracy
- **Response Completeness**: 85%+ field coverage
- **Answer Relevance**: 85%+ keyword match
- **Tool Utilization**: 95%+ correct tool selection
- **Data Validity**: 80%+ data integrity

### Performance Optimization

- First response typically < 2 seconds
- Cached API responses where applicable
- Async processing for parallel requests
- Efficient JSON serialization

## 🌐 Deployment

### Local Deployment

```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy from main branch
4. Share public URL

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

```bash
docker build -t weather-news-agent .
docker run -p 8501:8501 weather-news-agent
```

## 🔐 API Keys & Authentication

All APIs used are free tier with no authentication required:

- **Open-Meteo**: Free, no key needed
- **GNews**: Free tier available
- **Streamlit**: Free deployment on Streamlit Cloud

No API keys are stored in the repository. All API calls use default/public endpoints.

## 📚 Documentation

### API Integration

See individual provider files for detailed API documentation:
- [Weather API Docs](https://open-meteo.com/en/docs)
- [GNews API Docs](https://gnews.io/)

### Agent Framework

Microsoft Agent Framework documentation:
- Agent lifecycle and message flow
- Tool registration and invocation
- Response formatting and combination

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run evaluation tests
5. Submit a pull request

## 📝 License

This project is provided as-is for educational purposes.

## 🎓 Learning Resources

### Key Concepts

1. **MCP (Model Context Protocol)**
   - Tool providers and consumers
   - Asynchronous communication
   - Standard tool definitions

2. **Multi-Agent Systems**
   - Agent specialization
   - Query routing
   - Result aggregation

3. **Evaluation Frameworks**
   - Metric definition
   - Dataset creation
   - Report generation

### Referenced Technologies

- [Streamlit](https://streamlit.io/) - Web framework
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) - Agent orchestration
- [MCP Specification](https://modelcontextprotocol.io/) - Protocol standard
- [Open-Meteo](https://open-meteo.com/) - Weather API
- [GNews](https://gnews.io/) - News API

## ❓ Troubleshooting

### Common Issues

**Issue**: "Connection timeout to weather API"
- **Solution**: Check internet connection, API endpoint status

**Issue**: "GNews API returns empty results"
- **Solution**: Try different search terms, check rate limits

**Issue**: "Location not found"
- **Solution**: Use full city names (e.g., "New York" not "NYC")

**Issue**: "Streamlit app won't start"
- **Solution**: `pip install -r requirements.txt`, verify Python 3.8+

### Debug Logging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review evaluation reports for hints
3. Check API status pages
4. Review error logs in console

## 🎉 Acknowledgments

- Open-Meteo for free weather data
- GNews for free news aggregation
- Streamlit for the web framework
- Microsoft for Agent Framework

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Status**: Production Ready
