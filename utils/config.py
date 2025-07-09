import os
from dotenv import load_dotenv
import openai

# ✅ 1. 로컬 환경에서만 .env 로드
if os.getenv("RENDER") is None:
    dotenv_path = os.path.abspath(".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print("⚠️ .env 파일이 없습니다. 기본값을 사용하거나 환경변수를 직접 설정하세요.")

# ✅ 2. 환경변수 로딩 (기본값 설정 포함)
GOOGLE_SHEET_TITLE = os.getenv("GOOGLE_SHEET_TITLE", "MySheet")  # 기본 시트 이름
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY", "")             # 필수: Sheet key
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")  # 기본 credentials 경로
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ✅ 3. 필수 환경변수 검사
missing = []
if not GOOGLE_SHEET_KEY:
    missing.append("GOOGLE_SHEET_KEY")
if not OPENAI_API_KEY:
    missing.append("OPENAI_API_KEY")

if missing:
    raise EnvironmentError(f"필수 환경변수가 누락되었습니다: {', '.join(missing)}")

# ✅ 4. OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY

# ✅ 5. 공통 범용 변수로 정리해서 외부에서 import 하도록 제공
__all__ = [
    "GOOGLE_SHEET_TITLE",
    "GOOGLE_SHEET_KEY",
    "GOOGLE_CREDENTIALS_PATH",
    "OPENAI_API_KEY"
]

