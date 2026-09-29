# Unit Test Design Integration Guide

**Version:** 1.0  
**Date:** 2026-09-29  
**Purpose:** Document how the Unit Test Design Skill and CSV Validator work together  

---

## Overview

This document explains the new integrated testing workflow that combines:

1. **Unit Test Design Skill** (`docs/UNIT_TEST_DESIGN_SKILL.md`) — Comprehensive workflow for planning and implementing tests
2. **Enhanced CSV Validator** (`docs/validate_csv.py`) — Tool for validating and auto-fixing test specifications
3. **Test Specification CSV** (`docs/test_design.csv`) — Machine-readable, traceability matrix format

Together, these eliminate the need for a separate "test design prompt" or agent, because the Skill is a complete, self-contained workflow.

---

## What Changed

### Before: Manual + Agent-Based

```
User Question
    ↓
GitHub Copilot Agent
    ↓
Suggests Test Design
    ↓
User Manual Implementation
    ↓
Manual CSV Creation
    ↓
No automated validation
```

### After: Skill-Based + Automated

```
Follow Unit Test Design Skill
    ↓
Execute Phases 1-5 with Copilot assistance
    ↓
Create docs/test_design.csv
    ↓
Validate & Auto-Fix: python docs/validate_csv.py --fix
    ↓
Implement tests from validated specs
    ↓
Measure coverage: pytest --cov
```

**Benefits:**
- ✅ Structured, repeatable process
- ✅ No agent dependency
- ✅ Automated validation and fixing
- ✅ Comprehensive documentation
- ✅ Traceability from requirements → tests → code

---

## How to Use the New Workflow

### Step 1: Review the Skill

Read `docs/UNIT_TEST_DESIGN_SKILL.md`:
- Phases 1-5 provide complete guidance
- Workflow takes 3-4 hours for a typical project
- Suitable for any Python project

```bash
# Open and review the skill
cat docs/UNIT_TEST_DESIGN_SKILL.md
```

### Step 2: Execute Phase 1 (Test Strategy)

Define your testing approach:
- Test pyramid (unit/integration/E2E ratio)
- Coverage targets (typically >80%)
- Test categories (positive/negative/edge case)

**With Copilot:**
```
"I'm creating tests for a Python project with 4 modules. 
Help me define a test pyramid with the right number of tests 
and coverage targets"
```

**Output:** Strategy document (or table in markdown)

### Step 3: Execute Phase 2 (Test Specification)

Create CSV with test specifications:

```bash
# Create test_design.csv with columns:
# TCID, TEST CASE NAME, TEST CASE DESCRIPTION, 
# TEST PROCEDURE, EXPECTED RESULTS, VERDICT, PARAMETERS
```

**With Copilot:**
```
"Generate 20 comprehensive test cases in CSV format 
for a diagnostic test automation system with these modules: 
[list modules]. Include positive, negative, and error handling tests."
```

**Output:** `docs/test_design.csv` file

### Step 4: Validate & Auto-Fix CSV

Run the validator to check for issues:

```bash
# Validation-only mode (no changes)
python docs/validate_csv.py

# Validation + auto-fix mode
python docs/validate_csv.py --fix

# Validation + auto-fix + backup
python docs/validate_csv.py --fix --backup
```

**Output:**
```
✅ PASSED (with auto-fixes applied) - 3 fix(es)
  • Added 1 missing column(s)
  • Fixed 2 invalid VERDICT values
  • Generated 1 TCID
```

### Step 5: Execute Phase 3 (Test Implementation)

Implement actual pytest tests based on your CSV:

```bash
# Create test files
mkdir -p tests
touch tests/test_mock_ecu.py
touch tests/test_test_runner.py
touch tests/test_report.py
```

**With Copilot:**
```
"Based on this test specification CSV [paste TC_001 details], 
generate a pytest test function with arrange-act-assert pattern"
```

**Output:** Pytest implementation files

### Step 6: Execute Phase 4 (Coverage Validation)

Measure and report test coverage:

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # or explore in VS Code

