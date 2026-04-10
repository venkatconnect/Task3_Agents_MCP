"""
Evaluation Example and Test Harness

Demonstrates evaluation capabilities with example data and pre-computed results
for documentation and testing purposes.
"""

import json
from datetime import datetime
from typing import Dict, Any

# Example evaluation results for documentation
EXAMPLE_EVALUATION_RESULTS = {
    "timestamp": "2026-04-09T12:00:00",
    "total_tests": 10,
    "completed_tests": 10,
    "failed_tests": 0,
    "summary": {
        "overall_pass_rate": 0.90,
        "overall_average_score": 0.88,
        "by_metric_type": {
            "classification": {
                "passed": 10,
                "total": 10,
                "pass_rate": 1.0,
                "average_score": 1.00
            },
            "completeness": {
                "passed": 8,
                "total": 10,
                "pass_rate": 0.8,
                "average_score": 0.85
            },
            "relevance": {
                "passed": 9,
                "total": 10,
                "pass_rate": 0.9,
                "average_score": 0.91
            },
            "tool_usage": {
                "passed": 10,
                "total": 10,
                "pass_rate": 1.0,
                "average_score": 1.00
            },
            "data_validity": {
                "passed": 8,
                "total": 10,
                "pass_rate": 0.8,
                "average_score": 0.82
            }
        },
        "by_category": {
            "basic_weather": {
                "passed": 1,
                "total": 1
            },
            "weather_forecast": {
                "passed": 2,
                "total": 2
            },
            "weather_specific": {
                "passed": 1,
                "total": 1
            },
            "category_news": {
                "passed": 3,
                "total": 3
            },
            "keyword_search": {
                "passed": 1,
                "total": 1
            },
            "multi_agent": {
                "passed": 2,
                "total": 2
            }
        }
    },
    "results": [
        {
            "test_id": "weather_001",
            "query": "What is the current weather in New York?",
            "category": "basic_weather",
            "expected_agent": "weather",
            "actual_agent": "weather",
            "metrics": [
                {"type": "classification", "passed": True, "score": 1.0, "details": "Expected 'weather', got 'weather'"},
                {"type": "completeness", "passed": True, "score": 1.0, "details": "Found 5/5 expected fields"},
                {"type": "relevance", "passed": True, "score": 0.95, "details": "Matched 4/4 query keywords"},
                {"type": "tool_usage", "passed": True, "score": 1.0, "details": "Called: get_current_weather"},
                {"type": "data_validity", "passed": True, "score": 0.9, "details": "Validity issues: 0"}
            ],
            "response_preview": "🌤️ **Weather in New York** Temperature: 68°F (feels like 66°F)..."
        },
        {
            "test_id": "weather_002",
            "query": "Tell me the weather forecast for London",
            "category": "weather_forecast",
            "expected_agent": "weather",
            "actual_agent": "weather",
            "metrics": [
                {"type": "classification", "passed": True, "score": 1.0, "details": "Expected 'weather', got 'weather'"},
                {"type": "completeness", "passed": True, "score": 1.0, "details": "Found 4/4 expected fields"},
                {"type": "relevance", "passed": True, "score": 0.92, "details": "Matched 4/4 query keywords"},
                {"type": "tool_usage", "passed": True, "score": 1.0, "details": "Called: get_weather_forecast"},
                {"type": "data_validity", "passed": True, "score": 0.88, "details": "Validity issues: 0"}
            ],
            "response_preview": "📅 **7-Day Forecast for London** **2026-04-09**..."
        },
        {
            "test_id": "news_001",
            "query": "Tell me the latest technology news",
            "category": "category_news",
            "expected_agent": "news",
            "actual_agent": "news",
            "metrics": [
                {"type": "classification", "passed": True, "score": 1.0, "details": "Expected 'news', got 'news'"},
                {"type": "completeness", "passed": False, "score": 0.75, "details": "Found 3/4 expected fields"},
                {"type": "relevance", "passed": True, "score": 0.88, "details": "Matched 3/3 query keywords"},
                {"type": "tool_usage", "passed": True, "score": 1.0, "details": "Called: get_top_headlines"},
                {"type": "data_validity", "passed": False, "score": 0.75, "details": "Validity issues: 1"}
            ],
            "response_preview": "📰 **Top technology News** 1. AI Breakthrough in Natural Language..."
        },
        {
            "test_id": "combined_001",
            "query": "What's the weather in Paris and tell me the latest news?",
            "category": "multi_agent",
            "expected_agent": "combined",
            "actual_agent": "combined",
            "metrics": [
                {"type": "classification", "passed": True, "score": 1.0, "details": "Expected 'combined', got 'combined'"},
                {"type": "completeness", "passed": True, "score": 1.0, "details": "Found 6/6 expected fields"},
                {"type": "relevance", "passed": True, "score": 0.89, "details": "Matched 5/5 query keywords"},
                {"type": "tool_usage", "passed": True, "score": 1.0, "details": "Called: get_current_weather, search_news"},
                {"type": "data_validity", "passed": True, "score": 0.85, "details": "Validity issues: 0"}
            ],
            "response_preview": "🤖 **Combined Report** Agent 1: weather 🌤️ **Weather in Paris**..."
        }
    ]
}


