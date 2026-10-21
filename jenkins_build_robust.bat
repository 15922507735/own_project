@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
cd /d "%~dp0"

echo ============================================================
echo   QY_API_AUTO  CI Build
echo   Workspace : %CD%
echo ============================================================

REM ------------------------------------------------------------
REM  [1/4] Virtual environment
REM ------------------------------------------------------------
if exist ".venv\Scripts\python.exe" goto :venv_ready

echo [1/4] Creating virtualenv .venv ...
py -3 -m venv .venv 2>nul
if errorlevel 1 python -m venv .venv
if errorlevel 1 (
    echo [1/4] FATAL: failed to create virtualenv .venv
    exit /b 1
)

:venv_ready
set "PY=%CD%\.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo [1/4] FATAL: %PY% not found
    exit /b 1
)
echo [1/4] Python : %PY%
"%PY%" --version

REM ------------------------------------------------------------
REM  [2/4] Dependencies
REM ------------------------------------------------------------
echo [2/4] Installing dependencies from requirements.txt ...
"%PY%" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 echo [2/4] WARNING: pip install failed - continuing to pytest anyway

REM ------------------------------------------------------------
REM  [3/4] Allure results directory
REM      The Jenkins "Allure Report" build step reads ./allure-results.
REM      Creating it up front avoids the "allure-results does not exist"
REM      warning and guarantees a report artifact is archived.
REM ------------------------------------------------------------
if not exist "allure-results" mkdir "allure-results"

REM ------------------------------------------------------------
REM  [4/4] Run pytest, with retry
REM      pytest.ini already sets testpaths=./scripts and
REM      --alluredir ./allure-results, so no extra arguments are needed.
REM ------------------------------------------------------------
set "MAX_ATTEMPTS=3"
set "attempt=0"
set "final_code=1"

:run_pytest
set /a attempt+=1
echo.
echo [4/4] pytest - attempt !attempt! of !MAX_ATTEMPTS! ...

"%PY%" -m pytest
if errorlevel 1 goto :maybe_retry

set "final_code=0"
echo [4/4] pytest PASSED on attempt !attempt!.
goto :finish

:maybe_retry
set "final_code=1"
if !attempt! geq !MAX_ATTEMPTS! goto :finish
echo [4/4] attempt !attempt! failed - retrying in 10 seconds ...
ping -n 11 127.0.0.1 >nul 2>&1
goto :run_pytest

REM ------------------------------------------------------------
REM  Summary
REM ------------------------------------------------------------
:finish
echo.
echo ============================================================
echo   Build finished - exit code !final_code!
echo   Allure results : %CD%\allure-results
echo ============================================================
endlocal & exit /b %final_code%