@echo off
title madhushalasoftwareGpt — Build & Push to GitHub
color 0A
cls

echo.
echo  ================================================
echo   madhushalasoftwareGpt — Auto Build ^& Push
echo  ================================================
echo.

:: ── Ask for version number ───────────────────────────────────────
set /p VERSION="  Enter new version (e.g. 1.0.1): "

if "%VERSION%"=="" (
    echo   ERROR: Version cannot be empty!
    pause
    exit /b
)

echo.
echo  ------------------------------------------------
echo   Version: %VERSION%
echo  ------------------------------------------------
echo.

:: ── Update version.txt ───────────────────────────────────────────
echo %VERSION% > version.txt
echo   [1/6] version.txt updated to %VERSION% ... OK

:: ── Activate venv ────────────────────────────────────────────────
call venv\Scripts\activate
echo   [2/6] Virtual environment activated ... OK

:: ── Clean old build ──────────────────────────────────────────────
if exist dist   rmdir /s /q dist
if exist build  rmdir /s /q build
if exist madhushalasoftwareGpt.spec del madhushalasoftwareGpt.spec
echo   [3/6] Old build cleaned ... OK

:: ── Build EXE ────────────────────────────────────────────────────
echo.
echo   [4/6] Building EXE... (this takes 2-3 minutes)
echo.
pyinstaller --onefile --noconsole --add-data "version.txt;." --add-data "updater.py;." --name madhushalasoftwareGpt app.py

if not exist dist\madhushalasoftwareGpt.exe (
    echo.
    echo   ERROR: EXE build FAILED!
    pause
    exit /b
)
echo.
echo   [4/6] EXE built successfully!

:: ── Git commit & push ────────────────────────────────────────────
echo.
echo   [5/6] Pushing code to GitHub...
git add app.py version.txt updater.py
git commit -m "Release v%VERSION%"
git push origin main
echo   [5/6] Code pushed to GitHub ... OK

:: ── Create GitHub Release with EXE ──────────────────────────────
echo.
echo   [6/6] Uploading EXE to GitHub Releases...
gh release create v%VERSION% dist\madhushalasoftwareGpt.exe --title "Release v%VERSION%" --notes "Auto release v%VERSION%"

echo.
echo  ================================================
echo   ALL DONE! Release v%VERSION% is LIVE!
echo  ================================================
echo.
echo   Clients will auto-update next time they open the app!
echo.
pause
