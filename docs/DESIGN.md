# Simple Diagnostic Test Automation — Software Design Document

**Version:** 1.0  
**Date:** 2026-09-29  
**Author:** GitHub Copilot Training  
**Status:** Complete

---

## Table of Contents

1. [Design Overview](#design-overview)
2. [System Architecture](#system-architecture)
3. [Module Design](#module-design)
4. [Data Flow](#data-flow)
5. [Class Diagrams](#class-diagrams)
6. [API Design](#api-design)
7. [Error Handling Strategy](#error-handling-strategy)
8. [Testing Strategy](#testing-strategy)

---

## Design Overview

### Purpose
This document describes the software design of the Simple Diagnostic Test Automation system—a beginner-friendly Python framework for simulating diagnostic requests and validating responses.

### Scope
- Simulated ECU and CAN communication
- Diagnostic test case execution
- Response validation
- JSON report generation
- No real hardware required

### Design Principles
1. **Simplicity:** Each module has one clear responsibility
2. **Testability:** All modules can be tested independently
3. **Readability:** Clear naming and minimal complexity
4. **Maintainability:** Well-organized, documented code

---

## System Architecture

### High-Level Flow

```
┌─────────────────────────────────────┐
│    Test Configuration (JSON)        │
│  - Test Cases                       │
│  - Expected Responses               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    Main Entry Point (main.py)       │
│  - Orchestrates execution           │
│  - Handles exit codes               │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    Test Runner (test_runner.py)     │
│  - Loads JSON configuration         │
│  - Iterates over test cases         │
│  - Calls Mock ECU for each request  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    Mock ECU (mock_ecu.py)           │
│  - Simulates diagnostic behavior    │
│  - Returns predefined responses     │
│  - Handles unknown services         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│    Report Generator (report.py)     │
│  - Collects results                 │
│  - Generates JSON report            │
│  - Calculates summary statistics    │
└─────────────────────────────────────┘
```

### Layered Architecture

```
┌─────────────────────────────────────────┐
│ Presentation Layer                      │
│ (CLI: main.py)                          │
│ - Parse arguments                       │
│ - Handle exit codes                     │
│ - Print console output                  │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│ Business Logic Layer                    │
│ (test_runner.py)                        │
│ - Load test cases                       │
│ - Execute tests sequentially            │
│ - Collect results                       │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│ Service Layer                           │
│ (mock_ecu.py, report.py)                │
│ - ECU simulation                        │
│ - Report generation                     │
└─────────────────────────────────────────┘
```

---

## Module Design

### 1. mock_ecu.py — Simulated ECU

**Purpose:** Simulate an ECU that processes diagnostic requests and returns predefined responses.

**Functions:**
- `process_request(request_payload: str) -> str`

**Behavior:**
```
Input:  "10 01" → Output: "50 01"
Input:  "22 F1 90" → Output: "62 F1 90 12"
Input:  "27 01" → Output: "67 01"
Input:  "99 99" → Output: "7F 10 11" (negative response)
```

**Responsibilities:**
- Map incoming requests to responses
- Return negative response for unknown services
- Maintain deterministic behavior

**Implementation Strategy:**
```python
responses = {
    "10 01": "50 01",
    "22 F1 90": "62 F1 90 12",
    "27 01": "67 01",
}

if request in responses:
    return responses[request]
else:
    return "7F 10 11"  # Negative response
```

---

### 2. test_runner.py — Test Execution Engine

**Purpose:** Load test cases and orchestrate their execution.

**Functions:**
- `run_all_tests(json_file: str) -> List[Dict]`

**Input:** JSON file with test cases
```json
{
  "tests": [
    {
      "id": "TC_001",
      "description": "...",
      "request": "10 01",
      "expected": "50 01"
    }
  ]
}
```

**Output:** List of result dictionaries
```python
[
  {
    "id": "TC_001",
    "request": "10 01",
    "expected": "50 01",
    "actual": "50 01",
    "status": "PASS"
  },
  ...
]
```

**Algorithm:**
```
1. Load JSON file
2. For each test case:
   a. Extract request
   b. Call mock_ecu.process_request()
   c. Compare actual vs. expected
   d. Determine status (PASS/FAIL)
   e. Collect result
   f. Print to console
3. Return all results
```

**Responsibilities:**
- Parse and load JSON configuration
- Iterate over test cases
- Call appropriate services (mock_ecu)
- Collect and return results
- Print real-time feedback

---

### 3. report.py — Report Generation

**Purpose:** Generate structured reports from test results.

**Functions:**
- `generate_report(results: List[Dict], output_file: str) -> Dict`

**Input:** List of test results from test_runner

**Output:** JSON report file and dictionary
```json
{
  "timestamp": "2026-09-29T12:00:00.000000",
  "summary": {
    "total": 4,
    "passed": 3,
    "failed": 1
  },
  "test_results": [
    { "id": "TC_001", "status": "PASS", ... },
    ...
  ]
}
```

**Responsibilities:**
- Calculate summary statistics (total, passed, failed)
- Add timestamp to report
- Ensure output directory exists
- Write JSON file
- Return report as dictionary

---

### 4. main.py — Entry Point and CLI

**Purpose:** Provide command-line interface and orchestrate the application.

**Function:**
- `main() -> int`

**Exit Codes:**
- `0` = All tests passed
- `1` = Some tests failed
- `2` = Configuration or execution error

**Algorithm:**
```
1. Print banner
2. Call test_runner.run_all_tests()
3. Call report.generate_report()
4. Print summary
5. Return exit code based on results
```

**Responsibilities:**
- Parse command-line arguments
- Orchestrate execution flow
- Handle exceptions gracefully
- Return appropriate exit codes
- Print user-friendly output

---

## Data Flow

### Test Execution Data Flow

```
┌──────────────────────┐
│ test_data/tests.json │  (Input)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ test_runner.run_all_tests()          │
│ - Load JSON                          │
│ - Parse test cases                   │
└──────────┬───────────────────────────┘
           │
           ▼ (for each test)
┌──────────────────────────────────────┐
│ mock_ecu.process_request()           │
│ - Input: request payload             │
│ - Output: response payload           │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Compare Actual vs. Expected          │
│ - actual == expected → PASS          │
│ - actual != expected → FAIL          │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Collect Result                       │
│ {                                    │
│   "id": "TC_001",                   │
│   "status": "PASS",                 │
│   "expected": "50 01",              │
│   "actual": "50 01"                 │
│ }                                    │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ report.generate_report()             │
│ - Calculate summary                  │
│ - Generate JSON                      │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ reports/test_report.json             │  (Output)
└──────────────────────────────────────┘
```

---

## Class Diagrams

### Test Result Structure

```
┌─────────────────────────────────────┐
│         TestResult (Dict)           │
├─────────────────────────────────────┤
│ - id: str                           │
│ - request: str                      │
│ - expected: str                     │
│ - actual: str                       │
│ - status: str (PASS/FAIL)           │
└─────────────────────────────────────┘
```

### Test Case Structure (from JSON)

```
┌─────────────────────────────────────┐
│         TestCase (Dict)             │
├─────────────────────────────────────┤
│ - id: str                           │
│ - description: str                  │
│ - request: str                      │
│ - expected: str                     │
│ - type: str (positive/negative)     │
└─────────────────────────────────────┘
```

### Report Structure

```
┌─────────────────────────────────────┐
│          Report (Dict)              │
├─────────────────────────────────────┤
│ - timestamp: str (ISO 8601)         │
│ - summary: Dict                     │
│   ├─ total: int                     │
│   ├─ passed: int                    │
│   └─ failed: int                    │
│ - test_results: List[TestResult]    │
└─────────────────────────────────────┘
```

---

## API Design

### Public API

#### mock_ecu.py
```python
def process_request(request_payload: str) -> str:
    """
    Process a diagnostic request and return response.
    
    Args:
        request_payload: String like "10 01"
    
    Returns:
        String like "50 01" or "7F 10 11"
    """
```

#### test_runner.py
```python
def run_all_tests(json_file: str) -> List[Dict]:
    """
    Load and execute all test cases.
    
    Args:
        json_file: Path to test_data/tests.json
    
    Returns:
        List of test result dictionaries
    
    Raises:
        FileNotFoundError: If JSON file not found
        json.JSONDecodeError: If JSON is invalid
        KeyError: If required fields missing
    """
```

#### report.py
```python
def generate_report(results: List[Dict], 
                   output_file: str = "reports/test_report.json") -> Dict:
    """
    Generate a JSON report from test results.
    
    Args:
        results: List of test result dictionaries
        output_file: Path to save JSON report
    
    Returns:
        Report dictionary with summary and results
    """
```

#### main.py
```python
def main() -> int:
    """
    Execute all tests and generate report.
    
    Returns:
        Exit code: 0=pass, 1=fail, 2=error
    """
```

---

## Error Handling Strategy

### Error Levels

| Level | Scenario | Action | Exit Code |
|-------|----------|--------|-----------|
| **FATAL** | JSON file not found | Print error, exit | 2 |
| **FATAL** | Invalid JSON syntax | Print error, exit | 2 |
| **ERROR** | Missing required field | Print error, skip test | 2 |
| **WARNING** | Test fails | Record FAIL, continue | 1 |
| **INFO** | Test passes | Record PASS, continue | 0 |

### Error Messages

**Example: File not found**
```
Error: Cannot load test file 'test_data/tests.json'
Please ensure the file exists and is readable.
Exit code: 2
```

**Example: Invalid JSON**
```
Error: Invalid JSON syntax in test file
Details: Expecting value: line 1 column 2 (char 1)
Exit code: 2
```

**Example: Missing field**
```
Error: Test case TC_001 missing required field 'expected'
Exit code: 2
```

---

## Testing Strategy

### Unit Testing

| Module | Test Cases | Coverage |
|--------|-----------|----------|
| mock_ecu.py | 4 tests | 100% |
| test_runner.py | 3 tests | 80% |
| report.py | 2 tests | 80% |
| **Total** | **9 tests** | **~87%** |

### Test Categories

1. **Positive Tests** — Expected behavior
2. **Negative Tests** — Error handling
3. **Edge Cases** — Boundary conditions

### Quality Metrics

- **Code Coverage:** >80%
- **Test Pass Rate:** 100%
- **Execution Time:** <5 seconds
- **Portability:** Windows & Linux

---

## Design Trade-offs

| Aspect | Choice | Reasoning |
|--------|--------|-----------|
| **Architecture** | Layered (simple) | Beginner-friendly, easy to test |
| **Data Format** | JSON | Human-readable, standard format |
| **Error Handling** | Try-except + messages | Clear error reporting for beginners |
| **Testing** | pytest | Industry standard, simple syntax |
| **Deployment** | CLI only | No complex web framework needed |

---

## Future Enhancements (Out of MVP Scope)

- [ ] HTML report generation
- [ ] CSV test result export
- [ ] Database integration
- [ ] Real CAN interface
- [ ] Web UI dashboard
- [ ] Performance metrics
- [ ] Parallel test execution
- [ ] Configuration validation schema

---

## Design Validation Checklist

- ✅ All modules have single responsibility
- ✅ Data flow is clear and unidirectional
- ✅ Error handling is comprehensive
- ✅ APIs are simple and documented
- ✅ Design supports independent testing
- ✅ No hardcoded dependencies
- ✅ Configuration externalized (JSON)
- ✅ Exit codes support CI/CD integration

---

**Document Version:** 1.0  
**Last Updated:** 2026-09-29  
**Status:** Ready for Implementation
