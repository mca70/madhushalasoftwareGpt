@echo off
title madhushalasoftwareGpt — GitHub First Time Setup
color 0B
cls

echo.
echo  ================================================
echo   GitHub First-Time Setup for madhushalasoftwareGpt
echo  ================================================
echo.
echo  This will:
echo   1. Connect your project to GitHub
echo   2. Install GitHub CLI (gh)
echo   3. Push all files to GitHub
echo   4. Create first release
echo.
pause

:: ── Install GitHub CLI ───────────────────────────────────────────
echo.
echo  [1/5] Installing GitHub CLI (gh)...
winget install --id GitHub.cli -e --source winget
echo  [1/5] GitHub CLI installed!

:: ── Git first time config ────────────────────────────────────────
echo.
echo  [2/5] Configuring Git...
git config --global user.name "Madhushala Software"
git config --global user.email "abmtechno@email.com"
echo  [2/5] Git configured!

:: ── Init repo and connect ────────────────────────────────────────
echo.
echo  [3/5] Connecting to GitHub...
git init
git remote remove origin 2>nul
git remote add origin https://github.com/mca70/madhushalasoftwareGpt.git
git branch -M main
echo  [3/5] Connected to GitHub!

:: ── Login to GitHub CLI ──────────────────────────────────────────
echo.
echo  [4/5] Login to GitHub (browser will open)...
gh auth login
echo  [4/5] GitHub login done!

:: ── Push all files ───────────────────────────────────────────────
echo.
echo  [5/5] Pushing files to GitHub...
git add .
git commit -m "Initial setup v1.0.0"
git push -u origin main
echo  [5/5] Files pushed!

echo.
echo  ================================================
echo   SETUP COMPLETE!
echo   Now use BUILD_AND_PUSH.bat for every update!
echo  ================================================
echo.
pause
