@echo off
title madhushalasoftwareGpt - EXE Builder
color 0A

echo.
echo  ============================================
echo    madhushalasoftwareGpt - EXE Builder
echo  ============================================
echo.

:: ── STEP 1: Check Python ──────────────────────
echo [1/5] Checking Python installation...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo  Python found!
echo.

:: ── STEP 2: Create Virtual Environment ────────
echo [2/5] Creating virtual environment...
IF NOT EXIST "venv" (
    python -m venv venv
    echo  Virtual environment created!
) ELSE (
    echo  Virtual environment already exists, skipping...
)
echo.

:: ── STEP 3: Activate + Install packages ───────
echo [3/5] Installing required packages (Flask + PyInstaller)...
call venv\Scripts\activate.bat
pip install flask pyinstaller --quiet
echo  Packages installed!
echo.

:: ── STEP 4: Build EXE ─────────────────────────
echo [4/5] Building EXE... (This may take 2-3 minutes)
echo  Please wait...
pyinstaller --onefile --noconsole --name madhushalasoftwareGpt app.py
echo.

:: ── STEP 5: Check result ──────────────────────
echo [5/5] Checking output...
IF EXIST "dist\madhushalasoftwareGpt.exe" (
    echo.
    echo  ============================================
    echo    SUCCESS! EXE built successfully!
    echo  ============================================
    echo.
    echo    Location: dist\madhushalasoftwareGpt.exe
    echo.
    echo    You can now:
    echo    - Double-click the EXE to run it
    echo    - Share it with any Windows PC
    echo    - No Python needed on client machine!
    echo.
    echo  Opening dist folder...
    explorer dist
) ELSE (
    echo  BUILD FAILED! Check the errors above.
)

echo.
pause
