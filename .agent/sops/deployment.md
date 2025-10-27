# SOP: Deployment and Distribution

**version: v1.0.0**

## When to Use

Use this SOP when:
- Distributing application to new users
- Updating existing installations
- Setting up development environment on new machines
- Creating release packages
- Deploying to multiple workstations

## Important Notes

**This is a desktop application** - no web server deployment needed. Distribution involves:
- Installing Python and dependencies
- Copying application files
- Configuring user-specific settings
- Setting up launchers

## Deployment Types

### 1. Development Deployment
For developers working on the codebase

### 2. User Deployment
For end users who will run the application

### 3. Update Deployment
Updating existing installations to new versions

## Development Deployment

### Prerequisites

- Windows 10 or later
- Microsoft Outlook installed and configured
- Git installed (optional but recommended)
- Python 3.8+ installed

### Step 1: Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/Mark-Valorem/Customer_Price_Sending.git

# Or if private, use SSH
git clone git@github.com:Mark-Valorem/Customer_Price_Sending.git

# Navigate to directory
cd Customer_Price_Sending
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install development dependencies
pip install -e ".[dev]"

# Or install production only
pip install -r requirements.txt

# Verify installation
python -c "import pandas, win32com.client, tkinter; print('✓ All imports successful')"
```

### Step 4: Set Up Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Test pre-commit setup
pre-commit run --all-files
```

### Step 5: Configure Application

**Create/verify required files:**

1. **Customer Database**: `data/customer_database.json`
2. **Email Templates**: `email_templates.json`
3. **HTML Signatures**: `data/Mark_Anderson_231123.html`, `data/Jason_Najm_250427.html`
4. **Company Logo**: `valorem_logo.png`

### Step 6: Test Installation

```bash
# Run dashboard
python dashboard.py

# Run tests
pytest tests/ -v

# Run CLI version
python create_drafts_enhanced.py
```

## User Deployment

### Option A: Python Installation (Recommended)

**For users comfortable with Python**

#### Step 1: Install Python

1. Download Python 3.11 from python.org
2. Run installer with "Add Python to PATH" checked
3. Verify: `python --version`

#### Step 2: Copy Application Files

```bash
# Create application directory
mkdir C:\Apps\PriceSheetAutomation

# Copy files (via network share, USB, or git clone)
xcopy /E /I \\server\share\Customer_Price_Sending C:\Apps\PriceSheetAutomation
```

#### Step 3: Install Dependencies

```bash
cd C:\Apps\PriceSheetAutomation
pip install -r requirements.txt
```

#### Step 4: Configure User Settings

1. **Add HTML signatures** to `data/` folder
2. **Configure customer database** (if user manages own customers)
3. **Update file paths** in customer_database.json to user's SharePoint sync locations

#### Step 5: Create Desktop Shortcut

**Create:** `run_dashboard.vbs` (already exists)

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Apps\PriceSheetAutomation"
WshShell.Run "pythonw dashboard.py", 0, False
```

**Right-click → Create Shortcut → Move to Desktop**

### Option B: Standalone Executable (Future)

**Not yet implemented - future enhancement**

Using PyInstaller to create .exe:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --icon=valorem_logo.ico dashboard.py

# Distribute dist/dashboard.exe
```

## Update Deployment

### Updating Existing Installation

#### Method 1: Git Pull (For developers)

```bash
cd C:\Apps\PriceSheetAutomation
git pull origin main
pip install -r requirements.txt --upgrade
```

#### Method 2: File Replacement (For users)

1. **Backup customer database**:
   ```bash
   copy data\customer_database.json data\customer_database.backup.json
   ```

2. **Copy new files** (overwrite existing)

3. **Restore customer database** (if needed)

4. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

#### Method 3: Automated Update Script

**Create:** `scripts/update_application.bat`

```batch
@echo off
echo ====================================
echo Price Sheet Automation - Update
echo ====================================
echo.

REM Backup customer data
echo [1/5] Backing up customer data...
copy data\customer_database.json data\customer_database.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json

REM Pull latest changes
echo [2/5] Pulling latest changes...
git pull origin main

REM Update dependencies
echo [3/5] Updating dependencies...
pip install -r requirements.txt --upgrade

REM Run tests
echo [4/5] Running tests...
pytest tests/ -v -x

REM Done
echo [5/5] Update complete!
echo.
echo You can now run the application.
pause
```

## Version Management

### Creating a Release

#### Step 1: Bump Version

```bash
# Bump version (major, minor, or patch)
scripts\bump_version.bat major

# Or manually update:
# - pyproject.toml
# - src/__init__.py
# - .bumpversion.cfg
# - README.md
```

#### Step 2: Update Changelog

**Edit:** `CHANGELOG.md`

