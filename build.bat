@echo off
cd /d "%~dp0"
echo Cleaning dist folder...
REM if exist "dist" rmdir /s /q "dist"
echo Building site...
call npm run build
if %errorlevel% neq 0 (
    echo Build Failed!
    exit /b %errorlevel%
)
echo Build Success!
