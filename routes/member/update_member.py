import re
from flask import Blueprint, request, jsonify
from utils.parser.parse_request_and_update import parse_update_request
from utils.sheets import update_member_in_sheet
from routes.note.add_counseling import add_counseling_from_text

update_member_bp = Blueprint("update_member", __name__)

@update_member_bp.route("/update_member", methods=["POST"])
def update_member():
    try:
        data = request.get_json()
        text = data.get("요청문", "")
        return update_member_from_text(text)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_member_from_text(text: str):
    try:
        # ✅ 회원메모 요청 분기
        if "회원메모" in text and any(kw in text for kw in ["저장", "수정"]):
            return add_counseling_from_text(text)

        name, updates = parse_update_request(text)
        if not name or not updates:
            return jsonify({"error": "회원명 또는 수정 항목이 없습니다."}), 400

        result = update_member_in_sheet(name, updates)
        return jsonify(result), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


