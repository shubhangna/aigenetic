@echo off
setlocal enabledelayedexpansion

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
if "%COMMIT_MSG%"=="" (
    set /p COMMIT_MSG="Enter commit message (press Enter for default): "
)
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