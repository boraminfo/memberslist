from flask import Blueprint, request, jsonify
from utils.intent_utils import detect_intent

# 기능별 처리 함수 불러오기
from routes.member.save_member import save_member_from_text
from routes.member.update_member import update_member_from_text
from routes.member.delete_member import delete_member_from_text
from routes.member.find_member import find_member_from_text

from routes.order.parse_and_save_order import save_order_from_text
from routes.order.save_orders_to_sheet import save_orders_to_sheet  # ✅ 이 줄 추가


router = Blueprint("intent_router", __name__)



@router.route("/handle_member_intent", methods=["POST"])
def handle_member_intent():
    try:
        if not request.is_json:
            print("[요청 오류] JSON이 아닙니다.")
            return jsonify({"error": "요청이 JSON 형식이 아닙니다."}), 400

        try:
            data = request.get_json(force=True)
        except Exception as e:
            print("[JSON 파싱 오류]", e)
            return jsonify({"error": "유효하지 않은 JSON 형식입니다.", "details": str(e)}), 400

        print("[요청 데이터]", data)

        # 요청문 우선, 없으면 회원명을 텍스트로 대체
        text = data.get("요청문", "").strip()
        if not text:
            text = data.get("회원명", "").strip()

        if not text:
            return jsonify({"error": "요청문이 비어 있습니다."}), 400

        print("[요청문]", text)

        intent = detect_intent(text)
        print("[분석된 intent]", intent)

        if intent == "등록":
            return save_member_from_text(text)
        elif intent == "수정":
            return update_member_from_text(text)
        elif intent == "삭제":
            return delete_member_from_text(text)
        elif intent == "조회":
            return find_member_from_text(text)



        elif intent == "주문":
            if "orders" in data:
                clean_회원명 = data.get("회원명", "").replace("제품주문", "").replace("저장", "").strip()
                return save_orders_to_sheet(clean_회원명, data["orders"])
            else:
                return save_order_from_text(text)




        else:
            return jsonify({
                "message": "의도를 파악할 수 없습니다.",
                "요청문": text
            }), 400

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
