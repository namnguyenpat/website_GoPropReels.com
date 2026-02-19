@echo off
cd /d "%~dp0"
echo Starting Local Preview on Port 4323...
call npm run preview -- --port 4323 --host
pause
