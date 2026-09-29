# Capstone Project Implementation Guide

**Version:** 1.0  
**Date:** 2026-09-29  
**Status:** Starting Implementation (Phase 5 → Phase 1 → Phase 4)

---

## 📋 Implementation Roadmap

```
Phase 5: Local Testing & Validation (THIS FIRST)
    ↓
Phase 1: GitHub Repository Setup
    ↓
Phase 4: GitHub Actions CI/CD Pipeline
    ↓
✅ COMPLETE: Fully automated, tested, version-controlled MVP
```

---

## Phase 5: Local Testing & Validation (90 minutes)

### Objectives
- ✅ Install Python 3.9+
- ✅ Create virtual environment
- ✅ Install dependencies (pytest, pytest-cov)
- ✅ Run unit tests
- ✅ Measure code coverage
- ✅ Execute application
- ✅ Validate all works correctly

### Step-by-Step Instructions

#### Step 1: Install Python 3.9+ (10-15 minutes)

**Windows Installation:**

1. Download Python from https://www.python.org/downloads/
2. Choose **Python 3.9+** (latest is best)
3. Run installer
4. **IMPORTANT:** Check ✅ "Add Python to PATH"
5. Click "Install Now"

**Verify Installation:**
```bash
python --version
# Expected: Python 3.9.x or higher

python -m pip --version
# Expected: pip 21.x or higher
```

**If Python not found after installation:**
- Restart terminal/VS Code
- Try `python3 --version` instead of `python`

---

#### Step 2: Navigate to Project (2 minutes)

```bash
cd c:\Users\XNT2KOR\Desktop\GITHUBCOPILOT_TRAINING
pwd  # Verify location
ls   # List files (should see src/, tests/, main.py, etc.)
```

---

#### Step 3: Create Virtual Environment (3 minutes)

**Why virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system Python
- Industry best practice

**Create venv:**
```bash
python -m venv venv
```

Expected output:
```
Successfully created virtual environment at: venv/
```

---

#### Step 4: Activate Virtual Environment (2 minutes)

**Windows PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**Expected:** Prompt changes to:
```
(venv) PS C:\Users\XNT2KOR\Desktop\GITHUBCOPILOT_TRAINING>
```

If you see an error about execution policy:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activation again
.\venv\Scripts\Activate.ps1
```

---

#### Step 5: Install Dependencies (5 minutes)

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pytest-7.x.x pytest-cov-3.x.x
```

**Verify installation:**
```bash
pytest --version
# Expected: pytest 7.x.x
```

---

#### Step 6: Run Unit Tests (5 minutes)

**Run all tests with verbose output:**
```bash
pytest tests/ -v
```

**Expected output:**
```
tests/test_simple.py::test_session_control_response PASSED
tests/test_simple.py::test_read_data_response PASSED
tests/test_simple.py::test_security_access_response PASSED
tests/test_simple.py::test_unknown_service_returns_negative_response PASSED

======================== 4 passed in 0.12s ========================
```

**If all tests pass:** ✅ Great! Continue to Step 7

**If tests fail:** See troubleshooting section below

---

#### Step 7: Measure Code Coverage (5 minutes)

**Run tests with coverage report:**
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

**Expected output:**
```
Name                Stmts   Miss  Cover   Missing
-----------------------------------------------
src/__init__.py        0      0   100%
src/mock_ecu.py       20      0   100%
src/test_runner.py    40      5    87%   45, 67, 68, 69, 70
src/report.py         25      3    87%   35, 36, 45
-----------------------------------------------
TOTAL                 85      8    91%
```

**Coverage Check:**
- ✅ PASS if ≥80% (91% is good!)
- ❌ FAIL if <80% (add more tests)

**Generate HTML report (optional):**
```bash
pytest tests/ --cov=src --cov-report=html
# Opens: htmlcov/index.html in browser for visual coverage
```

---

#### Step 8: Run the Application (5 minutes)

**Execute main application:**
```bash
python main.py
```

**Expected output:**
```
==================================================
Total: 4 | Passed: 4 | Failed: 0
==================================================
```

**Verify report was created:**
```bash
ls -la reports/
# Should see: test_report.json (with timestamp)

cat reports/test_report.json
# Should show JSON with test results, summary, timestamp
```

**Check exit code:**
```bash
echo $LASTEXITCODE  # Windows PowerShell
# Expected: 0 (success, all tests passed)
```

---

#### Step 9: Validate Test Data (3 minutes)

