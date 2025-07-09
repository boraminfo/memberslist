from flask import Blueprint, request, jsonify
from utils.sheets import get_order_sheet

save_order_json_bp = Blueprint("save_order_json", __name__)  # ✅ 이름 정확히 맞춰야 함

@save_order_json_bp.route("/save_order", methods=["POST"])
def save_order_from_json():
    try:
        data = request.get_json()
        sheet = get_order_sheet()

        if not data or not isinstance(data, list):
            return jsonify({"error": "유효한 JSON 리스트가 필요합니다."}), 400

        for item in data:
            row = [
                item.get("주문일자", ""),
                item.get("회원명", ""),
                item.get("회원번호", ""),
                item.get("휴대폰번호", ""),
                item.get("제품명", ""),
                item.get("제품가격", ""),
                item.get("PV", ""),
                item.get("결재방법", ""),
                item.get("주문자_고객명", ""),
                item.get("주문자_휴대폰번호", ""),
                item.get("배송처", ""),
                item.get("수령확인", "")
            ]
            sheet.insert_row(row, 2, value_input_option="USER_ENTERED")

        return jsonify({"status": "success", "message": "주문이 성공적으로 저장되었습니다."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
