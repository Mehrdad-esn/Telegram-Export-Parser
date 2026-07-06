@echo off
title Telegram Export Parser Launcher
cd /d "%~dp0"

cls
echo =======================================================================
echo             Telegram Export Parser - Automation Starter
echo =======================================================================
echo.
echo [1/3] Starting Backend (FastAPI) on http://localhost:8000...
start "Telegram Parser Backend" cmd /k run-backend.bat

echo [2/3] Starting Frontend (Next.js) on http://localhost:3000...
start "Telegram Parser Frontend" cmd /k run-frontend.bat

echo.
echo [3/3] Opening Web Interface...
echo Waiting 5 seconds for services to start...
timeout /t 5 /nobreak > nul

start http://localhost:3000

echo.
echo =======================================================================
echo  Services started successfully!
echo  You can close this window now.
echo  Please keep the backend and frontend command prompt windows open.
echo =======================================================================
echo.
pause
