from flask import Blueprint, request, jsonify
from utils.sheets import get_worksheet
import re

delete_order_conf_bp = Blueprint("delete_order_conf_bp", __name__)








@delete_order_conf_bp.route("/delete_order_confirm", methods=["POST"])
def delete_order_confirm():
    try:
        data = request.get_json()
        번호들 = data.get("삭제번호", "").strip()

        if 번호들 in ["없음", "취소", ""]:
            return jsonify({"message": "삭제 요청이 취소되었습니다."}), 200

        번호_리스트 = sorted(set(map(int, re.findall(r'\d+', 번호들))))

        sheet = get_worksheet("제품주문")
        all_values = sheet.get_all_values()

        if not all_values or len(all_values) < 2:
            return jsonify({"error": "삭제할 주문 데이터가 없습니다."}), 400

        headers, rows = all_values[0], all_values[1:]
        row_count = min(5, len(rows))
        recent_rows = [(i + 2) for i in range(row_count)]  # 실제 행 번호

        # 유효한 번호인지 확인
        if not 번호_리스트 or any(n < 1 or n > row_count for n in 번호_리스트):
            return jsonify({"error": f"삭제할 주문 번호는 1 ~ {row_count} 사이로 입력해 주세요."}), 400

        삭제행목록 = [recent_rows[n - 1] for n in 번호_리스트]
        삭제행목록.sort(reverse=True)

        for row_num in 삭제행목록:
            sheet.delete_rows(row_num)

        return jsonify({
            "message": f"{', '.join(map(str, 번호_리스트))}번 주문이 삭제되었습니다.",
            "삭제행번호": 삭제행목록
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
