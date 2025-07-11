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
        print("[DEBUG] 요청문:", text)

        # "요약정보" 키워드 포함 여부 판단
        summary_mode = "요약정보" in text
        print("[DEBUG] 요약모드:", summary_mode)

        name = text.replace("요약정보", "").strip().replace(" ", "")
        print("[DEBUG] 추출된 이름:", name)

        if not name:
            return jsonify({"error": "회원명을 입력해 주세요."}), 400

        sheet = get_worksheet("DB")
        db = sheet.get_all_values()
        headers, rows = db[0], db[1:]

        for row in rows:
            row_dict = dict(zip(headers, row))
            if row_dict.get("회원명", "").replace(" ", "") == name:

                if summary_mode:
                    fields = [
                        "회원명", "휴대폰번호", "회원번호",
                        "비밀번호", "계보도", "근무처",
                        "메모", "주소", "코드"
                    ]
                    summary = {key: row_dict.get(key, "") for key in fields}
                    return jsonify({"요약정보": summary}), 200
                else:
                    return jsonify(row_dict), 200

        return jsonify({"error": f"{name} 회원을 찾을 수 없습니다."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500




