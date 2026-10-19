@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [SmartPhoto] First run: creating virtual environment...
    python -m venv .venv || goto :error
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto :error
)

".venv\Scripts\python.exe" download_models.py || echo [SmartPhoto] Some models failed to download, see messages above.

echo [SmartPhoto] Starting... the browser will open automatically.
echo [SmartPhoto] Add --lan to allow phones on the same Wi-Fi:  start.bat --lan
".venv\Scripts\python.exe" app.py %*
pause
exit /b 0

:error
echo [SmartPhoto] Setup failed. Please check the messages above.
pause
exit /b 1
