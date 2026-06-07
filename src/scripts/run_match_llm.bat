@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "PROJECT_ROOT=%CD%"
set "LOG_DIR=%PROJECT_ROOT%\logs"
set "ERROR_LOG_DIR=%PROJECT_ROOT%\errorlogs"
set "REPLAY_DIR=%PROJECT_ROOT%\replays"
set "VIEW_DIR=%PROJECT_ROOT%\view"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%ERROR_LOG_DIR%" mkdir "%ERROR_LOG_DIR%"
if not exist "%REPLAY_DIR%" mkdir "%REPLAY_DIR%"

echo Cleaning current-match logs...

del /q "%LOG_DIR%\decision_log.jsonl" >nul 2>nul
del /q "%LOG_DIR%\llm_decisions.jsonl" >nul 2>nul
del /q "%LOG_DIR%\llm_error_log.jsonl" >nul 2>nul
del /q "%LOG_DIR%\agent_debug.log" >nul 2>nul
del /q "%LOG_DIR%\latest_match_console.txt" >nul 2>nul

for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "MATCH_ID=%%i"

set "LLM_PLAYER=player_0"
set "LLM_MODEL=qwen2.5:1.5b"

set "REPLAY_OUTPUT=%REPLAY_DIR%\lux_s3_llm_vs_rule_%MATCH_ID%.html"
set "FIXED_REPLAY=%REPLAY_DIR%\lux_s3_llm_vs_rule_replay.html"
set "CONSOLE_LOG=%LOG_DIR%\match_console_%MATCH_ID%.txt"
set "LATEST_CONSOLE_LOG=%LOG_DIR%\latest_match_console.txt"
set "DECISION_LOG=%LOG_DIR%\decision_log.jsonl"
set "ERROR_LOG=%LOG_DIR%\llm_error_log.jsonl"
set "MATCH_HISTORY=%LOG_DIR%\match_history.jsonl"

echo.
echo Match ID:
echo   %MATCH_ID%
echo.
echo LLM player:
echo   %LLM_PLAYER%
echo.
echo LLM model:
echo   %LLM_MODEL%
echo.
echo Replay output:
echo   %REPLAY_OUTPUT%
echo.
echo Console log:
echo   %CONSOLE_LOG%
echo.
echo Make sure Ollama is running:
echo   ollama serve
echo.
echo Make sure model exists:
echo   ollama list
echo.
echo Running Lux AI Season 3 local match...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$env:LLM_PLAYER='%LLM_PLAYER%';" ^
  "$env:LLM_MODEL='%LLM_MODEL%';" ^
  "& '.\.venv\Scripts\luxai-s3.exe' 'main.py' 'main.py' '--output' '%REPLAY_OUTPUT%' 2>&1 | Tee-Object -FilePath '%CONSOLE_LOG%' | Tee-Object -FilePath '%LATEST_CONSOLE_LOG%';" ^
  "exit $LASTEXITCODE"

set "MATCH_EXIT_CODE=%ERRORLEVEL%"

if not "%MATCH_EXIT_CODE%"=="0" (
    echo.
    echo [ERROR] Lux LLM vs Rule match failed.
    echo Console log:
    echo   %CONSOLE_LOG%
    echo.
    pause
    exit /b %MATCH_EXIT_CODE%
)

if exist "%REPLAY_OUTPUT%" (
    copy /y "%REPLAY_OUTPUT%" "%FIXED_REPLAY%" >nul
)

echo.
echo Recording match result from console log...

python record_match_result_from_console.py ^
  --match-id "%MATCH_ID%" ^
  --console-log "%CONSOLE_LOG%" ^
  --decision-log "%DECISION_LOG%" ^
  --error-log "%ERROR_LOG%" ^
  --history-log "%MATCH_HISTORY%" ^
  --replay "%REPLAY_OUTPUT%" ^
  --llm-player "%LLM_PLAYER%" ^
  --llm-model "%LLM_MODEL%"

echo.
echo Match finished.
echo Replay:
echo   %REPLAY_OUTPUT%
echo Fixed replay:
echo   %FIXED_REPLAY%
echo Decision log:
echo   %DECISION_LOG%
echo Error log:
echo   %ERROR_LOG%
echo Match history:
echo   %MATCH_HISTORY%
echo Console log:
echo   %CONSOLE_LOG%
echo Latest console log:
echo   %LATEST_CONSOLE_LOG%
echo.

pause
endlocal