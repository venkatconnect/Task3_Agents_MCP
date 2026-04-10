"""
Evaluation Metrics for Weather & News Agent

Defines metrics to evaluate agent performance:
1. Query Classification Accuracy: Does agent classify query correctly?
2. Response Completeness: Does response include all expected fields?
3. Tool Utilization: Were appropriate tools called?
4. Answer Relevance: Do results match the user's intent?
5. Data Accuracy: Is the data valid and properly formatted?
"""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics for evaluation"""
    CLASSIFICATION = "classification"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"
    TOOL_USAGE = "tool_usage"
    DATA_VALIDITY = "data_validity"
    RESPONSE_FORMAT = "response_format"


@dataclass
class MetricResult:
    """Result of a single metric evaluation"""
    metric_type: MetricType
    test_id: str
    passed: bool
    score: float  # 0.0 to 1.0
    details: str
    error: Optional[str] = None


class QueryClassificationMetric:
    """
    Metric: Does the agent correctly classify the query type?
    
    Evaluates:
    - Weather queries classified as 'weather'
    - News queries classified as 'news'
    - Combined queries classified as 'combined'
    """
    
    def __init__(self):
        self.name = "Query Classification Accuracy"
        self.description = "Evaluates if the agent correctly classifies query type"
    
    def evaluate(
        self,
        test_id: str,
        actual_query_type: str,
        expected_query_type: str
    ) -> MetricResult:
        """
        Evaluate query classification
        
        Args:
            test_id: ID of the test case
            actual_query_type: Agent's classification
            expected_query_type: Expected classification
            
        Returns:
            MetricResult with evaluation outcome
        """
        passed = actual_query_type.lower() == expected_query_type.lower()
        score = 1.0 if passed else 0.0
        
        details = f"Expected '{expected_query_type}', got '{actual_query_type}'"
        
        return MetricResult(
            metric_type=MetricType.CLASSIFICATION,
            test_id=test_id,
            passed=passed,
            score=score,
            details=details
        )


class ResponseCompletenessMetric:
    """
    Metric: Does the response include all expected fields?
    
    Evaluates:
    - Weather responses include temperature, humidity, wind_speed, etc.
    - News responses include title, description, source, url
    """
    
    def __init__(self):
        self.name = "Response Completeness"
        self.description = "Checks if response includes all expected fields"
    
    def evaluate(
        self,
        test_id: str,
        response_data: Dict[str, Any],
        expected_fields: List[str]
    ) -> MetricResult:
        """
        Evaluate response completeness
        
        Args:
            test_id: ID of the test case
            response_data: The actual response data
            expected_fields: List of expected fields
            
        Returns:
            MetricResult with evaluation outcome
        """
        # Check if all expected fields are present
        agent_responses = response_data.get("responses", [])
        
        if not agent_responses:
            return MetricResult(
                metric_type=MetricType.COMPLETENESS,
                test_id=test_id,
                passed=False,
                score=0.0,
                details="No agent responses found",
                error="Empty response"
            )
        
        # Flatten all data from all agent responses
        all_results = {}
        for resp in agent_responses:
            exec_results = resp.get("execution_results", {})
            if isinstance(exec_results, dict):
                all_results.update(exec_results)
        
        # Check for expected fields
        found_fields = 0
        for field in expected_fields:
            if self._field_exists(field, all_results):
                found_fields += 1
        
        score = found_fields / len(expected_fields) if expected_fields else 0.0
        passed = score >= 0.8  # At least 80% of fields present
        
        details = f"Found {found_fields}/{len(expected_fields)} expected fields"
        
        return MetricResult(
            metric_type=MetricType.COMPLETENESS,
            test_id=test_id,
            passed=passed,
            score=score,
            details=details
        )
    
    def _field_exists(self, field: str, data: Dict) -> bool:
        """Check if a field exists in nested data"""
        if not isinstance(data, dict):
            return False
        
        # Check direct keys
        if field in data:
            return True
        
        # Check nested objects
        for key, value in data.items():
            if isinstance(value, dict) and self._field_exists(field, value):
                return True
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    if self._field_exists(field, value[0]):
                        return True
        
        return False


class AnswerRelevanceMetric:
    """
    Metric: Is the answer relevant to the user's query?
    
    Evaluates:
    - Query keywords present in response
    - Location/topic mentioned in response matches query
    - Response doesn't contain irrelevant information
    """
    
    def __init__(self):
        self.name = "Answer Relevance"
        self.description = "Evaluates if answer is relevant to the query"
    
    def evaluate(
        self,
        test_id: str,
        user_query: str,
        response_message: str
    ) -> MetricResult:
        """
        Evaluate answer relevance
        
        Args:
            test_id: ID of the test case
            user_query: Original user query
            response_message: Agent's response message
            
        Returns:
            MetricResult with evaluation outcome
        """
        # Extract key terms from query
        keywords = self._extract_keywords(user_query)
        
        # Check how many keywords appear in response
        response_lower = response_message.lower()
        matched_keywords = 0
        
        for keyword in keywords:
            if keyword.lower() in response_lower:
                matched_keywords += 1
        
        if not keywords:
            score = 0.5  # Neutral score if no keywords
        else:
            score = matched_keywords / len(keywords)
        
        passed = score >= 0.5  # At least 50% keyword match
        
        details = f"Matched {matched_keywords}/{len(keywords)} query keywords"
        
        return MetricResult(
            metric_type=MetricType.RELEVANCE,
            test_id=test_id,
            passed=passed,
            score=score,
            details=details
        )
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract meaningful keywords from query"""
        # Remove common words
        stop_words = {
            "what", "where", "when", "why", "how", "is", "the", "a", "an",
            "and", "or", "tell", "me", "get", "give", "show", "about", "of"
        }
        
        words = [w for w in query.lower().split() if w not in stop_words and len(w) > 2]
        return words


