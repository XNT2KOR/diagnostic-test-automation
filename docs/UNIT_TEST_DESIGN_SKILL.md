# Skill: Unit Test Design for Python Projects

**Version:** 1.0  
**Type:** Workflow Skill  
**Scope:** Workspace (applicable to any Python project)  
**Domain:** Test Strategy, Test Specification, Test Implementation  

---

## Overview

This skill provides a structured, reusable workflow for designing comprehensive unit tests for Python projects. It guides you through:

1. **Test Strategy Definition** — Understanding test pyramid, coverage targets, and test categories
2. **Test Specification** — Documenting what to test with clear procedures and expected results
3. **Test Implementation** — Writing actual pytest tests that validate functionality
4. **Coverage Validation** — Measuring and ensuring adequate test coverage
5. **Test Maintenance** — Updating and improving tests as code evolves

**Ideal For:**
- Beginners learning test-driven development (TDD)
- Teams standardizing test design across projects
- Projects requiring test traceability (TCID mapping)
- Quality assurance and verification workflows

---

## When to Use This Skill

**Trigger this skill when:**
- Starting a new Python project and need to plan testing strategy
- Adding significant new functionality requiring comprehensive tests
- Improving test coverage below target threshold (e.g., <80%)
- Onboarding new team members to testing standards
- Creating documentation for test specifications (CSV, traceability matrix)
- Reviewing code and identifying missing test scenarios

**Do NOT use this skill for:**
- Quick unit test fixes (use pytest documentation instead)
- Debugging failing tests (use debugging workflow)
- Performance testing or load testing (separate specialized skill)
- Mocking complex third-party services (use mocking patterns skill)

---

## Step-by-Step Workflow

### Phase 1: Test Strategy Definition (30-45 minutes)

**Objective:** Establish testing approach and coverage targets

#### 1.1 Understand Your Modules

List all modules that need testing:

```bash
# Example project structure
src/
├── mock_ecu.py          # Module 1: Mock ECU simulator
├── test_runner.py       # Module 2: Test execution engine
├── report.py            # Module 3: Report generation
└── main.py              # Module 4: CLI orchestrator
```

**Action:** For each module, document:
- Purpose (1-2 sentences)
- Key functions/classes
- Dependencies (what it imports)
- Complexity level (simple/medium/complex)

#### 1.2 Define Test Pyramid

Structure tests in a pyramid:

```
        E2E Tests (1)
       /           \
    Integration (2)
   /               \
Unit Tests (6+)
```

**Rule of Thumb:**
- **Unit Tests (60-70%):** Test individual functions in isolation
- **Integration Tests (20-30%):** Test module interactions
- **E2E Tests (10%):** Test full system workflows

**Action:** For your project, specify:
- Total desired test count (e.g., 20)
- Unit test count (e.g., 12)
- Integration test count (e.g., 6)
- E2E test count (e.g., 2)

#### 1.3 Set Coverage Target

Define minimum acceptable code coverage:

| Module | Target | Rationale |
|--------|--------|-----------|
| Core logic | >90% | Critical paths, must be thoroughly tested |
| Utilities | >85% | Used by many functions |
| Edge cases | >80% | Error handling, edge scenarios |
| Overall | >80% | Industry standard for production code |

**Action:** Document your project's coverage targets in a table.

#### 1.4 Identify Test Categories

Categorize tests by what they validate:

| Category | Purpose | Example |
|----------|---------|---------|
| **Positive Tests** | Valid input → correct output | `test_valid_request_returns_expected_response()` |
| **Negative Tests** | Invalid input → graceful error | `test_invalid_request_returns_negative_response()` |
| **Edge Cases** | Boundary conditions | `test_empty_string_request()`, `test_max_length_payload()` |
| **Error Handling** | Exception handling | `test_missing_file_raises_file_not_found()` |
| **State Changes** | Verify state after operation | `test_report_file_created_after_execution()` |

**Action:** List 3-5 test categories relevant to your project.

---

### Phase 2: Test Specification (45-60 minutes)

**Objective:** Document WHAT will be tested with detailed procedures

#### 2.1 Create Test Case Template

Document each test case with this structure:

| Field | Description | Example |
|-------|-------------|---------|
| **TCID** | Unique test ID | TC_001 |
| **Name** | Short test name | "Session Control Request" |
| **Description** | What is being tested | "Verify ECU returns correct response for diagnostic session control request" |
| **Procedure** | Step-by-step steps | 1. Load test data\n2. Call mock_ecu.process_request('10 01')\n3. Assert response equals '50 01' |
| **Expected Results** | What should happen | Response is exactly '50 01' |
| **Verdict** | Status (PASS/FAIL/PENDING) | PASS |
| **Parameters** | Test inputs | request='10 01' |

