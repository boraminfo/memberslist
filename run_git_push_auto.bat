@echo off
:: 🏁 현재 디렉토리 기준
set "BASE_DIR=%~dp0"

:: 📄 자동 환경 선택용 env 파일 (ex: pish_pc_home.env)
set "ENV_FILE_PATH=%BASE_DIR%env_active.txt"

:: ❓ env 파일이 없으면 종료
if not exist "%ENV_FILE_PATH%" (
    echo ❌ env_active.txt 파일이 존재하지 않습니다.
    echo    예시: pish_pc_home.env
    pause
    exit /b 1
)

:: 📦 env 파일명 읽기
set /p ENV_FILE=<"%ENV_FILE_PATH%"

:: 📢 확인 메시지
echo ✅ 자동 선택된 환경 파일: %ENV_FILE%

:: 🐍 Python 실행 (가상환경이 있을 경우 venv 경로 포함 가능)
python git_push_full_setup.py "%ENV_FILE%"

pause