def get_example_results() -> Dict[str, Any]:
    """Get example evaluation results"""
    return EXAMPLE_EVALUATION_RESULTS


def save_example_results(filepath: str):
    """Save example results to file"""
    with open(filepath, 'w') as f:
        json.dump(EXAMPLE_EVALUATION_RESULTS, f, indent=2)


def load_evaluation_results(filepath: str) -> Dict[str, Any]:
    """Load evaluation results from file"""
    with open(filepath, 'r') as f:
        return json.load(f)


def format_results_for_markdown(results: Dict[str, Any]) -> str:
    """Format evaluation results as Markdown"""
    
    summary = results.get("summary", {})
    pass_rate = summary.get("overall_pass_rate", 0)
    avg_score = summary.get("overall_average_score", 0)
    
    markdown = f"""# Evaluation Results

**Timestamp**: {results.get('timestamp')}

## Summary

- **Total Tests**: {results.get('total_tests')}
- **Completed**: {results.get('completed_tests')}
- **Failed**: {results.get('failed_tests')}
- **Overall Pass Rate**: {pass_rate:.1%}
- **Overall Average Score**: {avg_score:.2f}/1.0

## Metrics Performance

| Metric Type | Passed | Total | Pass Rate | Avg Score |
|---|---|---|---|---|
"""
    
    for metric, stats in summary.get("by_metric_type", {}).items():
        markdown += (
            f"| {metric} | {stats['passed']} | {stats['total']} | "
            f"{stats['pass_rate']:.1%} | {stats['average_score']:.2f} |\n"
        )
    
    markdown += "\n## Category Results\n\n"
    markdown += "| Category | Passed | Total | Pass Rate |\n"
    markdown += "|---|---|---|---|\n"
    
    for category, stats in summary.get("by_category", {}).items():
        rate = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
        markdown += f"| {category} | {stats['passed']} | {stats['total']} | {rate:.1%} |\n"
    
    return markdown


if __name__ == "__main__":
    # Display example results
    results = get_example_results()
    
    print("📊 Example Evaluation Results")
    print("=" * 60)
    print(f"Timestamp: {results['timestamp']}")
    print(f"Total Tests: {results['total_tests']}")
    print(f"Pass Rate: {results['summary']['overall_pass_rate']:.1%}")
    print(f"Average Score: {results['summary']['overall_average_score']:.2f}/1.0")
    
    print("\n📈 Metric Performance:")
    for metric, stats in results['summary']['by_metric_type'].items():
        print(
            f"  {metric}: {stats['passed']}/{stats['total']} "
            f"({stats['pass_rate']:.1%}) - Score: {stats['average_score']:.2f}"
        )
    
    # Generate markdown
    markdown = format_results_for_markdown(results)
    print("\n" + markdown)
