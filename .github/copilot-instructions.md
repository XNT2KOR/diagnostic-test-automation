# CAN/DCOM Diagnostic Test Automation — Simple Beginner Guide

## 1. Project Name

**Simple Diagnostic Test Automation**

---

## 2. Description

A beginner-friendly Python project that:
- Reads diagnostic test cases from a JSON file
- Simulates sending a diagnostic request to a pretend ECU
- Receives a simulated response
- Checks if the response is correct (PASS or FAIL)
- Generates a simple test report

**No real hardware needed. Everything is simulated in Python.**

---

## 3. Technology Stack

| What | Version |
|------|---------|
| Python | 3.9+ |
| Testing | pytest |
| Version Control | Git |
| Repository | GitHub |
| CI/CD | GitHub Actions |

**That's it. Very simple.**

---

## 4. Design Pattern

**Keep it simple: One function does one job**

```
1. Load test cases from JSON file
2. Send request to mock ECU
3. Get response back
4. Compare: Does response match expected?
5. Save PASS or FAIL result
6. Print report
```

No fancy design patterns needed for a beginner project.

---

## 5. Language & Libraries

### Python Version
```
Python 3.9 or higher
```

### What You Need
```
pip install pytest
pip install pytest-cov
```

**That's all. Just 2 libraries.**

### How to Set Up
```bash
# Create a folder
mkdir my-test-project
cd my-test-project

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install the 2 libraries
pip install pytest pytest-cov

# Create requirements.txt for later
pip freeze > requirements.txt
```

---

## 6. Coding Standards

Keep it simple:

| Rule | Example |
|------|---------|
| Use normal Python names | `test_result`, `can_message`, not `tst_rslt` |
| Indent with 4 spaces | See examples below |
| One task per function | Don't make mega-functions |
| Add a comment when unclear | `# Check if response matches` |

**That's all the "rules" you need.**

---

## 7. Folder Structure — Simple!

```
.
├── src/
│   ├── __init__.py
│   ├── mock_ecu.py          # Pretend ECU
│   ├── test_runner.py       # Run tests
│   └── report.py            # Print results
│
├── tests/
│   └── test_simple.py       # Your tests
│
├── test_data/
│   └── tests.json           # Test cases
│
├── main.py                  # Start here
├── requirements.txt         # Python libraries
├── .gitignore               # Ignore files
└── README.md                # Documentation
```

**That's it. 10 files total for the whole project.**

---

## 8. Sample Code

### 8.1 The Main Entry Point (main.py)

```python
"""Main entry point - run this to test everything."""

from src.test_runner import run_all_tests

if __name__ == "__main__":
    results = run_all_tests("test_data/tests.json")
    print("\n" + "="*50)
    print(f"Total: {len(results)} | Passed: {sum(1 for r in results if r['status'] == 'PASS')}")
    print("="*50)
```

### 8.2 The Mock ECU (src/mock_ecu.py)

```python
"""Pretend ECU that returns canned responses."""

def process_request(request_payload):
    """Process a diagnostic request and return a response.
    
    Args:
        request_payload: String like "10 01"
    
    Returns:
        String like "50 01" or None if service not recognized
    """
    
    # Simple mapping: request -> response
    responses = {
        "10 01": "50 01",           # Diagnostic session
        "22 F1 90": "62 F1 90 12",  # Read data
        "27 01": "67 01",           # Security access
    }
    
    if request_payload in responses:
        return responses[request_payload]
    else:
        return "7F 10 11"  # Negative response for unknown service
```

**That's it. No complex logic.**

### 8.3 The Test Runner (src/test_runner.py)

```python
"""Load tests and run them."""

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
```

**Simple and clear.**

### 8.4 Simple Test Data (test_data/tests.json)

```json
{
  "tests": [
    {
      "id": "TC_001",
      "description": "Test session control",
      "request": "10 01",
      "expected": "50 01"
    },
    {
      "id": "TC_002",
      "description": "Test read data",
      "request": "22 F1 90",
      "expected": "62 F1 90 12"
    },
    {
      "id": "TC_003",
      "description": "Test unknown service",
      "request": "99 99",
      "expected": "7F 10 11"
    }
  ]
}
```

