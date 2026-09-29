# AI-Assisted CAN/DCOM Diagnostic Test Automation MVP
## Complete Training Requirement Specification

**Training duration:** 16 hours  
**Target audience:** Automotive CAN/DCOM testing team  
**Primary objective:** Learn how GitHub Copilot can support requirement analysis, design, development, test automation, debugging, refactoring, code review, CI/CD, and AWS deployment.  
**Hardware requirement:** **None** — the complete MVP shall run using a simulated/mock ECU and simulated CAN/DCOM communication.

---

# 1. Document Purpose

This document defines a small end-to-end MVP that can be implemented during a 16-hour GitHub Copilot training.

The MVP represents a simplified automotive diagnostic testing workflow. It shall simulate sending diagnostic requests to an ECU, receiving diagnostic responses, validating the responses against expected results, generating a test report, executing the tests automatically in CI/CD, and publishing the generated report to AWS.

The application is intentionally simplified so that the training focuses on engineering workflow and effective use of GitHub Copilot rather than on ECU hardware, CAN hardware, Vector tools, HIL configuration, or proprietary automotive interfaces.

---

# 2. Problem Statement

In an automotive testing environment, a test engineer needs to validate diagnostic request/response behavior.

A typical diagnostic test contains:

- Request CAN ID
- Diagnostic request payload
- Expected response CAN ID
- Expected response payload
- Test case information
- Positive or negative test expectation

For this training, the ECU and CAN communication shall be simulated.

The test automation framework shall:

1. Read diagnostic test cases.
2. Send each request to a simulated ECU.
3. Receive a simulated ECU response.
4. Validate the response.
5. Mark the test as PASS or FAIL.
6. Generate an execution report.
7. Execute automatically through GitHub Actions.
8. Publish the test report/artifacts to AWS S3.

---

# 3. Training Goals

By completing this MVP, trainees should understand how GitHub Copilot can assist with:

- Requirement analysis
- Requirement clarification
- Acceptance criteria creation
- Software design
- Test design
- Python implementation
- Unit test generation
- Negative test generation
- Debugging
- Refactoring
- Documentation
- Code review
- Git workflow
- CI/CD workflow creation
- AWS deployment
- Test report generation

The engineer remains responsible for reviewing, validating, and accepting generated content.

---

# 4. Scope

## 4.1 In Scope

The MVP shall include:

- Python-based implementation
- Diagnostic test case input
- Simulated CAN/DCOM communication
- Simulated ECU
- Diagnostic request processing
- Diagnostic response generation
- Response validation
- Positive test cases
- Negative test cases
- Invalid response scenarios
- Automated test execution
- PASS/FAIL result generation
- JSON or HTML test report
- Unit tests
- Test coverage
- Logging
- Error handling
- Git repository
- GitHub Actions CI pipeline
- Test report artifact
- AWS S3 publication/deployment
- README documentation

## 4.2 Out of Scope

The MVP shall NOT require:

- Real ECU
- Real CAN interface
- Real CAN hardware
- Vector CANoe
- Vector CANalyzer
- CANoe CAPL
- HIL system
- Vehicle network
- Automotive Ethernet hardware
- AUTOSAR implementation
- Embedded C/C++ development
- ECU flashing
- Real UDS stack
- Real diagnostic transport protocol implementation
- Real-time bus timing
- Physical-layer validation
- Measurement equipment
- Proprietary OEM tools
- Production deployment

---

# 5. Assumptions

1. Python 3.x is available.
2. Git is available.
3. The trainees have access to GitHub.
4. GitHub Copilot is available.
5. AWS access is available for the deployment exercise.
6. No physical ECU is available or required.
7. CAN communication is represented using software objects/data structures.
8. The simulated ECU has deterministic responses.
9. Test cases are stored in a human-readable configuration file.
10. The MVP is intended for training and demonstration, not production ECU validation.

---

# 6. High-Level System Overview

The system shall follow this flow:

```text
Test Case Configuration
          |
          v
+-----------------------+
| Test Case Parser      |
+-----------------------+
          |
          v
+-----------------------+
| Diagnostic Executor   |
+-----------------------+
          |
          v
+-----------------------+
| Mock CAN/DCOM Layer   |
+-----------------------+
          |
          v
+-----------------------+
| Simulated ECU         |
+-----------------------+
          |
          v
     Actual Response
          |
          v
+-----------------------+
| Response Validator    |
+-----------------------+
          |
          v
+-----------------------+
| Test Result Collector |
+-----------------------+
          |
          v
+-----------------------+
| Report Generator      |
+-----------------------+
          |
          v
     HTML / JSON Report
          |
          v
     GitHub Actions
          |
          v
        AWS S3
```

