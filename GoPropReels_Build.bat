@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0GoPropReels_Build.ps1"