**Just 3 test cases. Easy to understand.**

### 8.5 Simple Unit Test (tests/test_simple.py)

```python
"""Simple tests for the mock ECU."""

from src.mock_ecu import process_request


def test_session_control_response():
    """Test that ECU returns correct response."""
    response = process_request("10 01")
    assert response == "50 01"


def test_read_data_response():
    """Test read data response."""
    response = process_request("22 F1 90")
    assert response == "62 F1 90 12"


def test_unknown_service_returns_error():
    """Test that unknown service gets negative response."""
    response = process_request("99 99")
    assert response == "7F 10 11"
```

**Run with:** `pytest tests/test_simple.py`

---

## 9. Sensitive Data Handling

### Simple Rule: Don't Put Secrets in Code

**Bad:**
```python
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"  # DON'T DO THIS!
```

**Good:**
```python
import os
AWS_KEY = os.getenv("AWS_KEY")  # Get from environment
```

### How to Do It

1. **Create a `.env` file** (not in Git):
```
AWS_KEY=your_secret_here
AWS_BUCKET=my-bucket
```

2. **Add to `.gitignore`**:
```
.env
*.pyc
__pycache__
venv/
```

3. **Load in your code**:
```python
import os
my_secret = os.getenv("AWS_KEY")  # Safe!
```

**That's all you need to know.**

---

## Quick Start Guide

### 1. Set Up (First Time Only)
```bash
# Create folder
mkdir my-test-project
cd my-test-project

# Initialize Git
git init

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install pytest
pip install pytest pytest-cov
pip freeze > requirements.txt
```

### 2. Create Files (Use Copilot!)
Ask Copilot: "Generate a simple Python function that loads a JSON file of diagnostic test cases"

### 3. Run Tests
```bash
pytest tests/
```

### 4. Run the App
```bash
python main.py
```

### 5. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

---

## 16-Hour Training Timeline (Simplified)

| Hour | Activity |
|------|----------|
| 1 | Setup: Git, Python, GitHub |
| 2-3 | Write `mock_ecu.py` with Copilot |
| 4-5 | Write `test_runner.py` with Copilot |
| 6-7 | Write tests in `tests/test_simple.py` |
| 8 | Debug and fix issues |
| 9 | Clean up code |
| 10 | Code review with Copilot |
| 11-12 | GitHub Actions setup |
| 13-14 | Try AWS S3 (optional) |
| 15-16 | Buffer / Extra practice |

---

## File Checklist

After completing the project, you should have:

- ✅ `main.py` — Runs everything
- ✅ `src/mock_ecu.py` — Fake ECU
- ✅ `src/test_runner.py` — Runs tests
- ✅ `src/__init__.py` — Package marker
- ✅ `test_data/tests.json` — Test cases
- ✅ `tests/test_simple.py` — Unit tests
- ✅ `tests/__init__.py` — Package marker
- ✅ `requirements.txt` — Python libraries
- ✅ `.gitignore` — Files to skip
- ✅ `README.md` — Instructions

**Total: ~200 lines of Python code. Very manageable.**

---

## Copilot Tips for Beginners

**Ask Copilot things like:**

1. "Write a Python function that loads JSON from a file"
2. "How do I compare two strings in Python?"
3. "Write a simple unit test with pytest"
4. "Generate a GitHub Actions workflow that runs pytest"
5. "How do I use environment variables in Python?"

**Copilot will help you with the typing. You focus on logic.**

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Did you install pytest? `pip install pytest` |
| "FileNotFoundError" | Is `test_data/tests.json` in the right folder? |
| GitHub Actions fails | Check that pytest runs locally first: `pytest tests/` |
| Can't run `main.py` | Make sure you activated venv: `source venv/bin/activate` |

---

## Resources

- Python basics: https://www.python.org/about/gettingstarted/
- pytest tutorial: https://docs.pytest.org/en/stable/
- GitHub for beginners: https://docs.github.com/en/get-started
- GitHub Copilot: https://github.com/features/copilot

---

**Last Updated:** 2026-09-28  
**Version:** 2.0 (Beginner-Friendly Simplified)**
