# Simple Diagnostic Test Automation

A beginner-friendly Python project for learning GitHub Copilot while building a diagnostic test automation framework.

## What This Project Does

- Reads diagnostic test cases from a JSON file
- Simulates sending diagnostic requests to a mock ECU
- Receives simulated responses
- Validates responses (PASS or FAIL)
- Generates a simple test report

**No real hardware needed!**

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_simple.py

# Run with coverage report
pytest tests/ --cov=src
```

### 3. Run the Application

```bash
python main.py
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── mock_ecu.py          # Simulated ECU
│   ├── test_runner.py       # Test execution logic
│   └── report.py            # Report generation
│
├── tests/
│   ├── __init__.py
│   └── test_simple.py       # Unit tests
│
├── test_data/
│   └── tests.json           # Test cases
│
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Learning Path

This project is designed for a 16-hour GitHub Copilot training:

1. **Hours 1:** Setup Git & Python environment
2. **Hours 2-3:** Write `mock_ecu.py` with Copilot assistance
3. **Hours 4-5:** Write `test_runner.py` with Copilot
4. **Hours 6-7:** Write tests with Copilot
5. **Hours 8-10:** Debug, clean up, and code review
6. **Hours 11-12:** Add GitHub Actions CI/CD
7. **Hours 13-16:** Optional AWS S3 integration and buffer time

## Sample Test Cases

Default test data includes:
- **TC_001:** Diagnostic session control (Positive)
- **TC_002:** Read data by identifier (Positive)
- **TC_003:** Unsupported service (Negative)

## Copilot Tips

Ask Copilot to help with:
- "Write a Python function to load JSON from a file"
- "Generate a simple unit test with pytest"
- "Create a GitHub Actions workflow for Python testing"
- "How do I use environment variables in Python?"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FileNotFoundError` for JSON | Check that `test_data/tests.json` exists |
| Tests won't run | Ensure you're in the virtual environment |

## Resources

- [Python Documentation](https://docs.python.org/)
- [pytest Tutorial](https://docs.pytest.org/)
- [GitHub Copilot](https://github.com/features/copilot)
- [Git Basics](https://git-scm.com/doc)

## License

MIT License - Use this for learning purposes.

---

**Version:** 1.0  
**Last Updated:** 2026-09-28
