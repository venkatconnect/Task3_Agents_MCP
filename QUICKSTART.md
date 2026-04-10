# Quick Start Guide

## ⚡ 5-Minute Setup

### 1. Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App (1 min)
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Try It Out (3 min)
Ask your first questions:

**Weather Query:**
```
What's the weather in New York?
```

**News Query:**
```
Tell me the latest technology news
```

**Combined Query:**
```
Weather in London and top business news headlines
```

---

## 🎯 Main Features

### 🌤️ Weather Agent
- Get current conditions for any location
- 7-day weather forecasts
- Real-time data via Open-Meteo API
- Temperature, humidity, wind, precipitation

### 📰 News Agent
- Search news by keyword
- Headlines by category
- Latest articles from multiple sources
- Real-time news via GNews API

### 🤖 Agent Orchestrator
- Intelligent query classification
- Automatic routing to appropriate agents
- Result combination and formatting
- Multi-agent coordination

---

## 🧪 Run Evaluation

```bash
# Run full evaluation suite
python evaluation/runner.py

# View example results
python evaluation/example_results.py

# Analyze metrics
python evaluation/advanced_metrics.py
```

### Expected Results
```
Overall Pass Rate: 90%
Overall Average Score: 0.88/1.0

Metrics Breakdown:
- Classification: 100% ✓
- Tool Usage: 100% ✓
- Relevance: 90% ✓
- Completeness: 80% ⚠
- Data Validity: 80% ⚠
```

---

## 📁 Project Structure

```
Task3_Agents_MCP/
├── app.py                 # Streamlit UI - START HERE!
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── PULL_REQUEST.md       # PR details with evaluation results
│
├── agent/                # Agent implementation
│   └── orchestrator.py   # Multi-agent orchestrator
│
├── mcp_servers/          # Data providers
│   ├── weather_provider.py
│   └── news_provider.py
│
└── evaluation/           # Evaluation framework
    ├── runner.py        # Evaluation executor
    ├── metrics.py       # 5 evaluation metrics
    ├── dataset.py       # 10 test cases
    ├── advanced_metrics.py
    └── example_results.py
```

---

## 🚀 Python Requirements

- **Python 3.8+**
- **pip** (package manager)
- **Internet connection** (for API access)

## 🎓 Learning Path

1. **Start**: Run the Streamlit app and try some queries
2. **Explore**: Read the README.md for architecture details
3. **Evaluate**: Run the evaluation framework to see metrics
4. **Review**: Check PULL_REQUEST.md for technical details
5. **Enhance**: Create your own agents or metrics!

---

## 💡 Example Queries

### Weather
- "What's the weather in New York?"
- "Tell me the forecast for Paris"
- "Will it rain in Seattle?"
- "How hot is Bangkok?"

### News
- "Latest AI news"
- "Top technology headlines"
- "Business news today"
- "Entertainment news"

### Combined
- "New York weather and AI news"
- "London forecast and sports headlines"
- "Berlin weather next week plus business news"

---

## 🔧 Troubleshooting

**Issue**: App won't start
- Solution: `pip install -r requirements.txt`

**Issue**: Location not recognized
- Solution: Use full city names (e.g., "New York" not "NYC")

**Issue**: No internet connection
- Solution: APIs require internet access for live data

**Issue**: Slow responses
- Solution: First request may be slower; subsequent ones are faster

---

## 📊 Evaluation Metrics Explained

### 1. **Classification Accuracy** (100%)
Does the agent correctly identify query type? ✓ Perfect!

### 2. **Tool Utilization** (100%)
Are the right tools called? ✓ Perfect!

### 3. **Answer Relevance** (90%)
Does the answer match the question? ✓ Very good!

### 4. **Completeness** (80%)
Are all expected fields included? ⚠ Good

### 5. **Data Validity** (80%)
Is the data valid and well-formatted? ⚠ Good

---

## 📚 Next Steps

1. ✅ **Quick Start**: Run the app (done!)
2. 🔄 **Evaluate**: Run evaluation suite
3. 📖 **Learn**: Read full README.md
4. 🛠️ **Customize**: Modify agents or add new providers
5. 🚀 **Deploy**: Deploy to Streamlit Cloud or Docker

---

## 🤝 Need Help?

1. Check the README.md for detailed documentation
2. Review PULL_REQUEST.md for technical details
3. Look at evaluation examples in `evaluation/example_results.py`
4. Run evaluation to understand metrics better

---

**Ready? Run this command:**
```bash
streamlit run app.py
```

Then ask: "What's the weather in New York?"

Let the magic happen! ✨
