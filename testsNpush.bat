@echo off
setlocal

rem ============================================================================
rem  testsNpush.bat - run the website test suite; commit + push only on request.
rem
rem    testsNpush.bat                            run the tests, nothing else
rem    testsNpush.bat --push                     tests, then commit + push
rem    testsNpush.bat --push "feat: my message"  same, with your commit message
rem
rem  Without --push this never touches git, so it is safe to run any time.
rem  The local site on http://localhost:8989 is started by this script calling
rem  localServer.bat, which exits straight away if it is already running.
rem ============================================================================

rem Work from the repo root wherever this was launched from (double-click,
rem another folder, a VS Code task...). setlocal restores the caller's folder.
cd /d "%~dp0"

set "PUSH="
set "COMMIT_MSG="

:parse_args
if "%~1"=="" goto args_done
set "ARG=%~1"
if /i "%ARG%"=="--push" (
    set "PUSH=1"
) else if /i "%ARG%"=="-h" (
    goto usage
) else if /i "%ARG%"=="--help" (
    goto usage
) else if "%ARG:~0,1%"=="-" (
    echo [ERROR] Unknown option "%ARG%".
    echo.
    goto usage_error
) else if defined COMMIT_MSG (
    set "COMMIT_MSG=%COMMIT_MSG% %ARG%"
) else (
    set "COMMIT_MSG=%ARG%"
)
shift
goto parse_args
:args_done

rem Use the project venv's python.exe directly. Its activate.bat hard-codes the
rem folder the venv was created in, so it breaks whenever the repo is moved.
set "PY="
for %%V in (.venv venv env) do (
    if not defined PY if exist "%%V\Scripts\python.exe" set "PY=%CD%\%%V\Scripts\python.exe"
)
if not defined PY set "PY=python"

"%PY%" -c "import pytest, playwright" >nul 2>&1
if errorlevel 1 goto missing_deps

echo ========================================================
echo Running tests with %PY%
echo ========================================================

rem Start the local site in its own minimized window. localServer.bat exits
rem straight away if one is already running.
start "aigenetic local server" /min cmd /c localServer.bat

"%PY%" -m pytest tests
set "RC=%errorlevel%"
if not "%RC%"=="0" goto tests_failed

echo.
echo ========================================================
if not defined PUSH (
    echo [PASSED] All tests passed. Nothing was committed or pushed.
    if defined COMMIT_MSG echo          Your commit message was ignored because --push was not given.
    echo          To commit and push, run: testsNpush.bat --push
    echo ========================================================
    exit /b 0
)
echo [PASSED] All tests passed. Committing and pushing...
echo ========================================================

git symbolic-ref -q HEAD >nul 2>&1
if errorlevel 1 (
    echo [ERROR] HEAD is detached. Check out a branch before pushing.
    exit /b 1
)

if not defined COMMIT_MSG set "COMMIT_MSG=test: pass all tests and update codebase"

git add -A
if errorlevel 1 goto git_failed

git diff --cached --quiet
if errorlevel 1 (
    echo Committing:
    git status --short
    git commit -m "%COMMIT_MSG%"
    if errorlevel 1 goto git_failed
) else (
    echo No changes to commit.
)

echo Pushing to remote...
git rev-parse --abbrev-ref --symbolic-full-name @{u} >nul 2>&1
if errorlevel 1 (
    echo No upstream branch yet - pushing to origin and tracking it.
    git push -u origin HEAD
) else (
    git push
)
if errorlevel 1 goto git_failed

echo.
echo ========================================================
echo [SUCCESS] Tests passed, changes committed and pushed.
echo ========================================================
exit /b 0


:tests_failed
echo.
echo ========================================================
echo [FAILED] Tests failed. Nothing was committed or pushed.
echo          Report: tests\reports\latest.html
echo ========================================================
exit /b %RC%

:git_failed
echo.
echo [ERROR] Git step failed - see the message above.
exit /b 1

:missing_deps
echo [ERROR] pytest and playwright are not installed for: %PY%
echo         Install them with:
echo           "%PY%" -m pip install -r tests\requirements-test.txt
echo           "%PY%" -m playwright install chromium
exit /b 1

:usage
echo Usage: testsNpush.bat [--push] ["commit message"]
echo.
echo   (no args)         Run the tests only. Never commits or pushes.
echo   --push            Run the tests; if they pass, git add -A, commit, push.
echo   "commit message"  Commit message to use with --push.
echo                     Default: "test: pass all tests and update codebase"
exit /b 0

:usage_error
echo Usage: testsNpush.bat [--push] ["commit message"]
exit /b 2
