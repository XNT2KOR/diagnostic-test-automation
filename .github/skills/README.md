# Skills Directory

This directory contains reusable workflow skills for the GitHub Copilot Training project.

**Skills** are structured guides that provide step-by-step workflows for common tasks, designed to be:
- ✅ **Repeatable** — Same approach every time
- ✅ **Self-contained** — All guidance in one file, no agent needed
- ✅ **Learner-friendly** — Clear phases with examples and best practices
- ✅ **Integrated** — Works with automated tools (CSV validator, pytest, etc.)

---

## Available Skills

### 1. Unit Test Design for Python Projects

**File:** [`unit-test-design.md`](unit-test-design.md)

**Purpose:** Comprehensive workflow for designing and implementing unit tests for Python projects.

**5-Phase Workflow:**
1. **Test Strategy Definition** (30-45 min) — Define pyramid, coverage targets, test categories
2. **Test Specification** (45-60 min) — Document test cases with procedures and expected results
3. **Test Implementation** (1-2 hours) — Write actual pytest tests
4. **Coverage Validation** (15-30 min) — Measure and report code coverage
5. **Test Maintenance** (Ongoing) — Keep tests updated as code evolves

**When to Use:**
- Starting a new Python project
- Adding significant new functionality
- Improving test coverage
- Onboarding team members to testing standards

**Tools & Integrations:**
- pytest (test runner)
- pytest-cov (coverage measurement)
- CSV validator (`docs/validate_csv.py`) — Validate test specifications
- GitHub Copilot — Assist with test generation

**Time to Complete:** 3-4 hours

---

### 2. Integration Guide

**File:** [`integration-guide.md`](integration-guide.md)

**Purpose:** Explains how the Unit Test Design Skill works with the CSV Validator and test specification CSV.

**Key Topics:**
- How the skill replaces test design prompts/agents
- Step-by-step workflow using the skill
- CSV validator features (validation, auto-fix)
- Integration with your project structure
- Examples and use cases
- Migration checklist

**When to Use:**
- Understanding the overall testing workflow
- Setting up test design for a team
- Integrating tests into CI/CD pipeline
- Migrating from manual test design

**Time to Read:** 30-45 minutes

---

## Quick Start

### For Individual Contributors

1. **Read the Skill**
   ```bash
   cat .github/skills/unit-test-design.md
   ```

2. **Follow Phases 1-5** with GitHub Copilot assistance

3. **Validate Test Specifications**
   ```bash
   python docs/validate_csv.py --fix
   ```

4. **Implement and Run Tests**
   ```bash
   pytest tests/ -v --cov=src
   ```

### For Team Lead / Onboarding

1. **Review Integration Guide**
   ```bash
   cat .github/skills/integration-guide.md
   ```

2. **Share Skill Reference**
   - Point team members to `.github/skills/unit-test-design.md`
   - Use Integration Guide for policy/process discussions

3. **Set Up CI/CD**
   - Integrate CSV validation into workflow
   - Run tests automatically on push/PR

---

## How Skills Compare to Agents

| Aspect | Agent | Skill |
|--------|-------|-------|
| **Reusability** | One-time answer | Repeatable workflow |
| **Structure** | Varies | Consistent 5-phase approach |
| **Automation** | Manual steps | Integrated with validator/pytest |
| **Offline Use** | Requires Copilot | Works standalone |
| **Team Consistency** | Depends on prompt | Consistent for everyone |
| **Maintenance** | Update prompt each time | Update skill once |

**Bottom Line:** Skills provide structured, repeatable workflows that work with automation and scale across teams.

---

## File Structure

```
.github/
└── skills/
    ├── README.md                    # This file
    ├── unit-test-design.md          # Main skill (5-phase workflow)
    └── integration-guide.md         # How skill + validator work together
```

---

## Tools & Resources

| Tool | Purpose | Location |
|------|---------|----------|
| **CSV Validator** | Validate and auto-fix test specs | `docs/validate_csv.py` |
| **Test Data** | Test case specifications | `docs/test_design.csv` |
| **pytest** | Test runner | Python package (requirements.txt) |
| **pytest-cov** | Coverage measurement | Python package (requirements.txt) |

---

## Related Documentation

- **System Design** — See [`docs/DESIGN.md`](../../docs/DESIGN.md)
- **Original Test Design** — See [`docs/UNIT_TEST_DESIGN.md`](../../docs/UNIT_TEST_DESIGN.md) (reference)
- **Requirements** — See [`docs/CAN_DCOM_Copilot_Requirements.md`](../../docs/CAN_DCOM_Copilot_Requirements.md)
- **Copilot Guidance** — See [`.github/copilot-instructions.md`](../copilot-instructions.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-09-29 | Initial skills directory with Unit Test Design skill |

---

## Contributing to Skills

To add a new skill:

1. Create a new `.md` file in this directory
2. Follow the skill template:
   - Overview section
   - When to use / When NOT to use
   - Step-by-step phases or workflow
   - Examples and best practices
   - Troubleshooting
   - Related resources
3. Update this README with the new skill reference
4. Share with team for feedback

---

**Last Updated:** 2026-09-29  
**Status:** ✅ Active  
**Maintainer:** GitHub Copilot Training Project