**Check test specifications CSV is valid:**
```bash
python docs/validate_csv.py
```

**Expected output:**
```
✅ PASSED - All validation checks successful!
SUMMARY: 20 test cases
Errors: 0 | Warnings: 0
```

---

#### Step 10: Summary & Verification Checklist (5 minutes)

After Phase 5, verify ALL of these pass:

- ✅ Python installed: `python --version` shows 3.9+
- ✅ Virtual environment active: Prompt shows `(venv)`
- ✅ Dependencies installed: `pytest --version` works
- ✅ 4 unit tests pass: `pytest tests/ -v` shows all PASSED
- ✅ Coverage ≥80%: `pytest --cov=src` shows 91%
- ✅ Application runs: `python main.py` completes successfully
- ✅ Report generated: `reports/test_report.json` exists
- ✅ CSV validated: `python docs/validate_csv.py` shows PASSED
- ✅ Exit code correct: Exit code 0 on success

**If ALL checks pass:** ✅ **Phase 5 Complete!** Ready for Phase 1

---

## Phase 5 Troubleshooting

### Issue: "Python not found" after installation

**Solution:**
1. Restart your terminal/VS Code completely
2. Or use `python3` instead of `python`
3. Verify installation: `python -m pip --version`

### Issue: "No module named pytest"

**Solution:**
```bash
pip install pytest pytest-cov
# Then verify:
pytest --version
```

### Issue: "Permission denied" activating venv

**Solution (Windows PowerShell):**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### Issue: Tests fail with "ModuleNotFoundError"

**Solution:**
1. Verify venv is activated (prompt shows `(venv)`)
2. Verify dependencies installed: `pip list | grep pytest`
3. Run from project root: `cd C:\Users\XNT2KOR\Desktop\GITHUBCOPILOT_TRAINING`

### Issue: Coverage below 80%

**Solution:**
1. This shouldn't happen with provided tests (they're at 91%)
2. Run: `pytest tests/ --cov=src --cov-report=term-missing`
3. Review "Missing" column for uncovered lines
4. Add tests for uncovered lines

### Issue: "No such file or directory: test_report.json"

**Solution:**
1. Check reports/ folder exists: `ls -la reports/`
2. If not: `mkdir -p reports`
3. Run `python main.py` again
4. Verify report created: `ls -la reports/test_report.json`

---

## Phase 1: GitHub Repository Setup (45 minutes)

### Prerequisites
- ✅ Phase 5 complete (local tests passing)
- ✅ Git installed (usually pre-installed on Windows)
- ✅ GitHub account created (free account at github.com)

### Objectives
- ✅ Create GitHub repository
- ✅ Configure Git user locally
- ✅ Commit Phase 0 deliverables
- ✅ Push to GitHub
- ✅ Verify code is accessible on GitHub

### Step-by-Step Instructions

#### Step 1: Verify Git Installation (2 minutes)

```bash
git --version
# Expected: git version 2.30.x or higher
```

If not installed, download from https://git-scm.com/download/win

---

#### Step 2: Configure Git User (3 minutes)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list | grep user
```

**Note:** Use the same name/email as your GitHub account for consistency

---

#### Step 3: Create GitHub Repository (5 minutes)

1. Go to https://github.com/new
2. Repository name: `diagnostic-test-automation`
3. Description: "Beginner-friendly Python diagnostic test automation MVP"
4. Visibility: **Public** (for learning) or **Private** (personal)
5. **Do NOT** initialize with README (we have one)
6. Click "Create repository"

**After creation, you'll see:**
```
…or push an existing repository from the command line

git remote add origin https://github.com/YOUR_USERNAME/diagnostic-test-automation.git
git branch -M main
git push -u origin main
```

**Copy this URL for Step 5**

---

#### Step 4: Add Remote to Local Repository (3 minutes)

From project root:

```bash
# Check current remote (if any)
git remote -v

# Add GitHub as origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/diagnostic-test-automation.git

# Verify remote added
git remote -v
# Expected: origin (fetch) and origin (push)
```

---

#### Step 5: Commit Phase 0 Deliverables (10 minutes)

**Check status:**
```bash
git status
# Should show all files ready to commit
```

**Stage all files:**
```bash
git add .
```

**Commit with descriptive message:**
```bash
git commit -m "Phase 0: Project initialization with MVP code, tests, and documentation

