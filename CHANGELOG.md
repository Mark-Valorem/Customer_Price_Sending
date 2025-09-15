# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Semantic versioning system with bump2version
- Conventional Commits enforcement with commitlint
- Pre-commit hooks for code quality and commit message validation
- GitHub Actions CI/CD pipeline for testing and releases
- Comprehensive project structure with src/, tests/, templates/ directories
- Automated changelog generation
- Version bump scripts for Windows and Linux/Mac
- Development dependencies in pyproject.toml
- Code formatting with Black and isort
- Security scanning with bandit
- Test coverage reporting

### Changed
- Project structure reorganized to follow Python best practices
- Documentation enhanced with CONTRIBUTING.md and updated README.md
- Version tracking added to src/__init__.py

## [0.1.0] - 2024-XX-XX

### Added
- Initial release of Customer Price Sheet Automation
- Outlook email draft creation with customer data from Excel
- Template management system with email_templates.json
- Enhanced script with interactive template selection
- VBS launcher scripts for easy execution
- Excel column verification and diagnostic tools
- Support for PDF attachments from SharePoint/OneDrive paths
- Multiple email templates (default, price_increase, no_change, promotional)
- Monthly customization with interactive prompts
- Automatic date calculation for current/previous months
- Safety features (draft-only, no automatic sending)

### Features
- **Core Scripts**: create_drafts.py, create_drafts_enhanced.py
- **Template Management**: manage_templates.py
- **Diagnostic Tools**: check_columns.py, diagnose_excel.py
- **Configuration**: email_templates.json with multiple templates
- **Easy Launch**: VBS scripts for double-click execution
- **Excel Integration**: Pandas-based data processing with proper header handling
- **Outlook Integration**: pywin32-based email draft creation
- **PDF Handling**: Automatic attachment from file paths