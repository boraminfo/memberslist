from flask import Blueprint, request, jsonify
from utils.parser.parse_order_text import parse_order_text
from utils.config import GOOGLE_SHEET_TITLE, GOOGLE_CREDENTIALS_PATH
import gspread
from oauth2client.service_account import ServiceAccountCredentials


parse_order_bp = Blueprint("parse_order", __name__)  # 블루프린트 이름 반드시 일치



def save_order_to_sheet(parsed):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    ss = client.open(GOOGLE_SHEET_TITLE)
    db_sheet = ss.worksheet("DB")
    order_sheet = ss.worksheet("제품주문")

    # 회원정보 조회
    name = parsed.get("회원명", "")
    member_number = ""
    member_phone = ""
    members = db_sheet.get_all_records()
    for m in members:
        if m.get("회원명") == name:
            member_number = m.get("회원번호", "")
            member_phone = m.get("휴대폰번호", "")
            break

    # 주문 행 삽입 (수량만큼 반복)
    for _ in range(parsed.get("수량", 1)):
        row = [
            parsed.get("주문일자", ""),
            name,
            member_number,
            member_phone,
            parsed.get("제품명", ""),
            "0",  # 제품가격
            "0",  # PV
            parsed.get("결재방법", ""),
            name,  # 주문자_고객명
            member_phone,
            parsed.get("배송처", ""),
            "0"  # 수령확인
        ]
        order_sheet.insert_row(row, 2, value_input_option="USER_ENTERED")










# ✅ API 라우트
@parse_order_bp.route("/parse_and_save_order", methods=["POST"])
def parse_and_save_order():
    try:
        user_input = request.json.get("text", "")
        parsed = parse_order_text(user_input)
        save_order_to_sheet(parsed)
        return jsonify({
            "status": "success",
            "message": f"{parsed.get('회원명', '회원')}님의 주문이 저장되었습니다.",
            "parsed": parsed
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500







def save_order_from_text(text: str):
    try:
        parsed = parse_order_text(text)
        save_order_to_sheet(parsed)
        return jsonify({
            "status": "success",
            "message": f"{parsed.get('회원명', '회원')}님의 주문이 저장되었습니다.",
            "parsed": parsed
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
