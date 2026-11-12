@echo off
cd /d "%~dp0"
netstat -ano | findstr /c:":8989 " | findstr /c:"LISTENING" >nul
if not errorlevel 1 (
    echo Port 8989 is already in use - the local server must already be running.
    exit /b 0
)
color 0b
title aigenetic local server :8989
python -m http.server 8989
