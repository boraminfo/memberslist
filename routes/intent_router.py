from flask import Blueprint, request, jsonify
from utils.intent_utils import detect_intent

# 기능별 처리 함수 불러오기
from routes.member.save_member import save_member_from_text
from routes.member.update_member import update_member_from_text
from routes.member.delete_member import delete_member_from_text
from routes.member.find_member import find_member_from_text

router = Blueprint("intent_router", __name__)

@router.route("/handle_member_intent", methods=["POST"])
def handle_member_intent():
    data = request.get_json()
    text = data.get("요청문", "").strip()

    intent = detect_intent(text)

    if intent == "등록":
        return save_member_from_text(text)
    elif intent == "수정":
        return update_member_from_text(text)
    elif intent == "삭제":
        return delete_member_from_text(text)
    elif intent == "조회":
        return find_member_from_text(text)
    else:
        return jsonify({
            "message": "의도를 파악할 수 없습니다.",
            "요청문": text
        }), 400


