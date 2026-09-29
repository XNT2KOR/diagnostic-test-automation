"""Main entry point for diagnostic test automation."""

from src.test_runner import run_all_tests
from src.report import generate_report
import sys


def main():
    """Run diagnostic tests and generate report."""
    
    try:
        print("=" * 50)
        print("Simple Diagnostic Test Automation")
        print("=" * 50)
        print()
        
        # Run all tests
        results = run_all_tests("test_data/tests.json")
        
        # Generate report
        generate_report(results)
        
        # Print summary
        print()
        print("=" * 50)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        total = len(results)
        print(f"Total: {total} | Passed: {passed} | Failed: {total - passed}")
        print("=" * 50)
        
        # Return appropriate exit code
        if passed == total:
            print("✓ All tests passed!")
            return 0
        else:
            print("✗ Some tests failed!")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