---

# 7. Technology Requirements

| Area | Requirement |
|---|---|
| Programming language | Python 3.x |
| Test framework | pytest |
| Configuration | JSON |
| Source control | Git |
| Repository | GitHub |
| AI assistant | GitHub Copilot |
| CI/CD | GitHub Actions |
| Cloud storage | AWS S3 |
| Report | JSON and/or HTML |
| ECU | Software simulation |
| CAN | Software simulation |

---

# 8. Functional Requirements

## FR-001: Test Case Loading

The system shall load diagnostic test cases from a JSON configuration file.

Each test case shall contain:

- Test Case ID
- Description
- Request CAN ID
- Request payload
- Expected Response CAN ID
- Expected response payload
- Test type

Example:

```json
{
  "test_cases": [
    {
      "id": "TC_001",
      "description": "Diagnostic session control - default session",
      "request_can_id": "0x18DA10F1",
      "request": "10 01",
      "expected_response_can_id": "0x18DAF110",
      "expected_response": "50 01",
      "type": "positive"
    }
  ]
}
```

---

## FR-002: Test Case Validation

The system shall validate the structure of each input test case before execution.

The system shall detect at least:

- Missing test case ID
- Missing request CAN ID
- Missing request payload
- Missing expected response CAN ID
- Missing expected response
- Invalid hexadecimal CAN ID
- Invalid hexadecimal payload
- Empty test case

Invalid test data shall produce a meaningful error message.

---

## FR-003: Simulated CAN Message

The system shall represent a CAN message using a software data structure.

A CAN message shall contain at minimum:

- CAN ID
- Payload

Example:

```text
CAN ID: 0x18DA10F1
Payload: 10 01
```

No physical CAN interface shall be used.

---

## FR-004: Simulated ECU

The system shall provide a simulated ECU.

The simulated ECU shall:

1. Receive a diagnostic request.
2. Identify the diagnostic service.
3. Return a predefined response.
4. Return a negative response for unsupported requests.

Example:

```text
Request:
10 01

Response:
50 01
```

Example negative response:

```text
Request:
99 99

Response:
7F 99 11
```

---

# 9. Supported Diagnostic Scenarios

The MVP shall support a small subset of diagnostic-style messages.

The exact services are intentionally limited for training.

## Scenario 1: Diagnostic Session Control

Request:

```text
10 01
```

Expected response:

```text
50 01
```

---

## Scenario 2: Read Data By Identifier

Request:

```text
22 F1 90
```

Expected response:

```text
62 F1 90 XX XX XX
```

For the MVP, the returned data may be fixed.

Example:

```text
62 F1 90 12 34 56
```

---

## Scenario 3: Security Access

Request:

```text
27 01
```

Expected response:

```text
67 01
```

---

## Scenario 4: Unsupported Service

Request:

```text
99 99
```

Expected response:

```text
7F 99 11
```

---

# 10. FR-005: Diagnostic Execution

The system shall execute each valid test case sequentially.

For every test case, the system shall:

1. Read the request.
2. Create a simulated CAN message.
3. Send the message to the simulated ECU.
4. Receive the ECU response.
5. Compare actual and expected CAN IDs.
6. Compare actual and expected payloads.
7. Determine PASS or FAIL.
8. Store the result.

---

# 11. FR-006: Response Validation

The response validator shall validate:

### CAN ID

```text
Expected CAN ID == Actual CAN ID
```

### Payload

```text
Expected Payload == Actual Payload
```

A test shall PASS only when all mandatory expected values match.

A mismatch shall result in FAIL.

---

# 12. FR-007: Positive Test Cases

The framework shall support positive test cases.

Example:

```text
TC_001

Request:
10 01

Expected:
50 01

Actual:
50 01

Result:
PASS
```

---

# 13. FR-008: Negative Test Cases

The framework shall support negative test cases.

Example:

```text
TC_004

Request:
99 99

Expected:
7F 99 11

Actual:
7F 99 11

Result:
PASS
```

A negative test passes when the expected negative response is received.

---

# 14. FR-009: Mismatched Response

The system shall identify an incorrect response.

Example:

```text
Expected:
50 01

Actual:
50 02

Result:
FAIL
```

The failure result shall identify what differed.

---

# 15. FR-010: Missing Response

The simulated ECU shall support a scenario where no response is returned.

The framework shall:

- Detect the missing response.
- Mark the test as FAIL.
- Provide an understandable failure reason.
- Continue executing remaining independent test cases.

---

# 16. FR-011: Invalid Input

