"""
Advanced Metrics Analysis for Agent Evaluation

Provides detailed analysis and visualization of agent performance metrics
including trend analysis, comparative metrics, and performance insights.
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import statistics


@dataclass
class PerformanceInsight:
    """Represents a performance insight"""
    title: str
    description: str
    value: Any
    recommendation: Optional[str] = None
    severity: Optional[str] = None  # "critical", "warning", "info"


class AdvancedMetricsAnalyzer:
    """
    Advanced analysis of agent evaluation metrics
    
    Provides:
    - Trend analysis (performance over time)
    - Comparative metrics (metric vs metric)
    - Performance insights and recommendations
    - Statistical analysis
    """
    
    def __init__(self):
        self.name = "Advanced Metrics Analyzer"
    
    def analyze_metric_distribution(
        self,
        metric_scores: List[float]
    ) -> Dict[str, Any]:
        """
        Analyze distribution of metric scores
        
        Args:
            metric_scores: List of metric scores
            
        Returns:
            Dictionary with distribution statistics
        """
        if not metric_scores:
            return {}
        
        return {
            "count": len(metric_scores),
            "mean": statistics.mean(metric_scores),
            "median": statistics.median(metric_scores),
            "stdev": statistics.stdev(metric_scores) if len(metric_scores) > 1 else 0,
            "min": min(metric_scores),
            "max": max(metric_scores),
            "variance": statistics.variance(metric_scores) if len(metric_scores) > 1 else 0,
            "quartiles": {
                "q1": self._percentile(metric_scores, 25),
                "q2": self._percentile(metric_scores, 50),
                "q3": self._percentile(metric_scores, 75)
            }
        }
    
    def identify_bottlenecks(
        self,
        summary: Dict[str, Any]
    ) -> List[PerformanceInsight]:
        """
        Identify performance bottlenecks and weak areas
        
        Args:
            summary: Summary statistics from evaluation
            
        Returns:
            List of performance insights with recommendations
        """
        insights = []
        
        # Check overall pass rate
        overall_pass_rate = summary.get("overall_pass_rate", 0)
        
        if overall_pass_rate < 0.7:
            insights.append(PerformanceInsight(
                title="Low Overall Pass Rate",
                description=f"Current pass rate is {overall_pass_rate:.1%}",
                value=overall_pass_rate,
                severity="critical",
                recommendation="Review agent logic and expected values"
            ))
        elif overall_pass_rate < 0.85:
            insights.append(PerformanceInsight(
                title="Moderate Pass Rate",
                description=f"Pass rate is {overall_pass_rate:.1%}, target is 90%+",
                value=overall_pass_rate,
                severity="warning",
                recommendation="Focus on improving weakest metrics"
            ))
        else:
            # Good performance - provide positive insight
            insights.append(PerformanceInsight(
                title="Strong Overall Performance",
                description=f"Pass rate is {overall_pass_rate:.1%} - Exceeds target!",
                value=overall_pass_rate,
                severity="info",
                recommendation="Monitor metrics and focus on edge cases"
            ))
        
        # Check individual metrics
        by_metric = summary.get("by_metric_type", {})
        
        for metric_type, stats in by_metric.items():
            pass_rate = stats.get("pass_rate", 0)
            avg_score = stats.get("average_score", 0)
            
            if pass_rate < 0.8:
                insights.append(PerformanceInsight(
                    title=f"Low {metric_type.replace('_', ' ').title()} Pass Rate",
                    description=f"{metric_type} has {pass_rate:.1%} pass rate",
                    value=pass_rate,
                    severity="warning" if pass_rate > 0.5 else "critical",
                    recommendation=f"Debug {metric_type} implementation and test cases"
                ))
            elif pass_rate == 1.0:
                # Perfect score - highlight
                insights.append(PerformanceInsight(
                    title=f"Perfect {metric_type.replace('_', ' ').title()} Score",
                    description=f"{metric_type} achieved 100% pass rate",
                    value=pass_rate,
                    severity="info",
                    recommendation=f"Maintain {metric_type} quality; good model"
                ))
            else:
                # Good but not perfect - highlight for improvement
                insights.append(PerformanceInsight(
                    title=f"Good {metric_type.replace('_', ' ').title()} Performance",
                    description=f"{metric_type} has {pass_rate:.1%} pass rate ({stats.get('passed')}/{stats.get('total')} tests)",
                    value=pass_rate,
                    severity="info",
                    recommendation=f"Minor improvements needed for {metric_type}"
                ))
            
            if avg_score < 0.8:
                insights.append(PerformanceInsight(
                    title=f"Low {metric_type} Average Score",
                    description=f"Average score: {avg_score:.2f}/1.0",
                    value=avg_score,
                    severity="info",
                    recommendation=f"Focus improvement efforts on {metric_type}"
                ))
        
        return insights
    
    def compare_metrics(
        self,
        summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comparative metrics analysis
        
        Args:
            summary: Summary statistics
            
        Returns:
            Dictionary with comparative analysis
        """
        by_metric = summary.get("by_metric_type", {})
        
        if not by_metric:
            return {}
        
        # Find best and worst performers by pass rate
        metric_pass_rates = {
            name: stats.get("pass_rate", 0)
            for name, stats in by_metric.items()
        }
        
        best_metric = max(metric_pass_rates, key=metric_pass_rates.get)
        worst_metric = min(metric_pass_rates, key=metric_pass_rates.get)
        
        # Find best and worst categories
        by_category = summary.get("by_category", {})
        category_rates = {
            name: stats.get("passed", 0) / stats.get("total", 1)
            for name, stats in by_category.items()
        }
        
        return {
            "best_performing_metric": {
                "name": best_metric,
                "pass_rate": metric_pass_rates[best_metric]
            },
            "worst_performing_metric": {
                "name": worst_metric,
                "pass_rate": metric_pass_rates[worst_metric]
            },
            "best_performing_category": {
                "name": max(category_rates, key=category_rates.get) if category_rates else None,
                "pass_rate": max(category_rates.values()) if category_rates else 0
            },
            "worst_performing_category": {
                "name": min(category_rates, key=category_rates.get) if category_rates else None,
                "pass_rate": min(category_rates.values()) if category_rates else 0
            },
            "metric_spread": max(metric_pass_rates.values()) - min(metric_pass_rates.values()) if metric_pass_rates else 0
        }
    
    def generate_trend_analysis(
        self,
        previous_summary: Optional[Dict[str, Any]],
        current_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate trend analysis comparing previous and current runs
        
        Args:
            previous_summary: Previous evaluation summary (optional)
            current_summary: Current evaluation summary
            
        Returns:
            Dictionary with trend analysis
        """
        if not previous_summary:
            return {"trend": "initial_run", "message": "No previous data for comparison"}
        
        prev_pass_rate = previous_summary.get("overall_pass_rate", 0)
        curr_pass_rate = current_summary.get("overall_pass_rate", 0)
        
        change = curr_pass_rate - prev_pass_rate
        direction = "improved" if change > 0 else "declined" if change < 0 else "stable"
        
        return {
            "trend": direction,
            "previous_pass_rate": prev_pass_rate,
            "current_pass_rate": curr_pass_rate,
            "change": change,
            "change_percentage": (change / prev_pass_rate * 100) if prev_pass_rate > 0 else 0,
            "message": f"Performance {direction} by {abs(change):.1%}"
        }
    
    def generate_recommendations(
        self,
        insights: List[PerformanceInsight]
    ) -> List[str]:
        """
        Generate actionable recommendations based on insights
        
        Args:
            insights: List of performance insights
            
        Returns:
            List of prioritized recommendations
        """
        recommendations = []
        
        # Prioritize by severity
        critical = [i for i in insights if i.severity == "critical"]
        warnings = [i for i in insights if i.severity == "warning"]
        info = [i for i in insights if i.severity == "info"]
        
        for insight_list in [critical, warnings, info]:
            for insight in insight_list:
                if insight.recommendation:
                    recommendations.append(insight.recommendation)
        
        return recommendations
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index % 1 == 0:
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index % 1)
    
    def export_insights_report(
        self,
        insights: List[PerformanceInsight],
        recommendations: List[str],
        filepath: str
    ):
        """
        Export insights and recommendations to file
        
        Args:
            insights: List of insights
            recommendations: List of recommendations
            filepath: Path to save report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "insights": [
                {
                    "title": i.title,
                    "description": i.description,
                    "value": str(i.value),
                    "severity": i.severity,
                    "recommendation": i.recommendation
                }
                for i in insights
            ],
            "recommendations": recommendations
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    # Example usage
    analyzer = AdvancedMetricsAnalyzer()
    
    # Example summary
    example_summary = {
        "overall_pass_rate": 0.90,
        "overall_average_score": 0.88,
        "by_metric_type": {
            "classification": {
                "passed": 10,
                "total": 10,
                "pass_rate": 1.0,
                "average_score": 1.0
            },
            "tool_usage": {
                "passed": 10,
                "total": 10,
                "pass_rate": 1.0,
                "average_score": 1.0
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
            "data_validity": {
                "passed": 8,
                "total": 10,
                "pass_rate": 0.8,
                "average_score": 0.82
            }
        },
        "by_category": {
            "basic_weather": {"passed": 1, "total": 1},
            "weather_forecast": {"passed": 2, "total": 2},
            "category_news": {"passed": 3, "total": 3},
            "keyword_search": {"passed": 1, "total": 1},
            "multi_agent": {"passed": 2, "total": 2},
            "edge_cases": {"passed": 1, "total": 1}
        }
    }
    
    # Generate insights
    insights = analyzer.identify_bottlenecks(example_summary)
    recommendations = analyzer.generate_recommendations(insights)
    comparison = analyzer.compare_metrics(example_summary)
    
    # Metric scores for distribution analysis
    all_scores = []
    for metric_data in example_summary.get("by_metric_type", {}).values():
        all_scores.append(metric_data.get("average_score", 0))
    distribution = analyzer.analyze_metric_distribution(all_scores)
    
    print("\n" + "=" * 70)
    print("📊 ADVANCED METRICS ANALYSIS REPORT")
    print("=" * 70)
    
    print(f"\n🎯 OVERALL PERFORMANCE")
    print(f"   Pass Rate: {example_summary['overall_pass_rate']:.1%} ({int(example_summary['overall_pass_rate']*50)}/50)")
    print(f"   Average Score: {example_summary['overall_average_score']:.2f}/1.0")
    
    print(f"\n📈 SCORE DISTRIBUTION")
    if distribution:
        print(f"   Mean: {distribution.get('mean', 0):.2f}")
        print(f"   Median: {distribution.get('median', 0):.2f}")
        print(f"   Std Dev: {distribution.get('stdev', 0):.2f}")
        print(f"   Range: {distribution.get('min', 0):.2f} - {distribution.get('max', 0):.2f}")
    
    print(f"\n💡 KEY INSIGHTS ({len(insights)})")
    for i, insight in enumerate(insights, 1):
        severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(insight.severity, "⚪")
        print(f"\n   {i}. {severity_icon} {insight.title}")
        print(f"      {insight.description}")
        if insight.recommendation:
            print(f"      → {insight.recommendation}")
    
    print(f"\n✅ RECOMMENDATIONS ({len(recommendations)})")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🔄 COMPARATIVE ANALYSIS")
    if comparison:
        best = comparison.get('best_performing_metric', {})
        worst = comparison.get('worst_performing_metric', {})
        print(f"   ⭐ Best: {best.get('name', 'N/A')} ({best.get('pass_rate', 0):.1%})")
        print(f"   ⚠️  Needs Work: {worst.get('name', 'N/A')} ({worst.get('pass_rate', 0):.1%})")
    
    print(f"\n📂 BY CATEGORY")
    for category, stats in example_summary.get("by_category", {}).items():
        cat_name = category.replace("_", " ").title()
        rate = stats.get("passed") / stats.get("total") if stats.get("total") > 0 else 0
        print(f"   {cat_name}: {stats.get('passed')}/{stats.get('total')} ({rate:.0%})")
    
    print("\n" + "=" * 70)
    print("✨ Analysis complete!")
    print("=" * 70 + "\n")
