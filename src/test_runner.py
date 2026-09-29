"""Test runner that loads and executes diagnostic tests."""

import json
from src.mock_ecu import process_request


def run_all_tests(json_file):
    """Load test cases from JSON and run each one.
    
    Args:
        json_file: Path to JSON file with test cases
    
    Returns:
        List of results like [{'id': 'TC_001', 'status': 'PASS'}, ...]
    """
    
    # Load test cases from JSON
    with open(json_file) as f:
        data = json.load(f)
    
    results = []
    
    # Run each test case
    for test in data["tests"]:
        test_id = test["id"]
        request = test["request"]
        expected_response = test["expected"]
        
        # Send request to mock ECU
        actual_response = process_request(request)
        
        # Check if correct
        if actual_response == expected_response:
            status = "PASS"
        else:
            status = "FAIL"
        
        results.append({
            "id": test_id,
            "request": request,
            "expected": expected_response,
            "actual": actual_response,
            "status": status
        })
        
        print(f"{test_id}: {status}")
    
    return results
