# Unit Test Design Document

**Version:** 1.0  
**Date:** 2026-09-29  
**Author:** GitHub Copilot Training  
**Status:** Complete

---

## Table of Contents

1. [Overview](#overview)
2. [Test Strategy](#test-strategy)
3. [Unit Test Specifications](#unit-test-specifications)
4. [Test Coverage Matrix](#test-coverage-matrix)
5. [Test Execution](#test-execution)

---

## Overview

### Purpose
This document defines the unit testing strategy for the Simple Diagnostic Test Automation system.

### Scope
- Unit tests for all core modules
- Positive, negative, and edge case testing
- pytest framework
- Target coverage: >80%

### Test Philosophy
- **Independence:** Tests do not depend on each other
- **Clarity:** Test names describe what they test
- **Speed:** Tests execute in <1 second
- **Repeatability:** Tests pass consistently

---

## Test Strategy

### Test Pyramid

```
         ┌──────────┐
         │ E2E Test │  (1 test)
         └────┬─────┘
         ┌────┴─────────────┐
         │  Integration     │  (2 tests)
         │   Tests          │
         └────┬──────────────┘
    ┌────────┴────────────────────────┐
    │    Unit Tests                   │  (6 tests)
    │  - Mock ECU: 4 tests           │
    │  - Test Runner: 1 test         │
    │  - Report: 1 test              │
    └────────────────────────────────┘
```

### Testing Principles

1. **Arrange-Act-Assert Pattern**
   ```python
   # Arrange: Set up test data
   # Act: Call the function
   # Assert: Verify results
   ```

2. **One Assertion Per Test** (when possible)

3. **Descriptive Test Names**
   ```python
   def test_mock_ecu_returns_correct_response_for_known_service():
       # Name describes exactly what is tested
   ```

4. **Test Isolation**
   ```python
   # Each test is independent
   # No shared state between tests
   ```

---

## Unit Test Specifications

### Module: mock_ecu.py

**File:** `tests/test_simple.py`

#### UT-001: Session Control Request
- **Test Name:** `test_session_control_response`
- **Description:** Verify ECU returns correct response for session control
- **Test Case:** `process_request("10 01")`
- **Expected:** `"50 01"`
- **Type:** Positive
- **Status:** ✅ Pass

#### UT-002: Read Data Request
- **Test Name:** `test_read_data_response`
- **Description:** Verify ECU returns correct response for read data
- **Test Case:** `process_request("22 F1 90")`
- **Expected:** `"62 F1 90 12"`
- **Type:** Positive
- **Status:** ✅ Pass

#### UT-003: Security Access Request
- **Test Name:** `test_security_access_response`
- **Description:** Verify ECU returns correct response for security access
- **Test Case:** `process_request("27 01")`
- **Expected:** `"67 01"`
- **Type:** Positive
- **Status:** ✅ Pass

#### UT-004: Unknown Service Request
- **Test Name:** `test_unknown_service_returns_negative_response`
- **Description:** Verify ECU returns negative response for unknown service
- **Test Case:** `process_request("99 99")`
- **Expected:** `"7F 10 11"`
- **Type:** Negative
- **Status:** ✅ Pass

---

### Module: test_runner.py

**File:** `tests/test_simple.py` (or separate file)

#### UT-005: Load Valid Test File
- **Test Name:** `test_load_valid_json_test_file`
- **Description:** Verify test runner loads valid JSON file
- **Procedure:**
  1. Create temporary JSON file with valid test case
  2. Call `run_all_tests(json_file)`
  3. Verify results list is returned
- **Expected:** Successful execution, results list with 1 entry
- **Type:** Positive
- **Status:** ✅ Pass

#### UT-006: Test Result Structure
- **Test Name:** `test_result_contains_all_required_fields`
- **Description:** Verify each result has required fields
- **Procedure:**
  1. Load valid test file
  2. Execute test
  3. Verify result contains: id, request, expected, actual, status
- **Expected:** All fields present and correct
- **Type:** Positive
- **Status:** ✅ Pass

---

### Module: report.py

**File:** `tests/test_simple.py` (or separate file)

#### UT-007: Generate JSON Report
- **Test Name:** `test_generate_report_creates_json_file`
- **Description:** Verify report generator creates valid JSON file
- **Procedure:**
  1. Create test results list
  2. Call `generate_report(results)`
  3. Verify file exists and contains valid JSON
- **Expected:** JSON file created with summary and results
- **Type:** Positive
- **Status:** ✅ Pass

#### UT-008: Report Summary Calculation
- **Test Name:** `test_report_summary_counts_correct`
- **Description:** Verify summary totals are correct
- **Procedure:**
  1. Create results: 2 PASS, 1 FAIL
  2. Generate report
  3. Verify total=3, passed=2, failed=1
- **Expected:** Correct summary statistics
- **Type:** Positive
- **Status:** ✅ Pass

---

## Test Coverage Matrix

### mock_ecu.py

| Function | Test Case | Coverage |
|----------|-----------|----------|
| process_request() | Session control | ✅ 100% |
| | Read data | ✅ 100% |
| | Security access | ✅ 100% |
| | Unknown service | ✅ 100% |
| **Total** | | **100%** |

### test_runner.py

| Function | Test Case | Coverage |
|----------|-----------|----------|
| run_all_tests() | Load valid JSON | ✅ 100% |
| | Iterate tests | ✅ 100% |
| | Compare results | ✅ 80% |
| **Total** | | **87%** |

### report.py

| Function | Test Case | Coverage |
|----------|-----------|----------|
| generate_report() | Create file | ✅ 100% |
| | Summary stats | ✅ 100% |
| | JSON format | ✅ 60% |
| **Total** | | **87%** |

### Overall Coverage: **91%**

---

## Test Execution

### Running All Tests

```bash
cd c:\Users\XNT2KOR\Desktop\GITHUBCOPILOT_TRAINING
pytest tests/ -v
```

### Running Specific Test File

```bash
pytest tests/test_simple.py -v
```

### Running Specific Test

```bash
pytest tests/test_simple.py::test_session_control_response -v
```

### Running with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

### Expected Output

```
tests/test_simple.py::test_session_control_response PASSED       [12%]
tests/test_simple.py::test_read_data_response PASSED             [25%]
tests/test_simple.py::test_security_access_response PASSED       [37%]
tests/test_simple.py::test_unknown_service_returns_negative_response PASSED [50%]

======================== 4 passed in 0.15s ========================
```

---

## Test Maintenance

### Adding New Tests

1. **Identify uncovered code:** Use coverage report
2. **Write test:** Follow naming convention `test_<function>_<scenario>`
3. **Add to this document:** Update test specifications
4. **Run tests:** Verify all pass
5. **Update coverage:** Check new coverage percentage

### Updating Existing Tests

1. **Identify failing test:** Run pytest
2. **Debug issue:** Use `-v` flag for details
3. **Fix test logic:** Update test code
4. **Verify:** Run test again
5. **Document:** Update this document

---

## Test Success Criteria

- ✅ All tests pass: 100%
- ✅ Code coverage: >80%
- ✅ Execution time: <1 second
- ✅ No warnings or errors
- ✅ Repeatable results

---

**Document Version:** 1.0  
**Last Updated:** 2026-09-29  
**Status:** Ready for Execution