```markdown
## [4.0.0] - 2025-10-26

### Added
- .agent documentation system
- Comprehensive SOPs
- System architecture documentation

### Changed
- Updated development workflow
- Enhanced documentation structure

### Fixed
- (list any bug fixes)
```

#### Step 3: Create Git Tag

```bash
# Create annotated tag
git tag -a v4.0.0 -m "Version 4.0.0: .agent documentation system"

# Push tag
git push origin v4.0.0
```

#### Step 4: Create GitHub Release

```bash
# Using GitHub CLI
gh release create v4.0.0 \
  --title "Version 4.0.0" \
  --notes "See CHANGELOG.md for details"

# Or create manually via GitHub web interface
```

## Configuration Management

### User-Specific Configuration

**Each user needs:**

1. **HTML Signatures**: `data/` folder
   - Mark_Anderson_231123.html
   - Jason_Najm_250427.html

2. **Customer Database**: `data/customer_database.json`
   - May be shared via network
   - Or user-specific copy

3. **Email Templates**: `email_templates.json`
   - Shared or customized per user

4. **File Paths**: Update in customer database
   - Point to user's SharePoint sync location
   - Example: `C:\Users\{USERNAME}\Valorem\...`

### Shared Configuration

**Via network share:**

```batch
REM Map network drive to shared config
net use Z: \\server\share\PriceSheetConfig

REM Create symlinks to shared files
mklink /H data\customer_database.json Z:\customer_database.json
mklink /H email_templates.json Z:\email_templates.json
```

## Troubleshooting Deployment Issues

### Python Not Found

**Error:** `'python' is not recognized`

**Solution:**
```bash
# Add Python to PATH
setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311"
```

### Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific module
pip install pandas
```

### Outlook COM Errors

**Error:** `pywintypes.com_error: Outlook.Application`

**Causes:**
- Outlook not installed
- Outlook not configured
- Outlook not signed in
- 32-bit/64-bit mismatch

**Solution:**
```bash
# Verify Outlook installation
start outlook

# Reinstall pywin32
pip uninstall pywin32
pip install pywin32
python venv\Scripts\pywin32_postinstall.py -install
```

### Permission Errors

**Error:** `PermissionError: [WinError 5] Access is denied`

**Solution:**
- Run as Administrator
- Check file/folder permissions
- Disable antivirus temporarily

## Multi-User Deployment

### Shared Network Installation

**Setup:**

```bash
# Install on network share
\\server\share\Apps\PriceSheetAutomation\

# Each user creates desktop shortcut
# Pointing to: \\server\share\Apps\PriceSheetAutomation\run_dashboard.vbs
```

**Pros:**
- Single installation to maintain
- Automatic updates for all users

**Cons:**
- Network dependency
- Slower startup
- Concurrent access issues

### Individual Installations

**Setup:**

```bash
# Each user has local copy
C:\Users\{USERNAME}\Apps\PriceSheetAutomation\
```

**Pros:**
- Faster performance
- No network dependency
- User-specific customization

**Cons:**
- Multiple installations to update
- Disk space per user

## Backup and Recovery

### Automated Backup

**Create:** `scripts/backup_data.bat`

```batch
@echo off
set BACKUP_DIR=.\backups\%date:~-4,4%%date:~-10,2%%date:~-7,2%
mkdir %BACKUP_DIR%

copy data\customer_database.json %BACKUP_DIR%\
copy email_templates.json %BACKUP_DIR%\
copy logs\*.log %BACKUP_DIR%\

echo Backup created: %BACKUP_DIR%
```

### Recovery Procedure

```bash
# Restore from backup
copy backups\20251026\customer_database.json data\
copy backups\20251026\email_templates.json .\
```

## Monitoring and Maintenance

### Log Files

**Locations:**
- `logs/email_generation_YYYYMMDD_HHMMSS.log`
- `logs/audit_log.json`

**Review regularly for:**
- Error patterns
- Failed draft generations
- Verification failures

### Health Checks

**Weekly checks:**
- [ ] All users can launch application
- [ ] Outlook integration working
- [ ] Customer database accessible
- [ ] PDF files accessible
- [ ] No errors in recent logs

## Quick Reference

### New Installation
```bash
git clone <repo>
cd Customer_Price_Sending
pip install -r requirements.txt
python dashboard.py
```

### Update Existing
```bash
cd Customer_Price_Sending
git pull origin main
pip install -r requirements.txt --upgrade
```

### Create Release
```bash
scripts\bump_version.bat major
git push --tags
gh release create v4.0.0
```

### Backup Data
```bash
copy data\customer_database.json backups\
```

---

**Related Documentation:**
- [Tech Stack](../system/tech-stack.md)
- [Architecture](../system/architecture.md)
- [Database Changes SOP](database-changes.md)