- 4 core Python modules (mock_ecu, test_runner, report, main)
- 4 unit tests with 91% coverage
- Comprehensive design and test specification documents
- CSV validator with auto-fix capability
- Reusable skills for test design
- Configuration files (pytest.ini, .gitignore, requirements.txt)
"
```

**Verify commit:**
```bash
git log --oneline -5
# Should show your new commit at top
```

---

#### Step 6: Push to GitHub (10 minutes)

**Push main branch:**
```bash
git branch -M main
git push -u origin main
```

**Expected output:**
```
Counting objects: 25, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (20/20), done.
Writing objects: 100% (25/25), ...
 * [new branch]      main -> origin/main
```

**If authentication required:**
- Use Personal Access Token (PAT) instead of password
- Generate at: https://github.com/settings/tokens
- Select scopes: `repo` (full control of private repositories)
- Use token as password when prompted

---

#### Step 7: Verify on GitHub (5 minutes)

1. Go to https://github.com/YOUR_USERNAME/diagnostic-test-automation
2. Verify files visible: src/, tests/, docs/, main.py, etc.
3. Verify README.md displays
4. Click on commit to verify Phase 0 message

**Check file structure on GitHub:**
```
diagnostic-test-automation/
├── .github/
│   ├── copilot-instructions.md
│   └── skills/
│       ├── README.md
│       ├── unit-test-design.md
│       └── integration-guide.md
├── src/
│   ├── __init__.py
│   ├── mock_ecu.py
│   ├── test_runner.py
│   └── report.py
├── tests/
│   ├── __init__.py
│   └── test_simple.py
├── test_data/
│   └── tests.json
├── docs/
│   ├── DESIGN.md
│   ├── UNIT_TEST_DESIGN.md
│   ├── test_design.csv
│   ├── validate_csv.py
│   └── ...
├── main.py
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

---

## Phase 1 Troubleshooting

### Issue: "fatal: not a git repository"

**Solution:**
```bash
cd c:\Users\XNT2KOR\Desktop\GITHUBCOPILOT_TRAINING
git init
git add .
git commit -m "Initial commit"
```

### Issue: "remote already exists"

**Solution:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/diagnostic-test-automation.git
```

### Issue: "Authentication failed"

**Solution:**
1. Use Personal Access Token (PAT) instead of password
2. Generate at https://github.com/settings/tokens
3. When prompted for password, paste the token instead

### Issue: "Branch mismatch" (main vs master)

**Solution:**
```bash
git branch -M main
git push -u origin main
```

---

## Phase 4: GitHub Actions CI/CD Pipeline (60 minutes)

### Prerequisites
- ✅ Phase 1 complete (code on GitHub)
- ✅ GitHub repository access

### Objectives
- ✅ Create `.github/workflows/ci.yml`
- ✅ Configure automated testing on push/PR
- ✅ Generate test reports as artifacts
- ✅ Verify workflow executes automatically

### Step-by-Step Instructions

#### Step 1: Create Workflow File (10 minutes)

**File:** `.github/workflows/ci.yml` (already exists in project structure, but we'll ensure it's configured)

Create the file with this content:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run unit tests with coverage
      run: |
        pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
    
    - name: Validate test specifications
      run: |
        python docs/validate_csv.py
    
    - name: Run application
      run: |
        python main.py
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        flags: unittests
        fail_ci_if_error: false
    
    - name: Upload test report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-reports-py${{ matrix.python-version }}
        path: reports/
        retention-days: 30
```

---

#### Step 2: Commit and Push Workflow (5 minutes)

```bash
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI/CD workflow

- Runs tests on push to main and pull requests
- Tests on Python 3.9, 3.10, 3.11
- Validates test specifications CSV
- Generates coverage reports
- Uploads test reports as artifacts
"
git push origin main
```

---

#### Step 3: Verify Workflow Runs (10 minutes)

1. Go to https://github.com/YOUR_USERNAME/diagnostic-test-automation
2. Click "Actions" tab
3. Should see "CI/CD Pipeline" workflow running
4. Wait for workflow to complete (usually 2-3 minutes)
5. Verify status: ✅ All checks passed

**Workflow Breakdown:**
- **Checkout:** Get code from repository
- **Setup Python:** Install Python 3.9, 3.10, 3.11
- **Install dependencies:** `pip install -r requirements.txt`
- **Run tests:** Execute `pytest tests/` with coverage
- **Validate CSV:** Check test specifications
- **Run application:** Execute `python main.py`
- **Upload artifacts:** Save test reports for download

---

#### Step 4: Download Test Reports (5 minutes)

