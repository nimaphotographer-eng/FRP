@echo off
setlocal
title Huawei FRP Assistant 1.3 - Local Build
echo ============================================================
echo Huawei FRP Assistant 1.3
echo ============================================================
where py >nul 2>nul
if errorlevel 1 (
  where python >nul 2>nul
  if errorlevel 1 (
    echo Python is not installed. Use GitHub Actions for cloud building.
    pause
    exit /b 1
  )
  set PY=python
) else (
  set PY=py
)
%PY% -m pip install -r requirements.txt
if errorlevel 1 goto :fail
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name HuaweiFRPAssistant ^
  --add-data "device_database.json;." app.py
if errorlevel 1 goto :fail
echo.
echo BUILD SUCCEEDED
echo Output: dist\HuaweiFRPAssistant.exe
pause
exit /b 0
:fail
echo.
echo BUILD FAILED
pause
exit /b 1
