# Contributing to Customer Price Sheet Automation

Thank you for your interest in contributing to the Customer Price Sheet Automation project! This document provides guidelines and workflows for contributing to this project.

## Table of Contents

- [Development Setup](#development-setup)
- [Version Management](#version-management)
- [Commit Message Format](#commit-message-format)
- [Release Workflow](#release-workflow)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Documentation](#documentation)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Microsoft Outlook (for testing email functionality)
- Node.js (for commit linting)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd customer-price-sheet-automation
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

5. **Install Node.js dependencies for commit linting:**
   ```bash
   npm install -g @commitlint/cli @commitlint/config-conventional
   ```

## Version Management

This project uses **Semantic Versioning (SemVer)** and automated version management with `bump2version`.

### Semantic Versioning

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality in a backwards compatible manner
- **PATCH** version: Backwards compatible bug fixes

### Version Bumping

Use the provided scripts to bump versions:

#### Windows:
```bash
# Patch version (0.1.0 → 0.1.1)
scripts\bump_version.bat patch

# Minor version (0.1.0 → 0.2.0)
scripts\bump_version.bat minor

# Major version (0.1.0 → 1.0.0)
scripts\bump_version.bat major
```

#### Linux/Mac:
```bash
# Make script executable (first time only)
chmod +x scripts/bump_version.sh

# Patch version (0.1.0 → 0.1.1)
./scripts/bump_version.sh patch

# Minor version (0.1.0 → 0.2.0)
./scripts/bump_version.sh minor

# Major version (0.1.0 → 1.0.0)
./scripts/bump_version.sh major
```

#### Script Options:

- `--dry-run`: Preview changes without making them
- `--no-push`: Don't push changes to remote repository
- `--help`: Show usage information

#### Examples:
```bash
# Preview what a minor version bump would do
scripts\bump_version.bat minor --dry-run

# Bump patch version but don't push to remote
scripts\bump_version.bat patch --no-push
```

### Manual Version Management

If you need to bump versions manually:

```bash
# Bump patch version
bump2version patch

# Bump minor version
bump2version minor

# Bump major version
bump2version major
```

## Commit Message Format

This project follows the **Conventional Commits** specification. Commit messages are automatically validated using `commitlint`.

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system changes
- **ci**: CI/CD changes
- **chore**: Maintenance tasks
- **revert**: Revert previous commit
- **bump**: Version bump commits

### Examples

```bash
# Feature addition
git commit -m "feat: add template selection for email drafts"

# Bug fix
git commit -m "fix: resolve Excel file reading issue with headers"

# Documentation update
git commit -m "docs: update installation instructions"

# Version bump (automatic)
git commit -m "bump: version 0.1.0 → 0.1.1"
```

### Scopes (Optional)

You can add scopes to provide more context:

```bash
git commit -m "feat(templates): add promotional email template"
git commit -m "fix(excel): handle missing customer data gracefully"
git commit -m "docs(api): update function documentation"
```

## Release Workflow

### Automatic Releases

1. **Create a version bump:**
   ```bash
   scripts\bump_version.bat patch  # or minor/major
   ```

2. **Push changes:**
   The script automatically pushes the commit and tag to trigger the release workflow.

3. **GitHub Actions handles:**
   - Running tests on multiple Python versions
   - Building distribution packages
   - Generating/updating CHANGELOG.md
   - Creating a GitHub Release with artifacts

### Manual Release Process

If you need to create a release manually:

1. **Ensure all changes are committed**
2. **Update version in configuration files**
3. **Create and push a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

### Release Artifacts

Each release includes:
- **Source distribution** (`tar.gz`)
- **Wheel distribution** (`.whl`)
- **Changelog** (automatically generated)
- **Release notes** (from commit history)

## Code Quality

### Pre-commit Hooks

Pre-commit hooks automatically run before each commit:

- **Code formatting** (Black)
- **Import sorting** (isort)
- **Linting** (flake8)
- **Security scanning** (bandit)
- **Commit message validation** (commitlint)
- **File checks** (trailing whitespace, large files, etc.)

### Manual Code Quality Checks

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Security scan
bandit -r src/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Code Style Guidelines

- **Line length**: 88 characters (Black default)
- **Import style**: Use isort with Black profile
- **Docstrings**: Use Google-style docstrings
- **Type hints**: Use type hints where appropriate

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Include docstrings for complex tests

### Test Coverage

Aim for high test coverage:
- **Minimum**: 80% coverage
- **Target**: 90%+ coverage
- View coverage reports in `htmlcov/index.html`

## Documentation

### Documentation Updates

When making changes:

1. **Update docstrings** for new/modified functions
2. **Update README.md** for user-facing changes
3. **Update CLAUDE.md** for AI guidance changes
4. **Add/update type hints** for better code documentation

### Documentation Style

- Use **Markdown** for all documentation files
- Include **code examples** where helpful
- Keep **installation instructions** up-to-date
- Document **breaking changes** clearly

## Development Workflow

### Feature Development

1. **Create a feature branch:**
   ```bash
   git checkout -b feat/new-feature-name
   ```

2. **Make your changes:**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push and create a pull request:**
   ```bash
   git push origin feat/new-feature-name
   ```

### Bug Fixes

1. **Create a bugfix branch:**
   ```bash
   git checkout -b fix/bug-description
   ```

2. **Fix the issue:**
   - Write a test that reproduces the bug
   - Implement the fix
   - Ensure all tests pass

3. **Commit and push:**
   ```bash
   git commit -m "fix: resolve issue with bug description"
   git push origin fix/bug-description
   ```

## Questions and Support

If you have questions or need support:

1. **Check existing documentation** (README.md, CLAUDE.md)
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact the maintainers** at support@valorem.com.au

Thank you for contributing to the Customer Price Sheet Automation project!