# SOP: Running Tests

**version: v1.0.0**

## When to Use

Run tests whenever you:
- Add new features or make code changes
- Fix bugs
- Refactor code
- Before creating pull requests
- Before deploying/releasing new versions
- As part of continuous integration

## Test Types

The project includes three types of tests:

1. **Unit Tests** - Test individual functions and modules
2. **Integration Tests** - Test component interactions
3. **GUI Tests** - Test dashboard functionality (Playwright)

## Prerequisites

### Install Test Dependencies

```bash
# Production + development dependencies
pip install -e ".[dev]"

# Or install test dependencies individually
pip install pytest pytest-cov playwright

# Install Playwright browsers (for GUI tests)
playwright install
```

### Test Structure

```
tests/
├── __init__.py
├── test_main.py                    # Main module tests
├── test_verification_system.py     # Verification tests
├── test_dashboard_playwright.py    # GUI automated tests
└── fixtures/                       # Test data files
    └── test_customer_database.json
```

## Running Unit Tests

### Run All Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=src

# Run with detailed coverage report
pytest tests/ -v --cov=src --cov-report=html
```

**Expected Output:**
```
tests/test_main.py::test_function_1 PASSED
tests/test_main.py::test_function_2 PASSED
tests/test_verification_system.py::test_verify_customer PASSED

========== 15 passed in 2.34s ==========

---------- coverage: 85% ----------
```

### Run Specific Test File

```bash
# Run single test file
pytest tests/test_verification_system.py -v

# Run with coverage for specific module
pytest tests/test_verification_system.py -v --cov=src.verification_system
```

### Run Specific Test Function

```bash
# Run single test function
pytest tests/test_verification_system.py::test_verify_customer -v

# Run tests matching pattern
pytest tests/ -k "verification" -v
```

### Run Tests with Different Output Modes

```bash
# Quiet mode (minimal output)
pytest tests/ -q

# Very verbose (show full diffs)
pytest tests/ -vv

# Show print statements
pytest tests/ -v -s

# Stop at first failure
pytest tests/ -x

# Run last failed tests only
pytest tests/ --lf
```

## Running GUI Tests (Playwright)

### Setup Playwright

```bash
# Install playwright and browsers
pip install playwright
playwright install chromium
```

### Run GUI Tests

```bash
# Run dashboard GUI tests
pytest tests/test_dashboard_playwright.py -v

# Run with headed browser (visible)
pytest tests/test_dashboard_playwright.py -v --headed

# Run with slow motion (debugging)
pytest tests/test_dashboard_playwright.py -v --headed --slowmo=1000
```

**Note:** GUI tests may require dashboard to not be running.

### GUI Test Features

- Window creation and initialization
- Button clicks and interactions
- Customer selection
- Verification console output
- Email generation workflow

## Coverage Reports

### Generate HTML Coverage Report

```bash
# Generate HTML report
pytest tests/ --cov=src --cov-report=html

# Open report (Windows)
start htmlcov/index.html

# Open report (Linux/Mac)
open htmlcov/index.html
```

### Coverage Report Formats

```bash
# Terminal report
pytest tests/ --cov=src --cov-report=term

# Terminal with missing lines
pytest tests/ --cov=src --cov-report=term-missing

# HTML report
pytest tests/ --cov=src --cov-report=html

