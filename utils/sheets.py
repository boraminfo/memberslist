import os
import time
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
import pytz


# 🔄 .env 파일 로드 (필요한 경우)
load_dotenv()

# 🔐 인증 클라이언트 생성
import json

def get_gspread_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)


# 📄 공통 시트 접근
def get_worksheet(sheet_name):
    client = get_gspread_client()
    sheet = client.open(os.getenv("GOOGLE_SHEET_TITLE"))
    return sheet.worksheet(sheet_name)

# ✅ 각 시트별 함수
def get_order_sheet():
    return get_worksheet("제품주문")

def get_member_sheet():
    return get_worksheet("DB")

def get_backup_sheet():
    return get_worksheet("백업")

def get_counseling_sheet():
    return get_worksheet("상담일지")

def get_mymemo_sheet():
    return get_worksheet("개인메모")

def get_dailyrecord_sheet():
    return get_worksheet("활동일지")

def get_image_sheet():
    return get_worksheet("사진저장")

# ✅ 회원 정보 조회
def get_member_info(member_name):
    sheet = get_member_sheet()
    records = sheet.get_all_records()
    for row in records:
        if row.get("회원명") == member_name:
            return row.get("회원번호", ""), row.get("휴대폰번호", "")
    return "", ""

# ✅ 안전한 셀 업데이트 (재시도 포함)
def safe_update_cell(sheet, row, col, value, max_retries=3, delay=2):
    for attempt in range(1, max_retries + 1):
        try:
            sheet.update_cell(row, col, value)
            return True
        except gspread.exceptions.APIError as e:
            if "429" in str(e):
                print(f"[⏳ 재시도 {attempt}] 429 오류 → {delay}초 대기")
                time.sleep(delay)
                delay *= 2
            else:
                raise
    print("[❌ 실패] 최대 재시도 초과")
    return False







def save_to_sheet(sheet_name, member_name, content):
    try:
        sheet = get_worksheet(sheet_name)
        if sheet is None:
            print(f"[오류] '{sheet_name}' 시트를 찾을 수 없습니다.")
            return False

        existing = sheet.get_all_values()
        contents = [row[2] if len(row) > 2 else "" for row in existing]  # 3열 기준 중복 체크
        if content in contents:
            print(f"[중복] 이미 같은 내용이 '{sheet_name}'에 존재합니다.")
            return False

        now = datetime.now(pytz.timezone("Asia/Seoul"))
        time_str = now.strftime("%Y-%m-%d %H:%M")

        sheet.insert_row([time_str, member_name, content], index=2)
        print(f"[저장완료] '{sheet_name}' 시트에 저장 완료")
        return True

    except Exception as e:
        print(f"[시트 저장 오류: {sheet_name}] {e}")
        return False
