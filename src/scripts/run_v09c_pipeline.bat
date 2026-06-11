@echo off
setlocal enabledelayedexpansion

title Lux S3 v0.9-C Pipeline

echo ============================================================
echo Lux S3 v0.9-C Sensor / Energy Overlay Pipeline
echo ============================================================
echo.

cd /d "%~dp0"

echo [PIPELINE] Project root:
echo   %cd%
echo.

echo [PIPELINE] Cleaning old frame/viewer logs...
if exist "logs\frame_log.jsonl" (
    del /f /q "logs\frame_log.jsonl"
    echo   deleted logs\frame_log.jsonl
) else (
    echo   skip logs\frame_log.jsonl
)

if exist "logs\viewer_frames.json" (
    del /f /q "logs\viewer_frames.json"
    echo   deleted logs\viewer_frames.json
) else (
    echo   skip logs\viewer_frames.json
)

if exist "logs\agent_debug.log" (
    del /f /q "logs\agent_debug.log"
    echo   deleted logs\agent_debug.log
) else (
    echo   skip logs\agent_debug.log
)

echo.
echo [PIPELINE] Running Lux S3 LLM match...
echo ------------------------------------------------------------
call run_match_llm.bat
set MATCH_EXIT_CODE=%ERRORLEVEL%
echo ------------------------------------------------------------

if not "%MATCH_EXIT_CODE%"=="0" (
    echo.
    echo [PIPELINE ERROR] run_match_llm.bat failed with exit code %MATCH_EXIT_CODE%.
    echo Please check the console output and logs folder.
    pause
    exit /b %MATCH_EXIT_CODE%
)

echo.
echo [PIPELINE] Match completed.
echo.

if not exist "logs\frame_log.jsonl" (
    echo [PIPELINE ERROR] logs\frame_log.jsonl was not generated.
    echo This usually means frame logging did not run or the agent crashed early.
    pause
    exit /b 1
)

echo [PIPELINE] Building viewer_frames.json...
python view\build_viewer_frames.py
set BUILD_EXIT_CODE=%ERRORLEVEL%

if not "%BUILD_EXIT_CODE%"=="0" (
    echo.
    echo [PIPELINE ERROR] build_viewer_frames.py failed with exit code %BUILD_EXIT_CODE%.
    pause
    exit /b %BUILD_EXIT_CODE%
)

if not exist "logs\viewer_frames.json" (
    echo.
    echo [PIPELINE ERROR] logs\viewer_frames.json was not generated.
    pause
    exit /b 1
)

echo.
echo [PIPELINE] Checking v0.9-C fields...
echo ------------------------------------------------------------

findstr /C:"v0.9-C" "logs\viewer_frames.json" >nul
if "%ERRORLEVEL%"=="0" (
    echo   [OK] agent version contains v0.9-C
) else (
    echo   [WARN] v0.9-C was not found in viewer_frames.json
)

findstr /C:"visible_tiles" "logs\viewer_frames.json" >nul
if "%ERRORLEVEL%"=="0" (
    echo   [OK] visible_tiles field found
) else (
    echo   [WARN] visible_tiles field not found
)

findstr /C:"energy_tiles" "logs\viewer_frames.json" >nul
if "%ERRORLEVEL%"=="0" (
    echo   [OK] energy_tiles field found
) else (
    echo   [WARN] energy_tiles field not found
)

findstr /C:"relic_candidate_tiles" "logs\viewer_frames.json" >nul
if "%ERRORLEVEL%"=="0" (
    echo   [OK] relic_candidate_tiles field found
) else (
    echo   [WARN] relic_candidate_tiles field not found
)

echo ------------------------------------------------------------
echo.

echo [PIPELINE] Summary statistics:
python -c "import json; d=json.load(open('logs/viewer_frames.json',encoding='utf-8')); fs=d.get('frames',[]); print('frames=',len(fs)); print('max visible=',max((len(f.get('vision',{}).get('visible_tiles',[])) for f in fs), default=0)); print('max explored=',max((len(f.get('vision',{}).get('explored_tiles',[])) for f in fs), default=0)); print('max energy=',max((len(f.get('vision',{}).get('energy_tiles',[])) for f in fs), default=0)); print('max candidates=',max((len(f.get('memory',{}).get('relic_candidate_tiles',[])) for f in fs), default=0))"

echo.
echo ============================================================
echo Pipeline finished.
echo ============================================================
echo.
echo Next step:
echo   1. Start server if it is not running:
echo      python -m http.server 8080
echo.
echo   2. Open:
echo      http://127.0.0.1:8080/s3_log_driven_gameview.html
echo.
echo Viewer shortcuts:
echo   V = visible tiles
echo   X = explored memory
echo   E = energy memory
echo   R = relic nodes
echo   C = candidate tiles
echo   S = stale tiles
echo   T = unit target lines
echo.
pause
endlocal