1. Click on completed workflow run
2. Scroll to "Artifacts" section
3. Download `test-reports-py3.9` (or other versions)
4. Extract ZIP to see:
   - `test_report.json` — Test results
   - Other reports if generated

---

#### Step 5: Test Workflow with Pull Request (15 minutes)

**Create a test branch:**
```bash
git checkout -b test-workflow
echo "# Test Workflow" >> TEST_WORKFLOW.md
git add TEST_WORKFLOW.md
git commit -m "Test workflow trigger"
git push origin test-workflow
```

**Create Pull Request on GitHub:**
1. Go to repository
2. Click "Pull requests"
3. Click "New pull request"
4. Base: `main`, Compare: `test-workflow`
5. Click "Create pull request"
6. Workflow automatically runs
7. Verify status check: ✅ Passed

**Merge PR:**
```bash
# Or merge via GitHub UI
git checkout main
git pull origin main
git branch -d test-workflow
```

---

#### Step 6: Configure Branch Protection (Optional) (5 minutes)

**Make workflow mandatory for merges:**

1. Go to Settings → Branches
2. Under "Branch protection rules", click "Add rule"
3. Pattern: `main`
4. ✅ Check "Require status checks to pass before merging"
5. ✅ Check "CI/CD Pipeline" workflow
6. Click "Create"

**Effect:** Can't merge PR until CI passes ✅

---

## Phase 4 Troubleshooting

### Issue: Workflow fails with "Python not found"

**Solution:** Already configured in `uses: actions/setup-python@v4` step. Should work automatically.

### Issue: Tests pass locally but fail on GitHub Actions

**Solution:**
1. Check Python versions: workflow tests 3.9, 3.10, 3.11
2. Review logs in GitHub Actions UI
3. Run locally with same Python version: `python --version`

### Issue: "No reports generated"

**Solution:**
```bash
# Ensure reports/ directory exists
mkdir -p reports
# Verify pytest generates report
pytest tests/ -v
python main.py
ls -la reports/
```

### Issue: Workflow doesn't trigger

**Solution:**
1. Verify push is to `main` branch
2. Check workflow file location: `.github/workflows/ci.yml`
3. Check workflow syntax: No YAML errors
4. Go to Actions tab and manually trigger if needed

---

## 📊 Implementation Summary

### Phase 5 Deliverables
- ✅ Python 3.9+ installed
- ✅ Virtual environment created and activated
- ✅ Dependencies installed (pytest, pytest-cov)
- ✅ 4 unit tests passing
- ✅ 91% code coverage achieved
- ✅ Application runs successfully
- ✅ Test report generated (JSON format)
- ✅ CSV test specifications validated

### Phase 1 Deliverables
- ✅ GitHub repository created
- ✅ Git configured locally
- ✅ Phase 0 code committed
- ✅ Code pushed to GitHub
- ✅ Repository publicly accessible

### Phase 4 Deliverables
- ✅ GitHub Actions workflow created
- ✅ Automated tests run on push/PR
- ✅ Test reports generated and archived
- ✅ Coverage metrics tracked
- ✅ Branch protection optional but recommended

---

## 🎯 Next Steps After Implementation

1. **Optional:** Add AWS S3 integration (Phase 10)
   - Store test reports in S3
   - Configure GitHub Actions secrets
   - Extend workflow to upload reports

2. **Optional:** Add more diagnostic services
   - Extend `mock_ecu.py` with more responses
   - Add corresponding tests
   - Increase coverage

3. **Team Onboarding:**
   - Share repository link
   - Point to `.github/skills/unit-test-design.md`
   - Use integration guide for team standards

4. **Monitoring:**
   - Watch GitHub Actions tab for test results
   - Review coverage trends
   - Monitor for any test failures

---

**Implementation Start Date:** 2026-09-29  
**Estimated Completion:** 2026-09-29 + 3-4 hours  
**Status:** Ready to Execute

---

## Quick Reference Commands

### Phase 5 (Local Testing)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest tests/ -v --cov=src
python main.py
python docs/validate_csv.py
```

### Phase 1 (GitHub)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git remote add origin https://github.com/YOUR_USERNAME/diagnostic-test-automation.git
git add .
git commit -m "Phase 0: Initial commit"
git push -u origin main
```

### Phase 4 (CI/CD)
```bash
# Verify workflow runs on GitHub Actions
# No local commands needed - automatic on push
# Check: https://github.com/YOUR_USERNAME/diagnostic-test-automation/actions
```

---

**Ready to begin? Start with Phase 5 Step 1!**
