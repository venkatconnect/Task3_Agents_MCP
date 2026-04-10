# 🌤️📰 Weather & News Agent

**🚀 Live App:** https://weather-agent-orchestrator.streamlit.app/

An intelligent agent-based application that intelligently answers real-time questions about weather and news using Agent Orchestration, MCP servers, and Streamlit.

## 🎯 What It Does

- **Ask**: Questions about weather and news
- **Get**: Real-time intelligent answers from specialized agents
- **See**: Execution details showing how agents work together
- **Evaluate**: 90% accuracy across 5 comprehensive metrics

## 🏗️ Architecture

```
User Query
    ↓
Streamlit Web Interface
    ↓
Orchestrator Agent (Classify & Route)
    ├→ Weather Agent ←→ Open-Meteo API
    └→ News Agent ←→ NewsAPI
    ↓
Combined Response
```

## ✨ Features

| Feature | Details |
|---------|---------|
| **Weather Agent** | Current weather, 7-day forecast, location-based |
| **News Agent** | Search news, category headlines, trending topics |
| **Orchestrator** | Query routing, response coordination |
| **Data Sources** | Open-Meteo (free) + NewsAPI (free tier) |
| **Evaluation** | 5 metrics, 10 test cases, 90% pass rate |

## 🚀 Quick Start

### 1. Local Setup
```bash
git clone <repo-url> && cd Task3_Agents_MCP
pip install -r requirements.txt
echo "NEWSAPI_KEY=your_key_from_newsapi.org" > .env
streamlit run app.py
```

Visit: http://localhost:8501

### 2. Or Use Live App
Visit: https://weather-agent-orchestrator.streamlit.app/

### 3. Try These Queries
- "What's the weather in New York?"
- "Latest technology news"
- "London weather and tech news"

## 📊 Evaluation Results

```
Overall Pass Rate: 90% (9/10 tests)

Metrics:
  ✅ Query Classification: 100%
  ✅ Tool Utilization: 100%
  ✅ Answer Relevance: 90%
  ⚠️ Completeness: 80%
  ⚠️ Data Validity: 80%
```

Run locally: `python evaluation/runner.py`

## 📁 Project Structure

```
Task3_Agents_MCP/
├── app.py                    # Streamlit UI
├── requirements.txt          # Dependencies
├── .env                      # API keys (do not commit)
│
├── mcp_servers/
│   ├── weather_provider.py  # Open-Meteo API
│   └── news_provider.py     # NewsAPI integration
│
├── agent/
│   └── orchestrator.py      # Multi-agent routing
│
└── evaluation/
    ├── dataset.py           # Test cases
    ├── metrics.py           # Evaluation metrics
    ├── runner.py            # Test executor
    └── advanced_metrics.py  # Performance analysis
```

## 🔑 API Keys

- **Open-Meteo**: ✅ Free (no key needed)
- **NewsAPI**: Get free key at https://newsapi.org/register

Add to `.env`:
```
NEWSAPI_KEY=your_api_key_here
```

## 🌐 Deployment

**Live on Streamlit Cloud:**
https://weather-agent-orchestrator.streamlit.app/

**Deploy Yourself:**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add API keys in Secrets tab
4. Done!

## 📚 Technologies

- Python 3.8+ | Streamlit 1.28+ | httpx | Pydantic
- Agent Framework | MCP Protocol | Async/Await

## 🤝 Contributing

Pull requests welcome! Please run `python evaluation/runner.py` before submitting.

## 📄 License

Educational use. See LICENSE for details.

---

**Questions?** Check the live app or open an issue on GitHub!

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Status**: Production Ready
