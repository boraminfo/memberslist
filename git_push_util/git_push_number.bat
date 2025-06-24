@echo off
setlocal enabledelayedexpansion

:: 📁 현재 BAT 파일의 경로
set "BASE_DIR=%~dp0"

:: 🔢 사용자 PC 선택
echo.
echo ================================
echo 💻 사용할 PC 환경을 선택하세요:
echo [1] pc_home
echo [2] pc_office
echo [3] pc_pohang
echo [4] pc_daejeon
echo ================================
set /p pc_choice="번호를 입력하세요 (1~3): "

if "%pc_choice%"=="1" (
    set "ENV_FILE=%BASE_DIR%pish_pc_home.env"
) else if "%pc_choice%"=="2" (
    set "ENV_FILE=%BASE_DIR%pish_pc_office.env"
) else if "%pc_choice%"=="3" (
    set "ENV_FILE=%BASE_DIR%pish_pc_pohang.env"
) else if "%pc_choice%"=="4" (
    set "ENV_FILE=%BASE_DIR%pish_pc_daejeon.env"
) else (
    echo ❌ 잘못된 선택입니다. 종료합니다.
    exit /b 1
)

:: 🌱 환경 변수 로드
for /f "tokens=1,2 delims==" %%A in (%ENV_FILE%) do (
    set "%%A=%%B"
)

:: 🔐 Git 사용자 계정 선택
echo.
echo ================================
echo 🔐 Git 사용자 계정을 선택하세요:
echo [1] %USER1_NAME%
echo [2] %USER2_NAME%
echo [3] %USER3_NAME%
echo ================================
set /p choice="번호를 입력하세요 (1~3): "

:: ✅ SSH 및 Remote 설정
if "%choice%"=="1" (
    set "SSH_KEY=%USER1_SSH%"
    set "REMOTE_URL=%USER1_REMOTE%"
) else if "%choice%"=="2" (
    set "SSH_KEY=%USER2_SSH%"
    set "REMOTE_URL=%USER2_REMOTE%"
) else if "%choice%"=="3" (
    set "SSH_KEY=%USER3_SSH%"
    set "REMOTE_URL=%USER3_REMOTE%"
) else (
    echo ❌ 잘못된 선택입니다.
    exit /b 1
)

:: 🔐 SSH 키 등록
echo 🔐 SSH 키 등록 중...
call ssh-agent > nul
call ssh-add "%SSH_KEY%"

:: 🚀 Git push
git add .
git commit -m "자동 커밋"
git push %REMOTE_URL%

endlocal