#### 2.2 Enumerate Test Cases by Module

For each module, list test cases:

```
MODULE: mock_ecu.py
├── TC_001: Valid request → correct response
├── TC_002: Unknown service → negative response
├── TC_003: Multiple request types
└── TC_004: Malformed request handling

MODULE: test_runner.py
├── TC_005: Load valid JSON test file
├── TC_006: Missing JSON file error
├── TC_007: Invalid JSON syntax error
└── TC_008: Empty test list handling

MODULE: report.py
├── TC_009: Generate JSON report with timestamp
├── TC_010: Report summary calculation
├── TC_011: Report file creation
└── TC_012: Report directory handling

MODULE: main.py (E2E)
├── TC_013: Execute complete workflow
├── TC_014: Exit code 0 on all tests pass
├── TC_015: Exit code 1 on any test fail
└── TC_016: Exit code 2 on configuration error
```

**Action:** Create a similar breakdown for your project.

#### 2.3 Document Test Procedures

For each test, write detailed numbered steps:

```markdown
### TC_001: Valid Session Control Request

**Procedure:**
1. Import mock_ecu module
2. Call mock_ecu.process_request('10 01')
3. Store returned response
4. Assert response == '50 01'
5. Verify no exceptions thrown

**Expected Result:**
- Function returns '50 01' (positive response)
- No exceptions or errors
- Execution time < 1 second
```

**Best Practices:**
- Use clear, actionable language ("call", "assert", "verify")
- Number each step
- One action per step
- Include expected outcomes at each step if complex

#### 2.4 Create Test Specification CSV

Document all test cases in a CSV file:

```csv
TCID,TEST CASE NAME,TEST CASE DESCRIPTION,TEST PROCEDURE,EXPECTED RESULTS,VERDICT,PARAMETERS
TC_001,Session Control Request,Verify ECU response for session control,"1. Call mock_ecu.process_request('10 01')
2. Assert response == '50 01'",Response is '50 01' exactly,PASS,request='10 01'
TC_002,Read Data Request,Verify ECU response for read data,"1. Call mock_ecu.process_request('22 F1 90')
2. Assert response == '62 F1 90 12'",Response is '62 F1 90 12' exactly,PASS,request='22 F1 90'
```

**Tools & Format:**
- Format: RFC 4180 compliant CSV
- Encoding: UTF-8
- Save location: `docs/test_design.csv`
- Validation: Use `docs/validate_csv.py --fix` to auto-correct issues

---

### Phase 3: Test Implementation (1-2 hours)

**Objective:** Write actual pytest tests based on specifications

#### 3.1 Create Test File Structure

Organize test files by module:

```
tests/
├── __init__.py
├── test_mock_ecu.py        # Tests for mock_ecu.py
├── test_test_runner.py     # Tests for test_runner.py
├── test_report.py          # Tests for report.py
└── test_integration.py     # Integration and E2E tests
```

**Naming Convention:**
- File: `test_<module_name>.py`
- Function: `test_<what_is_being_tested>()`
- Class (optional): `Test<ModuleName>`

#### 3.2 Implement Unit Tests

Follow this structure for each unit test:

```python
# tests/test_mock_ecu.py
import pytest
from src.mock_ecu import process_request


class TestMockECU:
    """Unit tests for mock ECU module."""
    
    def test_session_control_response(self):
        """TC_001: Verify ECU returns correct response for session control."""
        # Arrange (setup)
        request = "10 01"
        
        # Act (execute)
        response = process_request(request)
        
        # Assert (verify)
        assert response == "50 01", f"Expected '50 01', got '{response}'"
    
    def test_unknown_service_returns_negative_response(self):
        """TC_002: Verify ECU returns negative response for unknown service."""
        # Arrange
        request = "99 99"
        
        # Act
        response = process_request(request)
        
        # Assert
        assert response == "7F 10 11"
        assert response.startswith("7F")  # Negative response indicator


# Parametrized test example (tests multiple scenarios)
@pytest.mark.parametrize("request,expected", [
    ("10 01", "50 01"),
    ("22 F1 90", "62 F1 90 12"),
    ("27 01", "67 01"),
    ("99 99", "7F 10 11"),
])
def test_diagnostic_services(request, expected):
    """TC_003-006: Test multiple diagnostic services."""
    response = process_request(request)
    assert response == expected
```

