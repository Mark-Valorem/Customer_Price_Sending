# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-09-19

### Added
- User selection dropdown with HTML signatures for Jason Najm and Mark Anderson
- Company logo (Valorem) in the top-left corner of the dashboard
- Enhanced customer verification console with 50/50 split layout
- Real-time verification progress display for all customers
- Comprehensive verification summary with pass/fail statistics
- Playwright integration for automated UI testing
- Auto-save functionality for email templates
- Pillow dependency for image handling

### Changed
- **BREAKING**: Removed terminal/console window options - application now launches directly
- **BREAKING**: Simplified email draft management - removed load/save draft functionality
- Dashboard now uses only a default email template that can be edited in-place
- Verification now tests ALL customers with a single button click
- Improved verification console with color-coded output
- Updated VBS launcher for direct execution without selection dialog
- Version numbering changed from 0.x.x to 3.0.0

### Removed
- Terminal selection dialog from VBS launcher
- Load/Save draft buttons from UI
- Monthly drafts file management
- Separate verification status page (integrated into main panel)

### Fixed
- Signature duplication issues
- Variable resolution in email templates
- Error handling with better user feedback

## [0.3.1] - 2025-09-16

### Fixed
- Critical dashboard fixes for month/year consistency
- File extraction improvements

### Changed
- Code refactoring to remove v1/v2 confusion
- Better organization of project files

## [0.3.0] - 2025-09-15

### Added
- Enhanced customer database system v2 with verification
- Multi-layer verification system
- Audit logging for all operations
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

### Fixed
- Duplicate signature issues
- Template variable resolution

### Changed
- Project structure reorganized to follow Python best practices
- Documentation enhanced with CONTRIBUTING.md and updated README.md
- Version tracking added to src/__init__.py

## [0.2.0] - 2025-09-01

### Added
- Customer management panel
- Database-driven customer records
- JSON database support

### Changed
- Migrated from Excel to JSON database

## [0.1.0] - 2025-08-15

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