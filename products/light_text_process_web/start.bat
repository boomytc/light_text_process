@echo off
setlocal

cd /d "%~dp0"

if "%LIGHT_TEXT_PROCESS_WEB_HOST%"=="" set "LIGHT_TEXT_PROCESS_WEB_HOST=127.0.0.1"
if "%LIGHT_TEXT_PROCESS_WEB_PORT%"=="" set "LIGHT_TEXT_PROCESS_WEB_PORT=8011"

.venv\Scripts\python.exe -m uvicorn app:app --host "%LIGHT_TEXT_PROCESS_WEB_HOST%" --port "%LIGHT_TEXT_PROCESS_WEB_PORT%"
