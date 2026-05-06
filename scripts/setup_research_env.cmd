@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."

set "PYTHON_BIN=%PYTHON_BIN%"
if "%PYTHON_BIN%"=="" (
    where py >nul 2>&1
    if %ERRORLEVEL%==0 (
        py -3 "%SCRIPT_DIR%setup_research_env.py" --workspace "%REPO_ROOT%" %*
        exit /b %ERRORLEVEL%
    )

    where python >nul 2>&1
    if %ERRORLEVEL%==0 (
        python "%SCRIPT_DIR%setup_research_env.py" --workspace "%REPO_ROOT%" %*
        exit /b %ERRORLEVEL%
    )

    echo [error] Could not find py or python on PATH.
    exit /b 1
)

"%PYTHON_BIN%" "%SCRIPT_DIR%setup_research_env.py" --workspace "%REPO_ROOT%" %*
exit /b %ERRORLEVEL%
