"""Generate test reports."""

import json
from datetime import datetime


def generate_report(results, output_file="reports/test_report.json"):
    """Generate a JSON report from test results.
    
    Args:
        results: List of test result dictionaries
        output_file: Path to save the report
    """
    
    passed_count = sum(1 for r in results if r['status'] == 'PASS')
    total_count = len(results)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total_count,
            "passed": passed_count,
            "failed": total_count - passed_count
        },
        "test_results": results
    }
    
    # Create reports directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
    
    # Write report to file
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    return report
