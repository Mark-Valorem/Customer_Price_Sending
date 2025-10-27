# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.2] - 2025-10-27

### Fixed
- Recipient names now properly formatted with commas (e.g., "Hi Arnie, Steve, Pares, Brad and Maria" instead of "Hi Arnie and Steve and Pares and Brad and Maria")
- Email font now consistently applies Aptos/Calibri 11pt throughout entire email body
- Font styling applied directly to all paragraph tags to ensure proper rendering in Outlook
- Removed duplicate "and and" issue caused by empty strings in recipient names list

### Changed
- Created `format_recipient_names()` helper function for proper comma-separated name formatting
- Updated HTML email generation to apply inline styles to all `<p>` tags
- Simplified font-family list to "Aptos, Calibri, sans-serif" as requested

## [4.0.1] - 2025-10-27

### Fixed
- CC emails now configurable via Settings tab instead of hardcoded values
- Settings tab now actually saves and loads CC email configuration
- Email greetings now include ALL recipient names, not just the first name (e.g., "Hi John and Jane and Bob" instead of just "Hi John")
- Email font changed from Times New Roman 12pt to Aptos 11pt as requested
- Settings persistence via `config/app_settings.json` configuration file

### Changed
- Dashboard Settings tab now functional with save/load capabilities
- Email generator accepts CC emails as parameter instead of hardcoded
- Recipient name handling simplified to join all names with "and"

## [4.0.0] - 2025-10-26

### Added
- Comprehensive .agent documentation system for AI-optimized context management
- Standard Operating Procedures (SOPs) for common development tasks
- System architecture documentation with detailed component diagrams
- Database schema documentation with complete field reference
- Tech stack documentation with all dependencies and configurations
- API/Interface documentation for internal modules and COM integration
- Automated documentation maintenance via `/update-doc` command
- Version tracking for all documentation files

### Changed
- Updated CLAUDE.md with .agent documentation system rules
- Enhanced development workflow with comprehensive SOPs

## [3.0.1] - 2025-10-22

### Fixed
- Resolved "'str' object has no attribute 'get'" error in customer verification
- Fixed file_generation field handling for JSON database format compatibility
- Improved error handling for different data structure formats

### Changed
- Moved outdated launcher files to Archive/legacy_launchers/

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