The system shall handle malformed input without crashing unexpectedly.

Examples:

```text
Invalid CAN ID
Invalid hexadecimal payload
Missing mandatory field
Empty request
Unsupported data type
```

The system shall provide an actionable error message.

---

# 17. FR-012: Test Result

Every executed test case shall produce a result containing:

- Test Case ID
- Description
- Request CAN ID
- Request payload
- Expected response CAN ID
- Expected response
- Actual response CAN ID
- Actual response
- PASS/FAIL
- Failure reason
- Execution timestamp

Example:

```json
{
  "test_case_id": "TC_001",
  "result": "PASS",
  "failure_reason": null
}
```

---

# 18. FR-013: Test Summary

The framework shall calculate:

- Total tests
- Passed tests
- Failed tests
- Execution duration
- Pass percentage

Example:

```text
Total Tests : 10
Passed      : 8
Failed      : 2
Pass Rate   : 80%
Duration    : 1.25 sec
```

---

# 19. FR-014: Test Report

The system shall generate a machine-readable JSON report.

Optional enhancement: generate an HTML report.

The report shall contain:

1. Execution summary
2. Individual test results
3. Failure details
4. Execution timestamp

---

# 20. FR-015: Exit Code

The command-line application shall return:

```text
0 = all tests passed
1 = one or more tests failed
2 = invalid configuration or execution error
```

This requirement is important for CI/CD integration.

---

# 21. FR-016: Logging

The system shall provide logging for important execution steps.

At minimum:

```text
INFO  Loading test cases
INFO  Executing TC_001
INFO  Sending request
INFO  Receiving response
INFO  Validating response
INFO  TC_001 PASS
INFO  Test execution completed
```

Errors shall be logged appropriately.

---

# 22. Non-Functional Requirements

## NFR-001: Maintainability

The code shall be modular and separated into logical components.

## NFR-002: Readability

The code shall follow standard Python naming and formatting conventions.

## NFR-003: Testability

Core components shall be independently unit-testable.

## NFR-004: Reliability

One failed test case shall not prevent execution of unrelated remaining test cases.

## NFR-005: Error Handling

The system shall provide meaningful errors instead of exposing raw stack traces for expected user/configuration errors.

## NFR-006: Performance

The MVP shall execute the supplied training test suite within a few seconds.

## NFR-007: Portability

The application shall run on Windows and Linux environments without requiring CAN hardware.

## NFR-008: Security

No credentials, access keys, or secrets shall be committed to the Git repository.

---

# 23. Acceptance Criteria

The MVP shall be considered complete when all of the following are true.

## AC-001

The application can load valid test cases from JSON.

## AC-002

The application rejects invalid test case configuration with a meaningful error.

## AC-003

The application can simulate CAN diagnostic requests.

## AC-004

The simulated ECU returns predefined diagnostic responses.

## AC-005

Positive diagnostic scenarios can be validated.

## AC-006

Negative diagnostic scenarios can be validated.

## AC-007

A mismatched response produces FAIL.

## AC-008

A missing response produces FAIL.

## AC-009

All test cases produce structured execution results.

## AC-010

A JSON test report is generated.

## AC-011

The application returns an appropriate process exit code.

## AC-012

Unit tests are available for core components.

## AC-013

The test suite can execute automatically using GitHub Actions.

## AC-014

GitHub Actions publishes the test report as a workflow artifact.

## AC-015

The CI pipeline fails when automated tests fail.

## AC-016

A successful pipeline can publish the generated report to an AWS S3 bucket.

## AC-017

No physical CAN/ECU hardware is required.

---

# 24. Proposed Repository Structure

