@echo off
title madhushalasoftwareGpt — Auto Builder
color 0A
echo.
echo  ================================================
echo   Madhushala Auto Builder Starting...
echo  ================================================
echo.

:: Activate virtual environment
call venv\Scripts\activate

:: Check PyInstaller installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo  Installing PyInstaller...
    pip install pyinstaller
)

:: Run the watcher
python auto_build.py

pause
