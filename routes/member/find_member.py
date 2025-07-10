from flask import Blueprint, request, jsonify
from utils.sheets import get_worksheet

find_member_bp = Blueprint("find_member", __name__)

@find_member_bp.route("/find_member", methods=["POST"])
def find_member():
    try:
        data = request.get_json()
        name = data.get("회원명", "").strip()
        number = data.get("회원번호", "").strip()

        if not name and not number:
            return jsonify({"error": "회원명 또는 회원번호를 입력해야 합니다."}), 400

        sheet = get_worksheet("DB")
        db = sheet.get_all_values()
        headers, rows = db[0], db[1:]

        matched = []
        for row in rows:
            row_dict = dict(zip(headers, row))
            if name and row_dict.get("회원명") == name:
                matched.append(row_dict)
            elif number and row_dict.get("회원번호") == number:
                matched.append(row_dict)

        if not matched:
            return jsonify({"error": "해당 회원 정보를 찾을 수 없습니다."}), 404

        if len(matched) == 1:
            return jsonify(matched[0]), 200

        result = []
        for idx, member in enumerate(matched, start=1):
            result.append({
                "번호": idx,
                "회원명": member.get("회원명"),
                "회원번호": member.get("회원번호"),
                "휴대폰번호": member.get("휴대폰번호")
            })
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500






# ✅ intent_router에서 직접 호출되는 함수
def find_member_from_text(text: str):
    try:
        name = text.strip()
        if not name:
            return jsonify({"error": "회원명을 입력해 주세요."}), 400

        sheet = get_worksheet("DB")  # ← 여기서 get_member_sheet() 대신 통일
        db = sheet.get_all_values()
        headers, rows = db[0], db[1:]

        for row in rows:
            row_dict = dict(zip(headers, row))
            if row_dict.get("회원명") == name:
                return jsonify(row_dict), 200

        return jsonify({"error": f"{name} 회원을 찾을 수 없습니다."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