# XML report (for CI/CD)
pytest tests/ --cov=src --cov-report=xml
```

### Coverage Targets

| Component | Target | Current |
|-----------|--------|---------|
| src/ modules | 80%+ | Check with pytest |
| dashboard.py | 60%+ | GUI testing challenging |
| Overall | 75%+ | Balanced coverage |

## Manual Testing

Automated tests cannot cover all scenarios, especially Outlook integration.

### Manual Test Checklist

#### Pre-Launch Tests
- [ ] Outlook is installed and configured
- [ ] Outlook is signed in
- [ ] Test customer database exists
- [ ] Test PDF files exist at specified paths
- [ ] HTML signatures exist in data/ folder

#### Dashboard Launch
```bash
python dashboard.py
```

**Verify:**
- [ ] Window opens without errors
- [ ] Logo displays correctly
- [ ] All tabs visible (Email Generation, Customer Management, Settings)
- [ ] User dropdown shows both users
- [ ] Default template loads

#### Email Generation Tab
- [ ] Template editor displays default template
- [ ] Template can be edited
- [ ] Preview updates in real-time
- [ ] User selection changes signature in preview
- [ ] "Generate Drafts" button is clickable

#### Customer Management Tab
- [ ] Customer list loads all customers
- [ ] Customer details display on selection
- [ ] Add/Edit/Delete buttons work
- [ ] "Verify All" button triggers verification
- [ ] Verification console shows color-coded output
- [ ] Progress bar updates during verification

#### Draft Creation (Real Test)
1. Select test customer (with valid PDF)
2. Customize email template
3. Click "Generate Drafts"
4. **Check Outlook Drafts folder**:
   - [ ] Draft appears in Drafts
   - [ ] Subject line correct
   - [ ] Recipients correct (To and CC)
   - [ ] Email body formatted correctly
   - [ ] Signature included
   - [ ] PDF attached
   - [ ] Draft not sent (still in Drafts)

#### Error Handling
Test error scenarios:
- [ ] Missing PDF file - shows error message
- [ ] Invalid email format - caught by verification
- [ ] Outlook not running - displays error dialog
- [ ] Empty customer database - handles gracefully

### Test Data Setup

**Create test customer record:**

```json
{
  "id": "test_company_20251026",
  "company_name": "Test Company",
  "recipient_names": ["Test User"],
  "email_addresses": ["test@example.com"],
  "email_domain": "example.com",
  "file_generation": {
    "filename_pattern": "{month}_{file_body}",
    "file_body": "_Pricing_Test Company.pdf",
    "file_path": "C:\\Path\\To\\Test\\",
    "month_prefix": "251001",
    "current_filename": "251001_Pricing_Test Company.pdf"
  },
  "active": true,
  "verification_status": {
    "domain_verified": true,
    "file_path_verified": true
  }
}
```

**Create test PDF:**
- Place test PDF at path specified in customer record
- Filename must match `current_filename`

## Debugging Failed Tests

### View Test Output

```bash
# Run with print statements visible
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Enter debugger on failure
pytest tests/ -v --pdb
```

### Common Test Failures

#### Import Errors
**Symptom:** `ModuleNotFoundError: No module named 'src'`
**Solution:**
```bash
# Install package in development mode
pip install -e .
```

#### COM Initialization Errors
**Symptom:** `CoInitialize has not been called`
**Solution:** Ensure `pythoncom.CoInitialize()` called before COM ops

#### File Not Found
**Symptom:** `FileNotFoundError: customer_database.json`
**Solution:** Ensure test data files exist or create test fixtures

#### Outlook Not Available
**Symptom:** `pywintypes.com_error: Outlook.Application`
**Solution:** Tests requiring Outlook should be skipped on non-Windows or without Outlook:

```python
import pytest
import sys

@pytest.mark.skipif(sys.platform != "win32", reason="Outlook Windows-only")
def test_outlook_feature():
    # Test requiring Outlook
    pass
```

## Continuous Integration (CI)

### GitHub Actions Workflow

**File:** `.github/workflows/test.yml` (if exists)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest tests/ -v --cov=src
```

### Local CI Simulation

```bash
# Run full CI test suite locally
pre-commit run --all-files && pytest tests/ -v --cov=src --cov-report=term-missing
```

## Performance Testing

### Test Execution Time

```bash
# Show slowest tests
pytest tests/ -v --durations=10

# Set timeout for tests (prevent hanging)
pytest tests/ -v --timeout=30
```

### Expected Performance

| Test Type | Expected Time |
|-----------|---------------|
| Unit tests | < 0.1s each |
| Integration tests | < 1s each |
| GUI tests | 2-5s each |
| Full suite | < 30s |

## Test Writing Guidelines

### Test Structure (AAA Pattern)

```python
def test_feature_name():
    # Arrange - Set up test data
    customer = create_test_customer()
    template = load_test_template()

    # Act - Execute the function
    result = email_generator.generate_single_draft(customer, template, ...)

    # Assert - Verify results
    assert result["success"] == True
    assert result["customer"] == "Test Company"
```

### Test Naming Convention

```python
# Pattern: test_<function>_<scenario>_<expected_result>

def test_verify_customer_valid_email_returns_success():
    pass

def test_verify_customer_invalid_domain_returns_failure():
    pass

def test_generate_draft_missing_file_returns_error():
    pass
```

### Use Fixtures for Common Setup

```python
import pytest

@pytest.fixture
def test_customer():
    return {
        "company_name": "Test Corp",
        "email_addresses": ["test@test.com"],
        # ...
    }

def test_something(test_customer):
    # Use test_customer fixture
    result = process(test_customer)
    assert result["success"]
```

## Quick Reference

### Common Commands
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific file
pytest tests/test_verification_system.py -v

# Run specific test
pytest tests/test_main.py::test_function_name -v

# Run GUI tests
pytest tests/test_dashboard_playwright.py -v

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html
```

### Pre-Commit Testing
```bash
# Before committing
pytest tests/ -v --cov=src && pre-commit run --all-files
```

---

**Related Documentation:**
- [Adding Features SOP](adding-feature.md)
- [Architecture](../system/architecture.md)
- [Tech Stack](../system/tech-stack.md)