**Best Practices:**
- One assertion per test when possible
- Clear, descriptive test names (what is being tested)
- Use Arrange-Act-Assert pattern
- Include docstring with TCID reference
- Use parametrized tests to reduce duplication

#### 3.3 Implement Integration Tests

Test interactions between modules:

```python
# tests/test_integration.py
import json
import tempfile
import pytest
from src.test_runner import run_all_tests
from src.report import generate_report


def test_end_to_end_workflow():
    """TC_013: Execute complete test workflow end-to-end."""
    # Create temporary test data
    test_data = {
        "tests": [
            {"id": "TC_001", "request": "10 01", "expected": "50 01", "type": "positive"},
            {"id": "TC_002", "request": "99 99", "expected": "7F 10 11", "type": "negative"},
        ]
    }
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_file = f.name
    
    try:
        # Execute workflow
        results = run_all_tests(temp_file)
        
        # Verify results
        assert len(results) == 2
        assert all(r['status'] in ['PASS', 'FAIL'] for r in results)
        
        # Generate report
        report = generate_report(results)
        assert report['summary']['total'] == 2
    finally:
        import os
        os.unlink(temp_file)
```

#### 3.4 Implement Error Handling Tests

Test exception scenarios:

```python
# tests/test_error_handling.py
import pytest
from src.test_runner import run_all_tests


def test_missing_json_file_raises_error():
    """TC_009: Verify graceful error when JSON file missing."""
    with pytest.raises(FileNotFoundError):
        run_all_tests("nonexistent_file.json")


def test_invalid_json_syntax_raises_error():
    """TC_010: Verify graceful error when JSON invalid."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("{ invalid json }")
        temp_file = f.name
    
    try:
        with pytest.raises(json.JSONDecodeError):
            run_all_tests(temp_file)
    finally:
        os.unlink(temp_file)
```

---

### Phase 4: Coverage Validation (15-30 minutes)

**Objective:** Measure and report test coverage

#### 4.1 Run Tests with Coverage

```bash
# Run all tests with coverage report
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_mock_ecu.py --cov=src.mock_ecu

# Run with minimal coverage report
pytest tests/ --cov=src --cov-report=term-missing
```

#### 4.2 Interpret Coverage Report

```
Name                Stmts   Miss  Cover
---------------------------------------
src/__init__.py        0      0   100%
src/mock_ecu.py       20      0   100%    ← Full coverage
src/test_runner.py    40      5    87%    ← 5 lines not tested
src/report.py         25      3    87%    ← 3 lines not tested
---------------------------------------
TOTAL                 85      8    91%    ← Overall coverage
```

**Analysis:**
- **100% Coverage** — All code paths tested
- **87-99% Coverage** — Good, minor gaps (usually error paths)
- **80-86% Coverage** — Acceptable, some scenarios untested
- **<80% Coverage** — Below target, add more tests

#### 4.3 Identify Untested Code

Use `--cov-report=term-missing` to see which lines lack tests:

```
src/test_runner.py:25: if not results:
src/test_runner.py:26:     return []
src/test_runner.py:67: except Exception as e:
src/test_runner.py:68:     print(f"Error: {e}")
```

**Action:** For each missing line:
1. Determine if it's testable
2. Add a test case to cover it
3. Re-run coverage

#### 4.4 Create Coverage Report

Document coverage by module:

| Module | Lines | Covered | Coverage | Status |
|--------|-------|---------|----------|--------|
| mock_ecu.py | 20 | 20 | 100% | ✅ Excellent |
| test_runner.py | 40 | 35 | 87% | ✅ Good |
| report.py | 25 | 21 | 87% | ✅ Good |
| main.py | 40 | 36 | 90% | ✅ Good |
| **TOTAL** | **125** | **112** | **91%** | **✅ PASS** |

---

### Phase 5: Test Maintenance (Ongoing)

**Objective:** Keep tests updated as code evolves

#### 5.1 Add Tests for New Features

When adding a function:

```python
def new_feature(x):
    """Add new feature."""
    return x * 2


# Immediately add test
def test_new_feature():
    """Test new feature."""
    assert new_feature(5) == 10
```

**Best Practice:** Write test BEFORE or IMMEDIATELY AFTER writing code (TDD).

#### 5.2 Update Tests When Behavior Changes

If you modify a function's behavior:

```python
# OLD CODE
def process_request(request):
    if not request:
        return "ERROR"


# NEW CODE
def process_request(request):
    if not request:
        return None  # Changed behavior


# UPDATE TEST
def test_empty_request():
    # OLD: assert process_request("") == "ERROR"
    # NEW:
    assert process_request("") is None
```