class ToolUtilizationMetric:
    """
    Metric: Were appropriate tools called for the query?
    
    Evaluates:
    - Weather queries use weather tools
    - News queries use news tools
    - Combined queries use both tool types
    """
    
    def __init__(self):
        self.name = "Tool Utilization"
        self.description = "Checks if appropriate tools were called"
    
    def evaluate(
        self,
        test_id: str,
        query_type: str,
        tool_calls: List[Dict[str, Any]]
    ) -> MetricResult:
        """
        Evaluate tool utilization
        
        Args:
            test_id: ID of the test case
            query_type: Type of query (weather, news, combined)
            tool_calls: List of tool calls made
            
        Returns:
            MetricResult with evaluation outcome
        """
        if not tool_calls:
            return MetricResult(
                metric_type=MetricType.TOOL_USAGE,
                test_id=test_id,
                passed=False,
                score=0.0,
                details="No tools were called",
                error="Empty tool calls"
            )
        
        # Get tool names called
        called_tools = [call.get("tool_name", "") for call in tool_calls]
        
        weather_tools = {"get_current_weather", "get_weather_forecast"}
        news_tools = {"search_news", "get_top_headlines"}
        
        has_weather = any(tool in weather_tools for tool in called_tools)
        has_news = any(tool in news_tools for tool in called_tools)
        
        # Check if appropriate tools were used
        if query_type == "weather":
            passed = has_weather and not has_news
            score = 1.0 if passed else 0.5
        elif query_type == "news":
            passed = has_news and not has_weather
            score = 1.0 if passed else 0.5
        elif query_type == "combined":
            passed = has_weather and has_news
            score = 1.0 if passed else 0.5
        else:
            score = 0.5
            passed = False
        
        details = f"Called: {', '.join(called_tools)}"
        
        return MetricResult(
            metric_type=MetricType.TOOL_USAGE,
            test_id=test_id,
            passed=passed,
            score=score,
            details=details
        )


class DataValidityMetric:
    """
    Metric: Is the returned data valid and well-formatted?
    
    Evaluates:
    - Response follows expected schema
    - No null/empty required fields
    - Data types are correct
    """
    
    def __init__(self):
        self.name = "Data Validity"
        self.description = "Validates data format and structure"
    
    def evaluate(
        self,
        test_id: str,
        execution_results: Dict[str, Any]
    ) -> MetricResult:
        """
        Evaluate data validity
        
        Args:
            test_id: ID of the test case
            execution_results: Raw execution results from agent
            
        Returns:
            MetricResult with evaluation outcome
        """
        if not execution_results:
            return MetricResult(
                metric_type=MetricType.DATA_VALIDITY,
                test_id=test_id,
                passed=False,
                score=0.0,
                details="No execution results",
                error="Empty results"
            )
        
        # Validate basic structure
        issues = []
        
        # Check for required top-level keys
        if "weather" in execution_results:
            weather = execution_results["weather"]
            required_fields = ["location", "temperature", "humidity", "weather_condition"]
            for field in required_fields:
                if field not in weather or weather[field] is None:
                    issues.append(f"Missing or null weather field: {field}")
        
        if "news" in execution_results:
            news = execution_results["news"]
            if "articles" in news and news["articles"]:
                article = news["articles"][0]
                required_fields = ["title", "source", "url"]
                for field in required_fields:
                    if field not in article:
                        issues.append(f"Missing news field: {field}")
        
        if "forecast" in execution_results:
            forecast = execution_results["forecast"]
            if "forecast_days" not in forecast or not forecast["forecast_days"]:
                issues.append("Empty or missing forecast days")
        
        score = 1.0 - (len(issues) * 0.15)  # Deduct 15% per issue
        score = max(0.0, min(1.0, score))  # Clamp between 0 and 1
        passed = score >= 0.8
        
        details = f"Validity issues: {len(issues)}"
        error = "; ".join(issues) if issues else None
        
        return MetricResult(
            metric_type=MetricType.DATA_VALIDITY,
            test_id=test_id,
            passed=passed,
            score=score,
            details=details,
            error=error
        )


