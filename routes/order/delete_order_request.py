from flask import Blueprint, jsonify
from utils.sheets import get_worksheet

delete_order_req_bp = Blueprint("delete_order_req_bp", __name__)



@delete_order_req_bp.route("/delete_order_request", methods=["POST"])
def delete_order_request():
    try:
        sheet = get_worksheet("제품주문")
        all_values = sheet.get_all_values()

        if not all_values or len(all_values) < 2:
            return jsonify({"message": "등록된 주문이 없습니다."}), 404

        headers, rows = all_values[0], all_values[1:]
        row_count = min(5, len(rows))  # 최대 5건

        # 최신 주문 5건 가져오기
        recent_orders = [(i + 2, row) for i, row in enumerate(rows[:row_count])]

        response = []
        for idx, (row_num, row_data) in enumerate(recent_orders, start=1):
            try:
                item = {
                    "번호": idx,
                    "행번호": row_num,
                    "회원명": row_data[headers.index("회원명")],
                    "제품명": row_data[headers.index("제품명")],
                    "가격": row_data[headers.index("제품가격")],
                    "PV": row_data[headers.index("PV")],
                    "주문일자": row_data[headers.index("주문일자")]
                }
                response.append(item)
            except Exception:
                continue  # 누락된 필드가 있으면 건너뜀

        return jsonify({
            "message": f"📌 최근 주문 내역 {len(response)}건입니다. 삭제할 번호(1~{len(response)})를 선택해 주세요.",
            "주문목록": response
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

