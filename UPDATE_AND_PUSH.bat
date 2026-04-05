@echo off
title madhushalasoftwareGpt — Update & Push to GitHub
color 0A
cls

echo.
echo  ================================================
echo   madhushalasoftwareGpt — Update ^& Push Tool
echo   ABM Technomatrix Pvt. Ltd.
echo  ================================================
echo.

:: ── Ask for version number ───────────────────────────────────────
set /p VERSION="  Enter new version number (e.g. 1.0.2): "

if "%VERSION%"=="" (
    echo.
    echo   ERROR: Version cannot be empty!
    pause
    exit /b
)

echo.
echo  ------------------------------------------------
echo   Starting update process for v%VERSION%...
echo  ------------------------------------------------
echo.

:: ── Step 1: Update version.txt ───────────────────────────────────
echo %VERSION%> version.txt
echo   [1/7] version.txt updated to v%VERSION% ... OK

:: ── Step 2: Activate venv ────────────────────────────────────────
call venv\Scripts\activate
if errorlevel 1 (
    echo   ERROR: Virtual environment not found!
    echo   Make sure venv folder exists in this directory.
    pause
    exit /b
)
echo   [2/7] Virtual environment activated ... OK

:: ── Step 3: Kill old EXE if running ─────────────────────────────
taskkill /f /im madhushalasoftwareGpt.exe >nul 2>&1
echo   [3/7] Old EXE stopped ... OK

:: ── Step 4: Clean old build files ───────────────────────────────
if exist dist   rmdir /s /q dist
if exist build  rmdir /s /q build
if exist madhushalasoftwareGpt.spec del /f madhushalasoftwareGpt.spec
echo   [4/7] Old build cleaned ... OK

:: ── Step 5: Build new EXE ────────────────────────────────────────
echo.
echo   [5/7] Building EXE... (please wait 3-4 minutes)
echo.
pyinstaller --onefile --noconsole --add-data "version.txt;." --add-data "updater.py;." --name madhushalasoftwareGpt app.py

if not exist dist\madhushalasoftwareGpt.exe (
    echo.
    echo   ERROR: EXE build FAILED!
    echo   Please check the error above and try again.
    pause
    exit /b
)
echo.
echo   [5/7] EXE built successfully! ... OK

:: ── Step 6: Push code to GitHub ─────────────────────────────────
echo.
echo   [6/7] Pushing code to GitHub...
git add -A
git commit -m "Release v%VERSION%"
git push origin main
echo   [6/7] Code pushed to GitHub ... OK

:: ── Step 7: Create GitHub Release + Upload EXE ──────────────────
echo.
echo   [7/7] Uploading EXE to GitHub Release...
gh release create v%VERSION% dist\madhushalasoftwareGpt.exe --title "Release v%VERSION%" --notes "madhushalasoftwareGpt v%VERSION% - Updated"

echo.
echo  ================================================
echo   SUCCESS! Release v%VERSION% is LIVE!
echo  ================================================
echo.
echo   Download Page:
echo   https://mca70.github.io/madhushalasoftwareGpt
echo.
echo   Direct EXE Link:
echo   https://github.com/mca70/madhushalasoftwareGpt/releases/latest/download/madhushalasoftwareGpt.exe
echo.
echo   Clients will auto-update next time they open the app!
echo  ================================================
echo.
pause