#### 5.3 Remove Obsolete Tests

Delete tests for removed code:

```bash
# Search for references to removed function
grep -r "deleted_function" tests/

# Delete related test functions
rm tests/test_deleted_function.py
```

#### 5.4 Refactor Tests for Clarity

Over time, refactor tests to improve readability:

```python
# BEFORE: Test with magic values
def test_calculation():
    assert process([1, 2, 3]) == 6


# AFTER: Test with descriptive setup
def test_sum_calculation_with_positive_integers():
    """Test that positive integers are summed correctly."""
    # Arrange
    input_values = [1, 2, 3]
    expected_sum = 6
    
    # Act
    result = process(input_values)
    
    # Assert
    assert result == expected_sum, f"Expected {expected_sum}, got {result}"
```

---

## Prompts to Use With Copilot

Once you've defined your test strategy, use these prompts with GitHub Copilot:

### Test Generation Prompts

1. **"Generate pytest unit tests for this function covering positive cases, negative cases, and edge cases"**
   - Copilot will generate comprehensive test suite

2. **"Create parametrized pytest tests for these scenarios: [list scenarios]"**
   - Copilot will generate `@pytest.mark.parametrize` tests

3. **"Write integration tests that test the interaction between [module A] and [module B]"**
   - Copilot will test module interactions

4. **"Generate error handling tests for this function that verifies it gracefully handles [exception types]"**
   - Copilot will generate exception handling tests

### Test Review Prompts

5. **"Review these tests for coverage gaps. What scenarios are missing?"**
   - Copilot will identify untested paths

6. **"Suggest how to improve these tests for readability and maintainability"**
   - Copilot will refactor and suggest improvements

7. **"Are these tests following pytest best practices? What can be improved?"**
   - Copilot will audit test quality

---

## Validation Checklist

Before marking unit tests as complete, verify:

- ✅ Test strategy documented (pyramid, coverage targets)
- ✅ All modules have test files (`test_<module>.py`)
- ✅ Test cases documented in CSV or similar format
- ✅ All tests have descriptive names and docstrings
- ✅ Unit tests run in isolation (no dependencies between tests)
- ✅ Edge cases and error scenarios covered
- ✅ Coverage measurement tool configured (pytest-cov)
- ✅ Coverage >80% achieved
- ✅ All tests pass: `pytest tests/ -v` shows all ✅
- ✅ No test warnings or deprecation messages
- ✅ Test execution time <5 seconds for quick feedback

---

## Tools & Files

| Tool | Purpose | Command |
|------|---------|---------|
| **pytest** | Test runner | `pytest tests/ -v` |
| **pytest-cov** | Coverage measurement | `pytest tests/ --cov=src` |
| **CSV validator** | Validate test specs | `python docs/validate_csv.py --fix` |
| **Copilot** | Test generation assistance | Use in VS Code |

| File | Purpose |
|------|---------|
| `requirements.txt` | Lists pytest, pytest-cov dependencies |
| `pytest.ini` | Pytest configuration (test paths, naming) |
| `docs/test_design.csv` | Test specification matrix |
| `tests/test_*.py` | Actual test implementations |

---

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| Test names unclear (e.g., `test_x()`) | Use descriptive names: `test_valid_request_returns_response()` |
| No separation of arrange/act/assert | Structure all tests with AAA pattern |
| Testing implementation instead of behavior | Focus on WHAT function does, not HOW it does it |
| Tests with multiple assertions | One assertion per test (or related assertions in parametrized tests) |
| Tests dependent on execution order | Make tests independent; use fixtures for setup |
| Skipping edge cases | Test boundaries, empty inputs, invalid types |
| No documentation of test purpose | Add docstrings referencing TCID and requirement |
| Coverage report ignored | Review coverage report after each run; target >80% |

---

## Related Skills & Resources

- **Debugging Python Code** — When tests fail, use this to identify root causes
- **Code Review Workflow** — Verify test quality in pull requests
- **GitHub Actions CI/CD** — Automate test execution on every commit
- **Mocking and Fixtures** — For advanced pytest patterns

**External Resources:**
- pytest documentation: https://docs.pytest.org/
- Code coverage best practices: https://coverage.readthedocs.io/
- Test pyramid concept: https://testingpyramid.com/

---

**Version History:**
- v1.0 (2026-09-29) — Initial skill creation

**Last Updated:** 2026-09-29
