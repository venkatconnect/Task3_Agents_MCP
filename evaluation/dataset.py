"""
Evaluation Dataset for Weather & News Agent

Contains test cases with expected outputs for evaluating agent performance.
"""

import json
from datetime import datetime

# Evaluation dataset with test cases
EVALUATION_DATASET = [
    {
        "id": "weather_001",
        "query": "What is the current weather in New York?",
        "expected_agent": "weather",
        "expected_fields": ["temperature", "humidity", "weather_condition", "wind_speed"],
        "evaluation_criteria": ["location_accuracy", "data_format", "relevance"],
        "category": "basic_weather"
    },
    {
        "id": "weather_002",
        "query": "Tell me the weather forecast for London",
        "expected_agent": "weather",
        "expected_fields": ["forecast_days", "date", "max_temp", "min_temp"],
        "evaluation_criteria": ["forecast_accuracy", "completeness", "format"],
        "category": "weather_forecast"
    },
    {
        "id": "weather_003",
        "query": "Will it rain in Seattle tomorrow?",
        "expected_agent": "weather",
        "expected_fields": ["precipitation", "weather_condition"],
        "evaluation_criteria": ["precipitation_accuracy", "relevance"],
        "category": "weather_specific"
    },
    {
        "id": "news_001",
        "query": "Tell me the latest technology news",
        "expected_agent": "news",
        "expected_fields": ["title", "description", "source", "url"],
        "evaluation_criteria": ["relevance", "recency", "article_count"],
        "category": "category_news"
    },
    {
        "id": "news_002",
        "query": "What are the top business news headlines?",
        "expected_agent": "news",
        "expected_fields": ["title", "description", "source"],
        "evaluation_criteria": ["category_match", "article_quality"],
        "category": "category_news"
    },
    {
        "id": "news_003",
        "query": "Search for news about artificial intelligence",
        "expected_agent": "news",
        "expected_fields": ["title", "description", "source", "url"],
        "evaluation_criteria": ["keyword_relevance", "article_count"],
        "category": "keyword_search"
    },
    {
        "id": "combined_001",
        "query": "What's the weather in Paris and tell me the latest news?",
        "expected_agent": "combined",
        "expected_fields": ["weather_data", "news_data"],
        "evaluation_criteria": ["both_agents_invoked", "response_completeness"],
        "category": "multi_agent"
    },
    {
        "id": "combined_002",
        "query": "Weather in Tokyo and technology news headlines",
        "expected_agent": "combined",
        "expected_fields": ["temperature", "title", "source"],
        "evaluation_criteria": ["agent_selection", "data_combination"],
        "category": "multi_agent"
    },
    {
        "id": "edge_001",
        "query": "Tell me about sports news",
        "expected_agent": "news",
        "expected_fields": ["title", "description"],
        "evaluation_criteria": ["category_recognition", "relevance"],
        "category": "category_news"
    },
    {
        "id": "edge_002",
        "query": "How's the weather going to be in Berlin next week?",
        "expected_agent": "weather",
        "expected_fields": ["forecast_days"],
        "evaluation_criteria": ["intent_understanding", "forecast_generation"],
        "category": "weather_forecast"
    }
]


def get_evaluation_dataset():
    """
    Get the evaluation dataset
    
    Returns:
        List of test cases for evaluation
    """
    return EVALUATION_DATASET


def save_evaluation_dataset(filepath: str):
    """
    Save evaluation dataset to JSON file
    
    Args:
        filepath: Path to save the dataset
    """
    with open(filepath, 'w') as f:
        json.dump(EVALUATION_DATASET, f, indent=2)


def load_evaluation_dataset(filepath: str):
    """
    Load evaluation dataset from JSON file
    
    Args:
        filepath: Path to load the dataset from
        
    Returns:
        List of test cases
    """
    with open(filepath, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    # Display dataset statistics
    dataset = get_evaluation_dataset()
    
    print("📊 Evaluation Dataset Statistics")
    print(f"Total test cases: {len(dataset)}")
    
    # Count by category
    categories = {}
    agent_types = {}
    
    for test in dataset:
        cat = test.get("category")
        if cat not in categories:
            categories[cat] = 0
        categories[cat] += 1
        
        agent = test.get("expected_agent")
        if agent not in agent_types:
            agent_types[agent] = 0
        agent_types[agent] += 1
    
    print("\nBy Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print("\nBy Agent Type:")
    for agent, count in sorted(agent_types.items()):
        print(f"  {agent}: {count}")
    
    # Save to file
    import os
    dataset_file = os.path.join(os.path.dirname(__file__), "evaluation_dataset.json")
    save_evaluation_dataset(dataset_file)
    print(f"\n✅ Dataset saved to {dataset_file}")
