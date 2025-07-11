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

    creds_env = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    
    # 🔍 어떤 형식인지 로그로 확인
    print(f"[🔍 인증 파일/내용 확인] 시작 - 앞 50자: {creds_env[:50] if creds_env else 'None'}")

    if creds_env and creds_env.strip().startswith("{"):
        # ✅ 환경변수에 JSON 문자열이 직접 들어있는 경우
        creds_dict = json.loads(creds_env)
    else:
        # ✅ 환경변수에 파일 경로만 들어있는 경우 (예: credentials.json)
        creds_path = creds_env or "credentials.json"
        print(f"[🔍 인증 파일 경로 사용] creds_path = {creds_path}")
        with open(creds_path, "r", encoding="utf-8") as f:
            creds_dict = json.load(f)

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
    print(f"[safe_update_cell] 호출됨: row={row}, col={col}, value={value}")
    for attempt in range(1, max_retries + 1):
        try:
            sheet.update_cell(row, col, value)
            print(f"[✅ 성공] 셀 업데이트 완료 (row={row}, col={col})")
            return True
        except gspread.exceptions.APIError as e:
            if "429" in str(e):
                print(f"[⏳ 재시도 {attempt}] 429 오류 → {delay}초 대기")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"[❌ API 오류] {e}")
                break
        except Exception as e:
            print(f"[❌ 예외 발생] {e}")
            break
    print("[❌ 실패] 최대 재시도 초과 또는 예외 발생")
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






# ✅ 회원 정보 수정
def update_member_in_sheet(name, updates: dict):
    sheet = get_member_sheet()
    all_data = sheet.get_all_values()
    headers = all_data[0]
    rows = all_data[1:]

    for idx, row in enumerate(rows):
        row_dict = dict(zip(headers, row))
        if row_dict.get("회원명") == name:
            row_index = idx + 2  # 실제 시트에서의 행 번호
            수정결과 = []
            for key, value in updates.items():
                if key in headers:
                    col = headers.index(key) + 1  # 열 번호
                    from utils.sheets import safe_update_cell
                    if safe_update_cell(sheet, row_index, col, value):
                        수정결과.append({"필드": key, "값": value})
            return {
                "message": f"{name} 회원 정보가 수정되었습니다.",
                "수정내용": 수정결과
            }

    return {"error": f"{name} 회원을 찾을 수 없습니다."}










from datetime import datetime
import pytz

def save_orders_to_sheet(회원명, orders):
    """
    주문 정보를 '제품주문' 시트에 저장합니다.
    회원명(str)과 주문 리스트(list[dict])를 입력받습니다.
    """
    sheet = get_worksheet("제품주문")
    db_sheet = get_worksheet("DB")

    member_records = db_sheet.get_all_records()

    # 자연어에서 불필요한 키워드 제거
    clean_회원명 = 회원명.replace("제품주문", "").replace("저장", "").strip()

    # 회원 정보 조회
    회원번호 = ""
    회원_휴대폰번호 = ""
    for record in member_records:
        if record.get("회원명") == clean_회원명:
            회원번호 = record.get("회원번호", "")
            회원_휴대폰번호 = record.get("휴대폰번호", "")
            break

    def now_kst():
        return datetime.now(pytz.timezone("Asia/Seoul"))

    # 주문 정보 삽입
    row_index = 2  # 항상 위로 삽입
    for order in orders:
        row = [
            order.get("주문일자", now_kst().strftime("%Y-%m-%d")),
            clean_회원명,
            회원번호,
            회원_휴대폰번호,
            order.get("제품명", ""),
            float(order.get("제품가격", 0)),
            float(order.get("PV", 0)),
            order.get("결재방법", ""),
            order.get("주문자_고객명", ""),
            order.get("주문자_휴대폰번호", ""),
            order.get("배송처", ""),
            order.get("수령확인", "")
        ]
        sheet.insert_row(row, row_index)
        row_index += 1

    return True


