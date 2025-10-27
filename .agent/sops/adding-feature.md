# SOP: Adding a New Feature

**version: v1.0.0**

## When to Use

Use this SOP whenever you need to add new functionality to the Customer Price Sheet Automation system. This includes:
- New GUI features in the dashboard
- New email generation capabilities
- New verification checks
- New data fields in customer database
- New templates or customization options

## Prerequisites

- Development environment set up with dependencies
- Git working directory clean (committed or stashed changes)
- Understanding of system architecture (see [architecture.md](../system/architecture.md))
- Feature requirements clearly defined

## Step-by-Step Process

### 1. Plan the Feature

**Actions:**
1. **Define requirements** - What should the feature do?
2. **Identify affected components** - Which files/modules need changes?
3. **Check for breaking changes** - Will this affect existing functionality?
4. **Review architecture docs** - Understand current system design
5. **Create implementation plan** - Outline steps and dependencies

**Checklist:**
- [ ] Requirements documented
- [ ] Affected components identified
- [ ] Breaking changes assessed
- [ ] Architecture reviewed
- [ ] Implementation plan created

**Example:**
```markdown
## Feature: Add Bulk Email Validation

### Requirements
- Validate email syntax for all customers
- Display validation results in GUI
- Highlight invalid emails in red

### Affected Components
- src/verification_system.py (add email validator)
- dashboard.py (update verification console)
- data/customer_database.json (add validation_status field)

### Breaking Changes
- None (additive only)

### Implementation Steps
1. Add email_validator library to requirements.txt
2. Create validate_email_syntax() function
3. Update verify_single_customer() to include email validation
4. Update GUI to display email validation results
5. Add tests for email validation
```

### 2. Create Feature Branch

**Actions:**
```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Verify branch
git branch --show-current
```

**Branch Naming Convention:**
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions

**Examples:**
- `feature/bulk-email-validation`
- `fix/verification-timeout`
- `refactor/email-generator`

### 3. Implement the Feature

**Actions:**

#### For Dashboard (GUI) Changes:

**File:** `dashboard.py`

```python
# 1. Add new UI components
def create_new_feature_ui(self):
    # Create widgets
    button = ttk.Button(parent, text="Feature", command=self.on_feature_click)
    button.pack()

# 2. Add event handlers
def on_feature_click(self):
    # Handle feature activation
    result = self.feature_logic()
    self.display_result(result)

# 3. Add helper methods
def feature_logic(self):
    # Feature implementation
    return result
```

#### For Backend Module Changes:

**File:** `src/email_generator.py` or `src/verification_system.py`

```python
# 1. Add new function
def new_feature_function(parameter: type) -> return_type:
    """
    Feature description.

    Args:
        parameter: Description

    Returns:
        Description of return value
    """
    try:
        # Implementation
        result = process(parameter)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Feature error: {e}")
        return {"success": False, "error": str(e)}

# 2. Update existing functions if needed
def existing_function():
    # ... existing code ...

    # Add feature integration
    if feature_enabled:
        result = new_feature_function(data)

    # ... rest of code ...
```

#### For Database Changes:

**See:** [database-changes.md](database-changes.md) for detailed SOP

```python
# Add new field to customer records
customer_record = {
    # ... existing fields ...
    "new_feature_field": {
        "enabled": True,
        "value": "default"
    }
}
```

### 4. Update Dependencies

**If adding new libraries:**

```bash
# Add to requirements.txt
echo "new-library>=1.0.0" >> requirements.txt

# Add to pyproject.toml
# Edit [project] dependencies section manually

# Install new dependency
pip install new-library
```

### 5. Write Tests

**Create test file:** `tests/test_your_feature.py`

```python
import pytest
from src import your_module

def test_feature_success():
    """Test feature with valid input"""
    result = your_module.new_feature_function("valid_input")
    assert result["success"] == True
    assert "data" in result

def test_feature_failure():
    """Test feature with invalid input"""
    result = your_module.new_feature_function(None)
    assert result["success"] == False
    assert "error" in result

def test_feature_edge_case():
    """Test feature with edge case"""
    result = your_module.new_feature_function("")
    # Assert expected behavior
```

**Run tests:**
```bash
pytest tests/test_your_feature.py -v
pytest tests/ -v --cov=src  # Full test suite with coverage
```

### 6. Update Documentation

**Update files:**

1. **CLAUDE.md** - Add feature to relevant sections
2. **.agent/system/architecture.md** - Update if architecture changes
3. **.agent/system/database-schema.md** - Update if schema changes
4. **README.md** - Add to features list
5. **CHANGELOG.md** - Add to Unreleased section

