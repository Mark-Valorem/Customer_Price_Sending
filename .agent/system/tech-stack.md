# Technology Stack

**version: v1.0.0**

## Overview

The Customer Price Sheet Automation system is built entirely with Python and leverages Windows-specific COM automation for Microsoft Outlook integration. This document provides comprehensive details on all technologies, libraries, and tools used in the project.

## Core Technologies

### Python 3.8+

**Version Required**: 3.8 or higher
**Supported Versions**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

**Rationale**:
- Mature ecosystem for Windows automation
- Excellent COM support via pywin32
- Strong data processing capabilities with pandas
- Cross-version compatibility for enterprise environments

## Frontend (GUI)

### tkinter (Standard Library)

**Version**: Built-in with Python
**Purpose**: GUI dashboard interface

**Key Features Used:**
- `ttk` widgets for modern styling
- `PanedWindow` for resizable layouts
- `ScrolledText` for multi-line editors and consoles
- `Treeview` for customer list display
- `Canvas` for image display (logo)

**Example Usage:**
```python
import tkinter as tk
from tkinter import ttk, scrolledtext

root = tk.Tk()
notebook = ttk.Notebook(root)
```

**Why tkinter?**
- Built-in (no external dependencies)
- Native look and feel on Windows
- Lightweight and performant
- Sufficient for desktop application needs

## Data Processing

### pandas 1.5.0+

**Version Required**: ≥ 1.5.0
**Purpose**: Excel file processing and data manipulation

**Key Features Used:**
- Excel file reading (`.read_excel()`)
- DataFrame operations for data transformation
- Header skipping for non-standard Excel layouts
- Data validation and cleaning

**Example Usage:**
```python
import pandas as pd

df = pd.read_excel("file.xlsx", header=3)  # Headers on row 4
customers = df.to_dict('records')
```

### openpyxl 3.0.0+

**Version Required**: ≥ 3.0.0
**Purpose**: Excel file reading engine (used by pandas)

**Why openpyxl?**
- Modern .xlsx support
- Active maintenance
- Required by pandas for Excel operations

## Windows Integration

### pywin32 306+

**Version Required**: ≥ 306
**Purpose**: Microsoft Outlook COM automation

**Key Modules Used:**
- `win32com.client`: COM object creation
- `pythoncom`: COM threading support

**Example Usage:**
```python
import win32com.client
import pythoncom

pythoncom.CoInitialize()
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)  # 0 = MailItem
```

**COM Objects Used:**
- `Outlook.Application`: Main Outlook application object
- `MailItem (0)`: Email draft object

**Critical Notes:**
- Requires Outlook to be installed and configured
- Must call `pythoncom.CoInitialize()` before COM operations
- Single-threaded COM operations only

## Date and Time

### python-dateutil 2.8.0+

**Version Required**: ≥ 2.8.0
**Purpose**: Date calculations and formatting

**Key Features Used:**
- `relativedelta`: Month/quarter calculations
- Date parsing and formatting
- Timezone handling

**Example Usage:**
```python
from dateutil.relativedelta import relativedelta
from datetime import date

previous_month = date.today() - relativedelta(months=1)
```

## Image Processing

### Pillow 10.0.0+

**Version Required**: ≥ 10.0.0
**Purpose**: Image loading and display (logo)

**Key Features Used:**
- Image file loading (PNG, JPG)
- Image resizing for GUI display
- tkinter PhotoImage conversion

**Example Usage:**
```python
from PIL import Image, ImageTk

img = Image.open("logo.png")
photo = ImageTk.PhotoImage(img)
```

## Testing

### pytest 7.0.0+

**Version Required**: ≥ 7.0.0
**Purpose**: Unit and integration testing

**Key Features:**
- Test discovery and execution
- Fixtures for test setup
- Parameterized testing
- Coverage reporting

**Directory**: `tests/`

### pytest-cov 4.0.0+

**Version Required**: ≥ 4.0.0
**Purpose**: Code coverage reporting

**Usage:**
```bash
pytest tests/ -v --cov=src
```

### Playwright 1.40.0+

**Version Required**: ≥ 1.40.0
**Purpose**: GUI automated testing

**Key Features:**
- UI interaction automation
- Screenshot capture
- Test recording and playback

**Test File**: `tests/test_dashboard_playwright.py`

## Development Tools

### Code Quality

#### black 23.0.0+
**Purpose**: Code formatting
**Configuration**: `pyproject.toml`
```toml
[tool.black]
line-length = 88
target-version = ['py38']
```