```text
can-dcom-test-automation/
│
├── README.md
├── requirements.md
├── requirements.txt
├── pytest.ini
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── test_case_parser.py
│   ├── mock_can.py
│   ├── mock_ecu.py
│   ├── diagnostic_executor.py
│   ├── response_validator.py
│   └── report_generator.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_mock_ecu.py
│   ├── test_validator.py
│   ├── test_executor.py
│   └── test_end_to_end.py
│
├── test_data/
│   └── diagnostic_tests.json
│
├── reports/
│   └── .gitkeep
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# 25. Example Test Data

The initial test data shall contain at least the following cases.

```json
{
  "test_cases": [
    {
      "id": "TC_001",
      "description": "Diagnostic session control",
      "request_can_id": "0x18DA10F1",
      "request": "10 01",
      "expected_response_can_id": "0x18DAF110",
      "expected_response": "50 01",
      "type": "positive"
    },
    {
      "id": "TC_002",
      "description": "Read data by identifier",
      "request_can_id": "0x18DA10F1",
      "request": "22 F1 90",
      "expected_response_can_id": "0x18DAF110",
      "expected_response": "62 F1 90 12 34 56",
      "type": "positive"
    },
    {
      "id": "TC_003",
      "description": "Security access request",
      "request_can_id": "0x18DA10F1",
      "request": "27 01",
      "expected_response_can_id": "0x18DAF110",
      "expected_response": "67 01",
      "type": "positive"
    },
    {
      "id": "TC_004",
      "description": "Unsupported diagnostic service",
      "request_can_id": "0x18DA10F1",
      "request": "99 99",
      "expected_response_can_id": "0x18DAF110",
      "expected_response": "7F 99 11",
      "type": "negative"
    }
  ]
}
```

---

# 26. Required Automated Tests

The training implementation shall include tests for:

## Parser

- Valid configuration
- Missing mandatory field
- Invalid CAN ID
- Invalid payload
- Empty configuration

## Mock CAN

- Message creation
- CAN ID handling
- Payload handling

## Mock ECU

- Supported diagnostic request
- Unsupported diagnostic request
- No-response scenario

## Validator

- Matching CAN ID and payload
- Wrong CAN ID
- Wrong payload
- Missing response
- Empty response

## Executor

- Successful execution
- Failed test execution
- Multiple test cases
- Continuation after individual test failure

## End-to-End

At least one complete flow:

```text
JSON test case
     ↓
Executor
     ↓
Mock CAN
     ↓
Mock ECU
     ↓
Validator
     ↓
Result
     ↓
Report
```

---

# 27. Deliberate Defects for Training

After the first successful implementation, the trainer may introduce controlled defects.

Suggested defects:

### Defect 1 — Incorrect PASS/FAIL logic

Expected:

```python
actual == expected
```

Changed intentionally to:

```python
actual != expected
```

### Defect 2 — Partial payload validation

Only part of the response is compared.

### Defect 3 — CAN ID ignored

The implementation validates payload but does not validate CAN ID.

### Defect 4 — Missing response handled incorrectly

A missing response causes an exception instead of producing a controlled FAIL result.

### Defect 5 — CI exit code

The application generates a failed report but still returns exit code 0.

These defects create hands-on opportunities for:

- Copilot debugging
- Root-cause analysis
- Test generation
- Code review
- Refactoring

---

# 28. GitHub Copilot Training Opportunities

The same requirement shall be used throughout the training rather than giving isolated coding exercises.

## Phase 1 — Requirement Analysis

Prompt Copilot to:

- Identify functional requirements.
- Identify non-functional requirements.
- Find ambiguities.
- Generate acceptance criteria.
- Identify missing negative scenarios.
- Convert requirements into testable statements.

## Phase 2 — Design

Prompt Copilot to:

- Propose architecture.
- Identify modules.
- Define interfaces.
- Identify dependencies.
- Explain design trade-offs.

## Phase 3 — Development

Prompt Copilot to:

- Generate Python classes.
- Implement parsing.
- Implement mock ECU behavior.
- Implement validation.
- Implement reporting.

## Phase 4 — Test Automation

Prompt Copilot to:

- Generate pytest tests.
- Identify boundary conditions.
- Generate negative tests.
- Improve test coverage.
- Explain failing tests.

## Phase 5 — Debugging

Use deliberately introduced defects.

Prompt Copilot to:

- Analyze failing tests.
- Identify likely root cause.
- Suggest a fix.
- Explain why the fix works.
- Generate a regression test.

## Phase 6 — Refactoring

Prompt Copilot to:

- Identify duplication.
- Identify code smells.
- Improve modularity.
- Improve naming.
- Preserve existing behavior.

## Phase 7 — Code Review

Ask Copilot to review a pull request for:

- Functional defects
- Missing error handling
- Missing tests
- Security concerns
- Maintainability
- CI/CD impact

## Phase 8 — CI/CD

Ask Copilot to create a GitHub Actions workflow that:

1. Checks out the repository.
2. Installs Python.
3. Installs dependencies.
4. Executes pytest.
5. Generates the report.
6. Uploads the report as an artifact.
7. Fails the workflow when tests fail.

## Phase 9 — AWS

Ask Copilot to assist with:

- AWS CLI commands.
- S3 upload steps.
- GitHub Actions AWS integration.
- Environment variables/secrets.
- Deployment documentation.

---

# 29. CI/CD Requirements

The GitHub Actions pipeline shall execute on:

- Push to the main branch
- Pull request to the main branch

The pipeline shall perform:

```text
Checkout
   ↓
Setup Python
   ↓
Install Dependencies
   ↓
