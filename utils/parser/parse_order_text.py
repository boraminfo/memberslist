import re
from datetime import datetime, timedelta

def parse_date(text: str) -> str:
    today = datetime.today()
    if "오늘" in text:
        return today.strftime("%Y-%m-%d")
    elif "어제" in text:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "내일" in text:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        match = re.search(r"(20\d{2}[./-]\d{1,2}[./-]\d{1,2})", text)
        if match:
            return re.sub(r"[./]", "-", match.group(1))
    return today.strftime("%Y-%m-%d")












def parse_order_text(text: str) -> dict:
    """
    자연어 문장에서 회원명, 제품명, 수량, 결제방식, 주소, 주문일자 등을 추출합니다.
    """
    result = {}

    # 1. 회원명 (맨 앞 단어)
    match = re.match(r"(\S+?)(?:님)?[\s]", text)
    result["회원명"] = match.group(1) if match else ""

    # 2. 제품명 + 수량 (예: 노니 2개)
    prod_match = re.search(r"([\w가-힣]+)[\s]*(\d+)\s*개", text)
    if prod_match:
        result["제품명"] = prod_match.group(1)
        result["수량"] = int(prod_match.group(2))
    else:
        result["제품명"] = "제품"
        result["수량"] = 1

    # 3. 결제방법
    if "카드" in text:
        result["결재방법"] = "카드"
    elif "현금" in text:
        result["결재방법"] = "현금"
    elif "계좌" in text:
        result["결재방법"] = "계좌이체"
    else:
        result["결재방법"] = "카드"

    # 4. 배송처
    address_match = re.search(r"(?:주소|배송지)[:：]?\s*(.+)", text)
    if address_match:
        result["배송처"] = address_match.group(1).strip()
    else:
        result["배송처"] = ""

    # 5. 주문일자
    result["주문일자"] = parse_date(text)

    return result

import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from utils.config import GOOGLE_SHEET_TITLE, GOOGLE_CREDENTIALS_PATH












def save_order_to_sheet(parsed):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    ss = client.open(GOOGLE_SHEET_TITLE)
    db_sheet = ss.worksheet("DB")
    order_sheet = ss.worksheet("제품주문")

    name = parsed.get("회원명", "")
    member_number, member_phone = "", ""

    members = db_sheet.get_all_records()
    for m in members:
        if m.get("회원명") == name:
            member_number = m.get("회원번호", "")
            member_phone = m.get("휴대폰번호", "")
            break

    for _ in range(parsed.get("수량", 1)):
        row = [
            parsed.get("주문일자"),
            name,
            member_number,
            member_phone,
            parsed.get("제품명"),
            "0",  # 제품가격
            "0",  # PV
            parsed.get("결재방법"),
            name,
            member_phone,
            parsed.get("배송처"),
            "0"
        ]
        order_sheet.insert_row(row, 2, value_input_option="USER_ENTERED")
