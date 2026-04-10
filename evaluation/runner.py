"""
Evaluation Runner for Weather & News Agent

Executes evaluation tests and generates evaluation reports with metrics.
"""

import asyncio
import json
import logging
from typing import List, Dict, Any
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.dataset import get_evaluation_dataset
from evaluation.metrics import EvaluationMetrics, MetricResult
from agent.orchestrator import answer_question

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EvaluationRunner:
    """
    Runs evaluation tests and generates reports
    """
    
    def __init__(self):
        self.metrics = EvaluationMetrics()
        self.dataset = get_evaluation_dataset()
        self.results = []
    
    async def run_evaluation(self, limit: int = None) -> Dict[str, Any]:
        """
        Run evaluation on dataset
        
        Args:
            limit: Maximum number of tests to run (None for all)
            
        Returns:
            Dictionary with evaluation results and summary
        """
        logger.info("🚀 Starting evaluation run...")
        
        tests_to_run = self.dataset[:limit] if limit else self.dataset
        
        for i, test in enumerate(tests_to_run, 1):
            logger.info(f"Running test {i}/{len(tests_to_run)}: {test['id']}")
            
            try:
                # Run agent
                response = await answer_question(test["query"])
                
                # Evaluate
                metric_results = self.metrics.evaluate_all(
                    test_id=test["id"],
                    user_query=test["query"],
                    agent_response=response,
                    expected_fields=test["expected_fields"],
                    expected_agent=test["expected_agent"]
                )
                
                # Store results
                test_result = {
                    "test_id": test["id"],
                    "query": test["query"],
                    "category": test["category"],
                    "expected_agent": test["expected_agent"],
                    "actual_agent": response.get("query_type"),
                    "metrics": [
                        {
                            "type": r.metric_type.value,
                            "passed": r.passed,
                            "score": r.score,
                            "details": r.details
                        }
                        for r in metric_results
                    ],
                    "response_preview": response.get("message", "")[:200]
                }
                
                self.results.append(test_result)
                
                # Log result
                pass_rate = sum(1 for m in metric_results if m.passed) / len(metric_results)
                avg_score = sum(m.score for m in metric_results) / len(metric_results)
                logger.info(
                    f"  ✓ Test {test['id']}: "
                    f"Pass Rate: {pass_rate:.1%}, Avg Score: {avg_score:.2f}"
                )
            
            except Exception as e:
                logger.error(f"  ✗ Test {test['id']} failed: {str(e)}")
                self.results.append({
                    "test_id": test["id"],
                    "query": test["query"],
                    "category": test["category"],
                    "error": str(e),
                    "metrics": []
                })
        
        # Generate summary
        summary = self._generate_summary()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(tests_to_run),
            "completed_tests": len([r for r in self.results if "error" not in r]),
            "failed_tests": len([r for r in self.results if "error" in r]),
            "summary": summary,
            "results": self.results
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        
        # Flatten all metric results
        all_metrics = []
        for result in self.results:
            if "metrics" in result:
                all_metrics.extend(result["metrics"])
        
        if not all_metrics:
            return {}
        
        # Calculate statistics
        passed_count = sum(1 for m in all_metrics if m["passed"])
        total_count = len(all_metrics)
        avg_score = sum(m["score"] for m in all_metrics) / total_count if total_count > 0 else 0
        
        # Group by metric type
        by_type = {}
        for metric in all_metrics:
            mtype = metric["type"]
            if mtype not in by_type:
                by_type[mtype] = {"passed": 0, "total": 0, "scores": []}
            by_type[mtype]["passed"] += int(metric["passed"])
            by_type[mtype]["total"] += 1
            by_type[mtype]["scores"].append(metric["score"])
        
        # Calculate pass rates by type
        for mtype in by_type:
            scores = by_type[mtype]["scores"]
            by_type[mtype]["average_score"] = sum(scores) / len(scores) if scores else 0
            by_type[mtype]["pass_rate"] = (
                by_type[mtype]["passed"] / by_type[mtype]["total"]
                if by_type[mtype]["total"] > 0
                else 0
            )
            del by_type[mtype]["scores"]
        
        # Group by category
        by_category = {}
        for result in self.results:
            if "error" not in result:
                category = result["category"]
                if category not in by_category:
                    by_category[category] = {"passed": 0, "total": 0}
                by_category[category]["total"] += 1
                
                # Check if all metrics passed
                if all(m["passed"] for m in result["metrics"]):
                    by_category[category]["passed"] += 1
        
        return {
            "overall_pass_rate": passed_count / total_count if total_count > 0 else 0,
            "overall_average_score": avg_score,
            "by_metric_type": by_type,
            "by_category": by_category
        }
    
    def save_report(self, filepath: str):
        """Save evaluation report to file"""
        
        if not self.results:
            logger.error("No results to save. Run evaluation first.")
            return
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(self.results),
            "completed_tests": len([r for r in self.results if "error" not in r]),
            "failed_tests": len([r for r in self.results if "error" in r]),
            "summary": self._generate_summary(),
            "results": self.results
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"📊 Report saved to {filepath}")
    
    def print_summary(self):
        """Print summary to console"""
        
        summary = self._generate_summary()
        
        print("\n" + "="*60)
        print("📊 EVALUATION SUMMARY")
        print("="*60)
        
        print(f"\nOverall Pass Rate: {summary.get('overall_pass_rate', 0):.1%}")
        print(f"Overall Average Score: {summary.get('overall_average_score', 0):.2f}/1.0")
        
        print("\n📈 By Metric Type:")
        for mtype, stats in summary.get("by_metric_type", {}).items():
            print(
                f"  {mtype}: "
                f"{stats['passed']}/{stats['total']} passed "
                f"({stats['pass_rate']:.1%}), "
                f"Avg Score: {stats['average_score']:.2f}"
            )
        
        print("\n📂 By Category:")
        for category, stats in summary.get("by_category", {}).items():
            print(
                f"  {category}: "
                f"{stats['passed']}/{stats['total']} passed "
                f"({stats['passed']/stats['total']:.1%})"
            )
        
        print("\n" + "="*60)


async def main():
    """Main evaluation execution"""
    
    print("🤖 Weather & News Agent - Evaluation Suite\n")
    
    runner = EvaluationRunner()
    
    # Run evaluation
    report = await runner.run_evaluation(limit=None)
    
    # Print summary
    runner.print_summary()
    
    # Save report
    report_path = os.path.join(
        os.path.dirname(__file__),
        f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    runner.save_report(report_path)
    
    # Print detailed metrics example
    if runner.results:
        print("\n📋 Example Test Result:")
        print("-" * 60)
        
        example = runner.results[0]
        print(f"Test ID: {example['test_id']}")
        print(f"Query: {example['query']}")
        print(f"Expected Agent: {example['expected_agent']}")
        print(f"Actual Agent: {example['actual_agent']}")
        print("\nMetrics:")
        
        for metric in example.get("metrics", []):
            status = "✓" if metric["passed"] else "✗"
            print(
                f"  {status} {metric['type']}: "
                f"{metric['score']:.2f} - {metric['details']}"
            )


if __name__ == "__main__":
    asyncio.run(main())
