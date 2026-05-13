@echo off
echo =====================================
echo  FLEX Feedback Automator
echo =====================================

:: Check if venv exists
if not exist "Python\python.exe" (
    echo ERROR: Python folder not found.
    echo Make sure you extracted the full zip folder.
    echo.
    pause
    exit /b 1
)

:: Run using embedded Python
echo Launching...
Python\python.exe main.py

:: Keep window open if an error occurs
if %errorlevel% neq 0 (
    echo.
    echo Something went wrong. Screenshot this and contact the developer.
    pause
)