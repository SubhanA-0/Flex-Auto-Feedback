@echo off
echo =====================================
echo    Starting FLEX Feedback Automator  
echo =====================================

:: 1. Ensure required packages are installed
echo Checking dependencies...
pip install -q selenium webdriver-manager

:: 2. Launch the Tkinter App
echo Launching UI...
python main.py

:: 3. Keep the window open if an error occurs
pause