class EvaluationMetrics:
    """Collection of all evaluation metrics"""
    
    def __init__(self):
        self.metrics = [
            QueryClassificationMetric(),
            ResponseCompletenessMetric(),
            AnswerRelevanceMetric(),
            ToolUtilizationMetric(),
            DataValidityMetric()
        ]
    
    def evaluate_all(
        self,
        test_id: str,
        user_query: str,
        agent_response: Dict[str, Any],
        expected_fields: List[str],
        expected_agent: str
    ) -> List[MetricResult]:
        """
        Run all evaluation metrics for a test case
        
        Args:
            test_id: ID of the test case
            user_query: Original user query
            agent_response: Response from the agent
            expected_fields: Expected fields in response
            expected_agent: Expected agent type
            
        Returns:
            List of MetricResult objects
        """
        results = []
        
        # Get actual data
        actual_agent = agent_response.get("query_type", "unknown")
        message = agent_response.get("message", "")
        responses = agent_response.get("responses", [])
        
        # Extract all tool calls
        all_tools = []
        execution_results = {}
        for resp in responses:
            all_tools.extend(resp.get("tool_calls", []))
            execution_results.update(resp.get("execution_results", {}))
        
        # 1. Query Classification
        classification_result = self.metrics[0].evaluate(
            test_id, actual_agent, expected_agent
        )
        results.append(classification_result)
        
        # 2. Response Completeness
        completeness_result = self.metrics[1].evaluate(
            test_id, agent_response, expected_fields
        )
        results.append(completeness_result)
        
        # 3. Answer Relevance
        relevance_result = self.metrics[2].evaluate(
            test_id, user_query, message
        )
        results.append(relevance_result)
        
        # 4. Tool Utilization
        tool_result = self.metrics[3].evaluate(
            test_id, actual_agent, all_tools
        )
        results.append(tool_result)
        
        # 5. Data Validity
        validity_result = self.metrics[4].evaluate(
            test_id, execution_results
        )
        results.append(validity_result)
        
        return results
    
    def calculate_summary(self, all_results: List[MetricResult]) -> Dict[str, Any]:
        """
        Calculate summary statistics from all metric results
        
        Args:
            all_results: List of all metric results from all tests
            
        Returns:
            Dictionary with summary statistics
        """
        if not all_results:
            return {}
        
        # Group by metric type
        by_metric = {}
        for result in all_results:
            metric_name = result.metric_type.value
            if metric_name not in by_metric:
                by_metric[metric_name] = []
            by_metric[metric_name].append(result)
        
        # Calculate statistics
        summary = {
            "total_tests": len(set(r.test_id for r in all_results)),
            "total_evaluations": len(all_results),
            "overall_pass_rate": sum(1 for r in all_results if r.passed) / len(all_results) if all_results else 0,
            "overall_score": sum(r.score for r in all_results) / len(all_results) if all_results else 0,
            "by_metric": {}
        }
        
        for metric_name, results in by_metric.items():
            passed = sum(1 for r in results if r.passed)
            total = len(results)
            avg_score = sum(r.score for r in results) / total if results else 0
            
            summary["by_metric"][metric_name] = {
                "passed": passed,
                "total": total,
                "pass_rate": passed / total if total > 0 else 0,
                "average_score": avg_score
            }
        
        return summary


if __name__ == "__main__":
    # Display metric information
    metrics = EvaluationMetrics()
    
    print("📊 Evaluation Metrics")
    print(f"Total metrics: {len(metrics.metrics)}\n")
    
    for metric in metrics.metrics:
        print(f"📈 {metric.name}")
        print(f"   {metric.description}\n")
