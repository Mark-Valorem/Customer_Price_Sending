@echo off
:: Customer Database Migration & Enhanced Verification System v2.0
:: Launch Script for Windows
::
:: CRITICAL BUSINESS SYSTEM - Enhanced with customer database management
:: and multi-layer verification to prevent sending wrong pricing data.

title VALOREM CHEMICALS - Customer System v2.0

echo.
echo ================================================================================
echo VALOREM CHEMICALS - Customer Database Migration ^& Verification System v2.0
echo ================================================================================
echo.
echo CRITICAL BUSINESS SYSTEM
echo Enhanced with customer database management and multi-layer verification
echo to prevent sending wrong pricing data to customers.
echo.
echo Zero Tolerance Policy: Better to not send than send wrong data
echo.
echo ================================================================================
echo SYSTEM COMPONENTS
echo ================================================================================
echo.
echo [1] Enhanced Dashboard v2.0     - Main interface with customer management
echo [2] Migration Script           - Convert Excel to JSON database
echo [3] Verification Tests         - Run comprehensive security tests
echo [4] Original Dashboard         - Legacy interface (backup option)
echo [5] Customer Database          - View current database
echo [6] Audit Logs                - Review system activity logs
echo [7] Exit
echo.

:MENU
echo ================================================================================
set /p choice="Select option (1-7): "

if "%choice%"=="1" goto DASHBOARD_V2
if "%choice%"=="2" goto MIGRATION
if "%choice%"=="3" goto TESTS
if "%choice%"=="4" goto DASHBOARD_ORIGINAL
if "%choice%"=="5" goto VIEW_DATABASE
if "%choice%"=="6" goto VIEW_LOGS
if "%choice%"=="7" goto EXIT
echo Invalid choice. Please try again.
goto MENU

:DASHBOARD_V2
echo.
echo ================================================================================
echo LAUNCHING ENHANCED DASHBOARD v2.0
echo ================================================================================
echo.
echo Features:
echo - Customer database management
echo - Real-time verification status
echo - Multi-layer security checks
echo - Audit trail integration
echo.
echo Starting dashboard...
python dashboard_v2.py
goto MENU

:MIGRATION
echo.
echo ================================================================================
echo EXCEL TO JSON MIGRATION
echo ================================================================================
echo.
echo IMPORTANT: Close Excel file before proceeding!
echo.
echo This will migrate customer data from CustomerDetails worksheet
echo to customer_database_v2.json with comprehensive verification.
echo.
set /p confirm="Continue with migration? (y/n): "
if /i "%confirm%"=="y" (
    echo Running migration...
    python migrate_excel_to_json_v2.py
    echo.
    echo Migration completed. Check logs/migration_v2.log for details.
    pause
) else (
    echo Migration cancelled.
)
goto MENU

:TESTS
echo.
echo ================================================================================
echo COMPREHENSIVE VERIFICATION TESTS
echo ================================================================================
echo.
echo Running critical security tests:
echo - Domain verification tests (CRITICAL)
echo - File existence validation
echo - Security violation detection
echo - End-to-end workflow tests
echo.
echo This may take a few moments...
python tests/test_verification_system_v2.py
echo.
echo Test results above. Review any failures before using system.
pause
goto MENU

:DASHBOARD_ORIGINAL
echo.
echo ================================================================================
echo LAUNCHING ORIGINAL DASHBOARD (Legacy)
echo ================================================================================
echo.
echo Note: This is the original dashboard without v2.0 enhancements.
echo Consider using Enhanced Dashboard v2.0 for full customer management.
echo.
python dashboard.py
goto MENU

:VIEW_DATABASE
echo.
echo ================================================================================
echo CUSTOMER DATABASE CONTENTS
echo ================================================================================
echo.
if exist customer_database_v2.json (
    echo Database file: customer_database_v2.json
    echo.
    python -c "import json; data=json.load(open('customer_database_v2.json')); print(f'Version: {data[\"version\"]}'); print(f'Customers: {len(data[\"customers\"])}'); print(f'Created: {data[\"created_date\"]}'); print('\nCustomer List:'); [print(f'  - {c[\"company_name\"]} ({c[\"email_domain\"]})') for c in data['customers'] if c.get('active', True)]"
    echo.
    echo Use Enhanced Dashboard v2.0 to manage customers.
) else (
    echo ERROR: customer_database_v2.json not found.
    echo Run migration first to create database.
)
echo.
pause
goto MENU

:VIEW_LOGS
echo.
echo ================================================================================
echo SYSTEM LOGS
echo ================================================================================
echo.
echo Available log files:
if exist logs\ (
    dir logs\*.log /b 2>nul
    dir logs\*.json /b 2>nul
    echo.
    echo Log directory: logs\
    echo.
    echo Key log files:
    echo - migration_v2.log      : Excel to JSON migration details
    echo - verification_v2.log   : Customer verification attempts
    echo - audit_log_v2.json     : Complete audit trail
    echo - audit_system.log      : System operation logs
    echo.
    set /p logfile="Enter log filename to view (or press Enter to continue): "
    if not "!logfile!"=="" (
        if exist logs\!logfile! (
            echo.
            echo Contents of logs\!logfile!:
            echo ----------------------------------------
            type logs\!logfile!
            echo ----------------------------------------
        ) else (
            echo File not found: logs\!logfile!
        )
    )
) else (
    echo No logs directory found. System hasn't been used yet.
)
echo.
pause
goto MENU

:EXIT
echo.
echo ================================================================================
echo SYSTEM SHUTDOWN
echo ================================================================================
echo.
echo Customer Database Migration ^& Verification System v2.0
echo.
echo REMEMBER:
echo - Always verify before sending emails
echo - Review audit logs regularly
echo - System prevents wrong data exposure
echo - Contact support for any verification errors
echo.
echo Thank you for using the enhanced customer system!
echo.
pause
exit

:ERROR
echo.
echo ================================================================================
echo ERROR
echo ================================================================================
echo.
echo An error occurred running the system.
echo.
echo Troubleshooting:
echo 1. Ensure Python is installed and in PATH
echo 2. Check that all required files exist
echo 3. Verify customer_database_v2.json exists (run migration if needed)
echo 4. Review log files in logs\ directory
echo.
echo If problems persist, check README_v2.md for detailed troubleshooting.
echo.
pause
goto MENU