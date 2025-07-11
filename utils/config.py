import os
from dotenv import load_dotenv
import openai

# 1. 로컬에서 .env 로드
if os.getenv("RENDER") is None:
    dotenv_path = os.path.abspath(".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

# 2. 환경변수 불러오기
GOOGLE_SHEET_TITLE = os.getenv("GOOGLE_SHEET_TITLE", "MySheet")
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY", "")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ✅ 여기! 실제 로딩된 시트 이름 확인
print(f"[✅ config.py] 현재 시트 이름: {GOOGLE_SHEET_TITLE}")

# 3. 필수 검사
missing = []
if not GOOGLE_SHEET_KEY:
    missing.append("GOOGLE_SHEET_KEY")
if not OPENAI_API_KEY:
    missing.append("OPENAI_API_KEY")

if missing:
    raise EnvironmentError(f"필수 환경변수가 누락되었습니다: {', '.join(missing)}")

# 4. OpenAI 설정
openai.api_key = OPENAI_API_KEY

# 5. 외부에 export
__all__ = [
    "GOOGLE_SHEET_TITLE",
    "GOOGLE_SHEET_KEY",
    "GOOGLE_CREDENTIALS_PATH",
    "GOOGLE_SERVICE_ACCOUNT_JSON",
    "OPENAI_API_KEY"
]
