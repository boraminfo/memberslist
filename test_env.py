import os
from dotenv import load_dotenv
import json

# 환경 변수 명확히 로드
dotenv_path = os.path.abspath(".env")
if not os.path.exists(dotenv_path):
    raise FileNotFoundError(".env 파일을 찾을 수 없습니다.")

load_dotenv(dotenv_path)

print("✅ GOOGLE_SHEET_TITLE:", os.getenv("GOOGLE_SHEET_TITLE"))
print("✅ GOOGLE_SHEET_KEY 존재 여부:", "Yes" if os.getenv("GOOGLE_SHEET_KEY") else "No")

# JSON 테스트
try:
    key_data = json.loads(os.getenv("GOOGLE_SHEET_KEY"))
    print("✅ GOOGLE_SHEET_KEY 파싱 성공, project_id:", key_data.get("project_id"))
except Exception as e:
    print("❌ GOOGLE_SHEET_KEY 파싱 실패:", str(e))



import os

path = os.path.abspath('.env')
print("✅ .env 경로:", path)
print("✅ 파일 존재 여부:", os.path.exists(path))