#### isort 5.12.0+
**Purpose**: Import sorting
**Configuration**: `pyproject.toml`
```toml
[tool.isort]
profile = "black"
multi_line_output = 3
```

#### flake8 6.0.0+
**Purpose**: Code linting and style checking
**Integration**: pre-commit hooks

### Version Management

#### bump2version 1.0.1+
**Purpose**: Automated version bumping
**Configuration**: `.bumpversion.cfg`
**Usage**: `scripts/bump_version.bat major|minor|patch`

#### pre-commit 3.0.0+
**Purpose**: Git hooks for code quality
**Configuration**: `.pre-commit-config.yaml`
**Usage**: `pre-commit install`

## Build and Distribution

### setuptools 45+

**Purpose**: Package building
**Configuration**: `pyproject.toml`

### build 0.10.0+

**Purpose**: Modern Python package building
**Usage**: `python -m build`

### twine 4.0.0+

**Purpose**: Package upload to PyPI
**Usage**: `twine upload dist/*`

## Project Configuration

### pyproject.toml

Modern Python project configuration following PEP 517/518:

```toml
[project]
name = "customer-price-sheet-automation"
version = "4.0.0"
requires-python = ">=3.8"
dependencies = [
    "pandas>=1.5.0",
    "pywin32>=306",
    "openpyxl>=3.0.0",
    "python-dateutil>=2.8.0",
    "Pillow>=10.0.0",
    "playwright>=1.40.0",
]

[project.optional-dependencies]
dev = [
    "bump2version>=1.0.1",
    "pre-commit>=3.0.0",
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
]
```

## Platform Requirements

### Operating System
- **Required**: Windows 10 or later
- **Why**: Microsoft Outlook COM automation is Windows-only

### Microsoft Outlook
- **Required**: Outlook 2016 or later
- **Configuration**: Must be signed in and configured
- **Access**: Desktop client (not Outlook Web App)

### File System
- **Requirements**:
  - NTFS file system for long paths
  - Access to SharePoint-synced folders (OneDrive)
  - Read/write permissions for application directory

## Runtime Dependencies Summary

### Production Dependencies
```
pandas>=1.5.0           # Data processing
pywin32>=306            # Outlook COM automation
openpyxl>=3.0.0         # Excel file reading
python-dateutil>=2.8.0  # Date calculations
Pillow>=10.0.0          # Image loading
playwright>=1.40.0      # GUI testing
```

### Development Dependencies
```
bump2version>=1.0.1     # Version management
pre-commit>=3.0.0       # Git hooks
pytest>=7.0.0           # Testing framework
pytest-cov>=4.0.0       # Coverage reporting
black>=23.0.0           # Code formatting
isort>=5.12.0           # Import sorting
flake8>=6.0.0           # Linting
```

## Installation

### Production Environment
```bash
pip install -r requirements.txt
```

### Development Environment
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

## Dependency Management

### requirements.txt
Production dependencies in pinned format for reproducible builds.

### pyproject.toml
Modern dependency specification with version ranges.

### Update Strategy
1. Test with latest versions quarterly
2. Pin major versions for stability
3. Use `pip list --outdated` to check for updates
4. Test thoroughly before updating pywin32 (breaking changes possible)

## Performance Considerations

### Startup Time
- **Python import**: ~500ms
- **tkinter initialization**: ~1000ms
- **COM initialization**: ~500ms
- **Total**: ~2-3 seconds

### Memory Usage
- **Base Python**: ~20 MB
- **tkinter GUI**: ~30 MB
- **pandas + data**: ~20 MB
- **COM objects**: ~10 MB
- **Total**: ~80-100 MB

### Disk Space
- **Python 3.8+**: ~100 MB
- **Dependencies**: ~150 MB
- **Application code**: ~5 MB
- **Total**: ~255 MB

## Known Limitations

1. **Windows Only**: No cross-platform support (Outlook COM limitation)
2. **Outlook Required**: Must have Outlook installed and running
3. **Single-threaded**: COM automation is single-threaded
4. **No Web Interface**: Desktop application only
5. **File System Access**: Requires local file system access

## Future Technology Considerations

1. **Database**: SQLite for larger customer base
2. **Async**: asyncio for concurrent operations
3. **API**: FastAPI for web interface (optional)
4. **Packaging**: PyInstaller for standalone executable
5. **Cloud**: Azure/AWS integration for cloud storage

---

**Related Documentation:**
- [Architecture](architecture.md)
- [Database Schema](database-schema.md)
- [Adding Features SOP](../sops/adding-feature.md)
