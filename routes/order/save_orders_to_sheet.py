from utils.sheets import get_worksheet
from flask import jsonify
from datetime import datetime
import pytz

def save_orders_to_sheet(회원명, orders):
    sheet = get_worksheet("제품주문")
    db_sheet = get_worksheet("DB")

    member_records = db_sheet.get_all_records()

    # 회원 정보 찾기
    회원번호 = ""
    회원_휴대폰번호 = ""
    clean_회원명 = 회원명.replace("제품주문", "").replace("저장", "").strip()

    for record in member_records:
        if record.get("회원명") == clean_회원명:
            회원번호 = record.get("회원번호", "")
            회원_휴대폰번호 = record.get("휴대폰번호", "")
            break

    def now_kst():
        return datetime.now(pytz.timezone("Asia/Seoul"))

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
        sheet.insert_row(row, 2, value_input_option="USER_ENTERED")

    return jsonify({"status": "success", "message": f"{clean_회원명}의 주문이 저장되었습니다."})
