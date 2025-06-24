@echo off
cd /d %~dp0
echo 🚀 Python Git Push 도우미 실행 중...

:: 가상환경 python 경로
set PY_PATH=venv310\Scripts\python.exe

if exist %PY_PATH% (
    %PY_PATH% git_push_selectable.py
) else (
    echo ❌ Python 가상환경을 찾을 수 없습니다: %PY_PATH%
    pause
)