# Coverage summary
pytest tests/ --cov=src --cov-report=term-missing
```

**Output:** Coverage report showing >80% target achieved

### Step 7: Execute Phase 5 (Maintenance)

Maintain tests as code evolves:
- Add tests for new features
- Update tests when behavior changes
- Remove tests for deleted code
- Periodically refactor for clarity

---

## CSV Validator Features

### Validation Checks

The validator performs 6 automated checks:

| Check | Purpose | Auto-Fix |
|-------|---------|----------|
| File exists | Ensures CSV file present | ❌ No |
| Valid CSV format | Checks RFC 4180 compliance | ⚠️ Yes |
| Required columns | All 7 columns present | ✅ Yes (adds missing) |
| Unique TCIDs | No duplicate test IDs | ✅ Yes (renames duplicates) |
| Mandatory fields | No empty required fields | ✅ Yes (adds placeholders) |
| Valid verdicts | Only PASS/FAIL/PENDING/SKIP | ✅ Yes (defaults to PASS) |

### Auto-Fix Capability

When you run `python docs/validate_csv.py --fix`, it:

1. **Adds missing columns** — Creates empty columns for any missing
2. **Generates missing TCIDs** — Assigns TC_001, TC_002, etc.
3. **Fills empty mandatory fields** — Uses [TODO: field_name] placeholders
4. **Fixes invalid verdicts** — Replaces invalid values with 'PASS'
5. **Renames duplicate TCIDs** — Appends _DUP_<row> to duplicates
6. **Preserves data** — Never deletes existing data
7. **Creates backups** — Optional --backup flag saves original

### Example Usage

```bash
# Scenario: CSV has issues
$ python docs/validate_csv.py

❌ FAILED - 3 error(s) found:
  ❌ Missing columns: TEST CASE DESCRIPTION, PARAMETERS
  ❌ Row 5: Missing TEST PROCEDURE
  ❌ Invalid VERDICT values: TC_010='PASSED' (should be PASS)

# Auto-fix the issues
$ python docs/validate_csv.py --fix

✅ PASSED (with auto-fixes applied) - 3 fix(es)
  • Added 2 missing column(s)
  • Fixed 1 invalid VERDICT value
  • Generated 1 placeholder field

CSV file auto-fixed and saved: docs/test_design.csv
```

---

## Integration With Your Project

### File Layout

```
GITHUBCOPILOT_TRAINING/
├── docs/
│   ├── DESIGN.md                          # System architecture
│   ├── UNIT_TEST_DESIGN.md                # Test design (original)
│   ├── UNIT_TEST_DESIGN_SKILL.md          # NEW: Comprehensive workflow skill
│   ├── test_design.csv                    # Machine-readable test specs
│   ├── validate_csv.py                    # ENHANCED: With auto-fix
│   ├── CSV_VALIDATION_REPORT.md           # Validation guidance
│   └── CAN_DCOM_Copilot_Requirements.md   # Requirements reference
│
├── tests/
│   ├── __init__.py
│   ├── test_mock_ecu.py                   # Unit tests (TC_001-004)
│   ├── test_test_runner.py                # Unit tests (TC_005-008)
│   ├── test_report.py                     # Unit tests (TC_009-012)
│   └── test_integration.py                # E2E tests (TC_013-020)
│
├── src/
│   ├── __init__.py
│   ├── mock_ecu.py
│   ├── test_runner.py
│   └── report.py
│
├── pytest.ini                             # Pytest configuration
├── requirements.txt                       # pytest, pytest-cov
└── main.py                                # Entry point
```

### Workflow Integration

**Test Design Phase:**
1. Open `docs/UNIT_TEST_DESIGN_SKILL.md` in VS Code
2. Follow Phases 1-5 with GitHub Copilot assistance
3. Create or update `docs/test_design.csv`
4. Run `python docs/validate_csv.py --fix` to clean up
5. Continue to implementation

**Test Implementation Phase:**
1. Refer to `docs/test_design.csv` for TCID → test mapping
2. Create test files in `tests/`
3. Implement each TC_XXX as a pytest test function
4. Run `pytest tests/ -v` to verify all pass

**CI/CD Integration:**
```yaml
# .github/workflows/ci.yml
- name: Run Tests with Coverage
  run: |
    pytest tests/ -v --cov=src --cov-report=xml
    python docs/validate_csv.py  # Validate test specs
```

---

## Why This Replaces the Test Design Prompt/Agent

### Before: Prompt-Based Approach

**Problem:** 
- User asks a question: "How do I design unit tests for my project?"
- Copilot agent responds with a one-time answer
- No reusable structure or validation
- Manual CSV creation and error fixing
- No traceability after initial response

**Limitations:**
- Not repeatable for future projects
- No automated validation
- Errors discovered late (during implementation)
- Hard to maintain and update

### After: Skill-Based Approach

**Solution:**
1. **Skill is complete & self-contained** — All guidance in one file, no agent needed
2. **Workflow is structured** — Phases 1-5 provide clear path
3. **Automated validation** — CSV validator catches issues immediately
4. **Auto-fix capability** — No manual error correction needed
5. **Reusable** — Apply skill to any Python project
6. **Documented** — Easy to onboard new team members

**Advantages:**
- ✅ Same approach every time (consistency)
- ✅ Faster execution (validator automates cleanup)
- ✅ Better quality (validation catches gaps early)
- ✅ No agent dependency (works offline)
- ✅ Team can collaborate using same skill

---

## Examples

### Example 1: New Project

**Scenario:** Starting a new Python project that needs comprehensive test design

**Workflow:**
```bash
# 1. Create project structure
mkdir my-project && cd my-project