Run Unit Tests
   ↓
Run Integration Tests
   ↓
Generate Test Report
   ↓
Upload Report Artifact
```

The workflow shall fail if automated tests fail.

---

# 30. AWS Deployment Requirements

AWS S3 shall be used as the deployment target for the training MVP.

The CI/CD workflow shall publish the generated report to an S3 bucket after successful validation.

Example:

```text
GitHub
   |
   v
GitHub Actions
   |
   +-- pytest
   |
   +-- report generation
   |
   v
AWS S3
   |
   +-- latest/report.html
   +-- latest/results.json
```

The exact AWS account, bucket name, region, and credentials shall be provided separately by the training environment.

AWS credentials shall never be hard-coded in source code.

GitHub Actions secrets or an appropriate AWS authentication mechanism shall be used.

---

# 31. Deployment Acceptance Criteria

The AWS portion is complete when:

1. CI executes successfully.
2. Test cases execute automatically.
3. Test results are generated.
4. The report is available as a GitHub Actions artifact.
5. The successful pipeline publishes the report to S3.
6. The S3 object can be verified.
7. No AWS credentials are present in source code.

---

# 32. Definition of Done

The MVP is complete when:

- [ ] Requirements are documented.
- [ ] Repository is created.
- [ ] Python environment is configured.
- [ ] Test data is available.
- [ ] Mock CAN layer is implemented.
- [ ] Mock ECU is implemented.
- [ ] Diagnostic executor is implemented.
- [ ] Response validator is implemented.
- [ ] Positive tests are implemented.
- [ ] Negative tests are implemented.
- [ ] Error handling is implemented.
- [ ] Test report is generated.
- [ ] Unit tests pass.
- [ ] Code has been reviewed.
- [ ] Code has been refactored.
- [ ] CI pipeline is working.
- [ ] Test reports are stored as CI artifacts.
- [ ] AWS S3 deployment is working.
- [ ] README explains how to run the application.
- [ ] No real ECU or CAN hardware is required.

---

# 33. 16-Hour Training Mapping

| Stage | Activity | Duration |
|---|---|---:|
| 1 | GitHub + Copilot introduction | 1.0 hr |
| 2 | Requirement analysis | 1.5 hr |
| 3 | Design and architecture | 1.5 hr |
| 4 | Python implementation | 2.5 hr |
| 5 | Test automation | 2.5 hr |
| 6 | Debugging with deliberate defects | 1.5 hr |
| 7 | Refactoring | 1.0 hr |
| 8 | Code review | 1.0 hr |
| 9 | GitHub Actions CI/CD | 1.5 hr |
| 10 | AWS S3 deployment | 1.0 hr |
| **Total** | | **16.0 hr** |

---

# 34. Expected Final Deliverable

At the end of the training, each team should have a GitHub repository containing:

```text
can-dcom-test-automation
│
├── Requirements
├── Python implementation
├── Mock ECU
├── Mock CAN interface
├── Diagnostic test data
├── Automated tests
├── Test reports
├── Documentation
├── GitHub Actions workflow
└── AWS deployment configuration
```

The final demonstration should show:

```text
1. Modify a diagnostic test case
          ↓
2. Commit and push
          ↓
3. GitHub Actions starts
          ↓
4. Automated tests execute
          ↓
5. PASS/FAIL results generated
          ↓
6. Report generated
          ↓
7. Report uploaded to AWS S3
```

---

# 35. Training Success Criteria

The training should not be measured only by whether the generated application works.

Participants should demonstrate that they can use GitHub Copilot to:

1. Understand a requirement.
2. Question an ambiguous requirement.
3. Convert requirements into acceptance criteria.
4. Design a solution before coding.
5. Generate and modify implementation code.
6. Generate meaningful automated tests.
7. Identify missing test scenarios.
8. Debug AI-generated or human-written code.
9. Refactor safely.
10. Perform an engineering-focused code review.
11. Build a CI pipeline.
12. Deploy an artifact to AWS.
13. Critically review Copilot output instead of accepting it blindly.

---

# 36. Training Constraint

The MVP shall remain intentionally small.

The objective is **not** to build a complete automotive diagnostic framework.

The objective is to provide a realistic CAN/DCOM testing scenario through which participants can experience the complete software engineering lifecycle with GitHub Copilot:

```text
Requirement
    ↓
Analysis
    ↓
Design
    ↓
Implementation
    ↓
Test Automation
    ↓
Debug
    ↓
Refactor
    ↓
Review
    ↓
CI/CD
    ↓
AWS
```

This scope shall be sufficient for the 16-hour training while remaining achievable without real automotive hardware.