**Example CHANGELOG entry:**
```markdown
## [Unreleased]

### Added
- Bulk email validation feature (#42)
  - Validates email syntax for all customers
  - Displays validation results in GUI
  - Highlights invalid emails in red
```

### 7. Run Code Quality Checks

```bash
# Run pre-commit hooks
pre-commit run --all-files

# Or run individual checks
black src/ dashboard.py tests/
isort src/ dashboard.py tests/
flake8 src/ dashboard.py tests/
pytest tests/ -v --cov=src
```

**Fix any issues** before committing.

### 8. Commit Changes

**Follow conventional commit format:**

```bash
# Stage changes
git add .

# Commit with conventional format
git commit -m "feat: add bulk email validation feature

- Add email_validator library to dependencies
- Implement validate_email_syntax() function
- Update verification console to display email validation
- Add validation_status field to customer database
- Add tests for email validation

Closes #42"
```

**Conventional Commit Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation
- `test:` - Test additions
- `chore:` - Maintenance tasks

### 9. Test in Real Environment

**Manual testing checklist:**
- [ ] Feature works as expected in GUI
- [ ] No errors in console/logs
- [ ] Existing features still work
- [ ] Outlook integration works (if applicable)
- [ ] Customer data loads correctly
- [ ] Performance is acceptable

**Test with real data:**
```bash
# Run dashboard
python dashboard.py

# Or run CLI
python create_drafts_enhanced.py
```

### 10. Create Pull Request (Optional)

**If using PR workflow:**

```bash
# Push feature branch
git push origin feature/your-feature-name

# Create PR via GitHub CLI or web interface
gh pr create --title "Add bulk email validation" --body "Closes #42"
```

**PR Description Template:**
```markdown
## Description
Brief description of the feature

## Changes
- List of changes made
- Files modified
- New dependencies

## Testing
- [ ] Unit tests added
- [ ] Manual testing completed
- [ ] No breaking changes

## Screenshots (if GUI changes)
[Add screenshots]

## Related Issues
Closes #42
```

### 11. Merge to Main

**After approval (or for solo work):**

```bash
# Switch to main branch
git checkout main

# Merge feature branch
git merge feature/your-feature-name

# Push to remote
git push origin main

# Delete feature branch (optional)
git branch -d feature/your-feature-name
```

### 12. Update Documentation

**Run documentation update command:**

```bash
# Use automated doc update (if available)
# This saves feature plan to .agent/tasks/

# Or manually create task document
```

**Create task record:** `.agent/tasks/bulk-email-validation.md`

```markdown
# Task: Bulk Email Validation

**Completed**: 2025-10-26
**Version**: 4.0.0

## Implementation Summary
Added bulk email validation feature to verify email syntax for all customers...

## Technical Decisions
- Used email-validator library for robust validation
- Integrated into existing verification system
- Added new GUI display section

## Challenges
- Handling invalid email formats gracefully
- Maintaining backward compatibility

## Lessons Learned
- Always validate inputs early
- GUI updates should be non-blocking
```

## Common Pitfalls

### 1. Forgetting to Initialize COM
**Problem:** COM operations fail in new functions
**Solution:** Always call `pythoncom.CoInitialize()` before COM ops

### 2. Breaking Existing Functionality
**Problem:** Changes affect unrelated features
**Solution:** Run full test suite before committing

### 3. Not Updating Documentation
**Problem:** Docs become outdated
**Solution:** Update docs as part of feature development

### 4. Skipping Tests
**Problem:** Bugs discovered in production
**Solution:** Write tests before marking feature complete

### 5. Database Schema Changes Without Migration
**Problem:** Old data breaks with new code
**Solution:** Follow database-changes SOP carefully

## Rollback Procedure

**If feature causes problems:**

```bash
# Revert last commit
git revert HEAD

# Or reset to previous state
git reset --hard HEAD~1

# Push revert
git push origin main
```

## Quick Reference

**Feature development checklist:**
1. [ ] Plan documented
2. [ ] Feature branch created
3. [ ] Code implemented
4. [ ] Tests written and passing
5. [ ] Code quality checks passed
6. [ ] Documentation updated
7. [ ] Manual testing completed
8. [ ] Changes committed with conventional format
9. [ ] Merged to main
10. [ ] Task documented in .agent/tasks/

---

**Related Documentation:**
- [Architecture](../system/architecture.md)
- [Database Changes SOP](database-changes.md)
- [Running Tests SOP](running-tests.md)
- [Tech Stack](../system/tech-stack.md)
