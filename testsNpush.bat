@echo off
setlocal enabledelayedexpansion

:: Activate virtual environment if it exists
if exist "%~dp0.venv\Scripts\activate.bat" (
    call "%~dp0.venv\Scripts\activate.bat"
) else if exist "%~dp0venv\Scripts\activate.bat" (
    call "%~dp0venv\Scripts\activate.bat"
) else if exist "%~dp0env\Scripts\activate.bat" (
    call "%~dp0env\Scripts\activate.bat"
)

echo ========================================================
echo Running tests...
echo ========================================================

python -m pytest tests/
if errorlevel 1 (
    echo.
    echo ========================================================
    echo [FAILED] Tests failed. Aborting commit and push.
    echo ========================================================
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo [PASSED] All tests passed! Proceeding to commit and push...
echo ========================================================

git add .

set "COMMIT_MSG=%*"

if "!COMMIT_MSG!"=="" (
    set "COMMIT_MSG=test: pass all tests and update codebase"
)

:: Check if there are staged changes to commit
git diff --cached --quiet
if errorlevel 1 (
    echo Committing changes with message: "!COMMIT_MSG!"
    git commit -m "!COMMIT_MSG!"
    if errorlevel 1 (
        echo [ERROR] Git commit failed.
        exit /b %errorlevel%
    )
) else (
    echo No staged changes to commit.
)

echo Pushing changes to remote...
git push
if errorlevel 1 (
    echo [ERROR] Git push failed.
    exit /b %errorlevel%
)

echo.
echo ========================================================
echo [SUCCESS] Tests passed, changes committed and pushed!
echo ========================================================