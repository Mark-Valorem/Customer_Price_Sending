@echo off
REM Customer Price Sheet Automation - Version Bump Script (Windows)
REM This script automates the version bumping process using bump2version
REM and pushes the changes and tags to the remote repository.

setlocal enabledelayedexpansion

REM Parse command line arguments
set BUMP_TYPE=%1
set DRY_RUN=false
set NO_PUSH=false

:parse_args
if "%2"=="--dry-run" (
    set DRY_RUN=true
    shift
    goto :parse_args
)
if "%2"=="--no-push" (
    set NO_PUSH=true
    shift
    goto :parse_args
)
if "%2"=="--help" goto :show_usage
if "%2"=="-h" goto :show_usage
if not "%2"=="" (
    echo [ERROR] Unknown option: %2
    goto :show_usage
)

REM Validate arguments
if "%BUMP_TYPE%"=="" (
    echo [ERROR] Bump type is required
    goto :show_usage
)

if not "%BUMP_TYPE%"=="patch" if not "%BUMP_TYPE%"=="minor" if not "%BUMP_TYPE%"=="major" (
    echo [ERROR] Invalid bump type: %BUMP_TYPE%
    goto :show_usage
)

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Not in a git repository
    exit /b 1
)

REM Check if working directory is clean
for /f %%i in ('git status --porcelain') do (
    echo [ERROR] Working directory is not clean. Please commit or stash changes first.
    git status --short
    exit /b 1
)

REM Check if bump2version is installed
bump2version --help >nul 2>&1
if errorlevel 1 (
    echo [ERROR] bump2version is not installed. Install it with: pip install bump2version
    exit /b 1
)

REM Get current version
for /f "tokens=2 delims==" %%a in ('findstr /C:"current_version" .bumpversion.cfg') do (
    set CURRENT_VERSION=%%a
    set CURRENT_VERSION=!CURRENT_VERSION: =!
)
echo [INFO] Current version: !CURRENT_VERSION!

REM Dry run mode
if "%DRY_RUN%"=="true" (
    echo [WARNING] DRY RUN MODE - No changes will be made
    bump2version --dry-run --verbose %BUMP_TYPE%
    exit /b 0
)

REM Confirm the action
echo.
echo [WARNING] This will:
echo   1. Bump the %BUMP_TYPE% version
echo   2. Update version in pyproject.toml and src/__init__.py
echo   3. Create a git commit with the version change
echo   4. Create a git tag for the new version
if not "%NO_PUSH%"=="true" (
    echo   5. Push changes and tags to the remote repository
)
echo.

set /p CONFIRM="Do you want to continue? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo [INFO] Operation cancelled
    exit /b 0
)

REM Perform the version bump
echo [INFO] Bumping %BUMP_TYPE% version...
bump2version %BUMP_TYPE%
if errorlevel 1 (
    echo [ERROR] Version bump failed
    exit /b 1
)

REM Get new version
for /f "tokens=2 delims==" %%a in ('findstr /C:"current_version" .bumpversion.cfg') do (
    set NEW_VERSION=%%a
    set NEW_VERSION=!NEW_VERSION: =!
)
echo [SUCCESS] Version bumped: !CURRENT_VERSION! -^> !NEW_VERSION!

REM Push changes if not disabled
if not "%NO_PUSH%"=="true" (
    echo [INFO] Pushing changes to remote repository...

    REM Push commits and tags
    git push
    if errorlevel 1 (
        echo [ERROR] Failed to push commits
        exit /b 1
    )

    git push --tags
    if errorlevel 1 (
        echo [ERROR] Failed to push tags
        exit /b 1
    )

    echo [SUCCESS] Changes and tags pushed to remote repository
    echo [INFO] GitHub Actions will now build and create a release for v!NEW_VERSION!
) else (
    echo [WARNING] Changes not pushed (--no-push flag used)
    echo [INFO] To push manually, run:
    echo   git push
    echo   git push --tags
)

echo [SUCCESS] Version bump complete!
echo [INFO] New version: !NEW_VERSION!
echo [INFO] Tag created: v!NEW_VERSION!
goto :eof

:show_usage
echo Usage: %0 ^<bump_type^> [options]
echo.
echo Bump types:
echo   patch     Increment patch version (0.1.0 -^> 0.1.1)
echo   minor     Increment minor version (0.1.0 -^> 0.2.0)
echo   major     Increment major version (0.1.0 -^> 1.0.0)
echo.
echo Options:
echo   --dry-run     Show what would be done without making changes
echo   --no-push     Don't push changes to remote repository
echo   --help        Show this help message
echo.
echo Examples:
echo   %0 patch                    # Bump patch version and push
echo   %0 minor --dry-run          # See what minor bump would do
echo   %0 major --no-push          # Bump major version but don't push
exit /b 1