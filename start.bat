@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Resolve base directory of this script
set "BASE_DIR=%~dp0"
set "API_DIR=%BASE_DIR%DrinksRobot\API"
set "INDEX_HTML=%BASE_DIR%DrinksRobot\Web\HTML\index.html"

REM Choose Python launcher
where python >nul 2>&1
if errorlevel 1 (
  set "PYTHON=py -3"
) else (
  set "PYTHON=python"
)

REM Start backend in a new window
pushd "%API_DIR%"
start "DrinksRobot API" cmd /c "%PYTHON% startup.py"
popd

REM Wait for backend to respond (try up to ~20s)
set "CHECK_URL=http://localhost:5001/robot_progress"
where curl >nul 2>&1
if errorlevel 1 (
  REM No curl, do a simple wait
  timeout /t 5 /nobreak >nul
) else (
  for /l %%I in (1,1,20) do (
    curl -s -o NUL -m 1 "%CHECK_URL%" >nul 2>&1
    if not errorlevel 1 goto :OPEN_BROWSER
    timeout /t 1 /nobreak >nul
  )
)

:OPEN_BROWSER
start "" "%INDEX_HTML%"

endlocal
exit /b 0