# 2. Review skill (takes 20 minutes to understand)
cat docs/UNIT_TEST_DESIGN_SKILL.md

# 3. With Copilot, execute Phases 1-2 (60 min)
#    Output: docs/test_design.csv with 15 test cases

# 4. Validate & auto-fix (2 min)
python docs/validate_csv.py --fix

# 5. Implement tests based on CSV (120 min)
pytest tests/ -v --cov=src
```

**Result:** 15 validated test cases, >80% coverage, zero manual validation work

### Example 2: Adding Feature to Existing Project

**Scenario:** Adding new feature to existing project with tests

**Workflow:**
```bash
# 1. Update test_design.csv with new test cases
#    (e.g., TC_021, TC_022, TC_023 for new feature)

# 2. Validate new test cases
python docs/validate_csv.py

# 3. Implement tests
pytest tests/test_new_feature.py

# 4. Verify coverage target maintained
pytest tests/ --cov=src --cov-report=term-missing
```

**Result:** New tests validated before implementation, maintains coverage

### Example 3: Team Onboarding

**Scenario:** New team member needs to understand testing approach

**Workflow:**
```bash
# 1. Point to skill
"Review docs/UNIT_TEST_DESIGN_SKILL.md for our testing approach"

# 2. Review test specs
"See docs/test_design.csv for all test cases (TC_001 through TC_020)"

# 3. Run validator to verify quality
"python docs/validate_csv.py shows test specs are valid"

# 4. Follow skill to add tests for assigned feature
"Use Phases 1-5 workflow, add your test cases to CSV"
```

**Result:** Consistent, scalable onboarding process

---

## Migration Checklist

If you have existing test design documents, migrate them:

- ✅ Read existing test specifications
- ✅ Create `docs/test_design.csv` with all test cases
- ✅ Run `python docs/validate_csv.py --fix` to validate
- ✅ Review fixes applied (check output)
- ✅ Update tests based on validated specs
- ✅ Archive old test design documents (reference only)
- ✅ Update team to use new skill-based approach

---

## Troubleshooting

### CSV Validator Issues

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python 3.9+, verify `python --version` |
| "File not found" | Ensure `docs/test_design.csv` exists |
| "Invalid CSV format" | Run with `--fix` to auto-correct formatting |
| "Encoding errors" | Validator auto-converts to UTF-8 with `--fix` |
| Backup not created | Use `--backup` flag: `python ... --backup` |

### Test Implementation Issues

| Issue | Solution |
|-------|----------|
| "Test fails unexpectedly" | Review TC_XXX procedure in CSV for expected behavior |
| "Coverage below target" | Review coverage report; add tests for missing lines |
| "TCID mismatch" | Use TCID from CSV exactly; sync before implementation |

---

## Next Steps

1. **Review the Skill** — Read `docs/UNIT_TEST_DESIGN_SKILL.md` thoroughly (30 min)
2. **Validate Existing CSV** — Run `python docs/validate_csv.py` (1 min)
3. **Fix Issues** — Run with `--fix` flag if needed (1 min)
4. **Implement Tests** — Use Phases 3-5 to add/update test implementations (2-4 hours)
5. **Measure Coverage** — Achieve >80% target with `pytest --cov` (30 min)
6. **Update Team** — Share skill link in team documentation

---

## Summary

| Aspect | Before | After |
|--------|--------|-------|
| **How to design tests** | Ask agent each time | Follow reusable skill |
| **Validate test specs** | Manual review | Automated validator |
| **Fix errors** | Manual edits | Auto-fix with `--fix` |
| **Coverage tracking** | Separate process | Integrated in Phase 4 |
| **Onboarding new team** | Repeat explanation | Point to skill |
| **Maintenance** | Ad-hoc | Documented Phase 5 |

**Bottom Line:** The Skill + Validator combination is **faster, more consistent, and automated** compared to a prompt-based agent approach.

---

**Last Updated:** 2026-09-29  
**Status:** Ready for Use  
**Replaces:** Test Design Prompt / Agent (no longer needed)
