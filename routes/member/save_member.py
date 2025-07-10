from flask import Blueprint, request, jsonify
from utils.sheets import get_member_sheet
from utils.parser.parse_registration import parse_registration

save_member_bp = Blueprint("save_member", __name__)




@save_member_bp.route("/save_member", methods=["POST"])
def save_member():
    try:
        req = request.get_json()
        요청문 = req.get("요청문") or req.get("회원명", "")

        if not 요청문:
            return jsonify({"error": "입력 문장이 없습니다"}), 400

        return save_member_from_text(요청문)  # ✅ 공통 함수로 위임

    except Exception as e:
        return jsonify({"error": str(e)}), 500







# ✅ intent_router에서 직접 호출되는 함수
def save_member_from_text(text: str):
    try:
        name, number, phone, lineage = parse_registration(text)
        if not name:
            return jsonify({"error": "회원명을 추출할 수 없습니다"}), 400

        sheet = get_member_sheet()
        headers = [h.strip() for h in sheet.row_values(1)]
        rows = sheet.get_all_records()

        for i, row in enumerate(rows):
            if str(row.get("회원명", "")).strip() == name:
                for key, value in {
                    "회원명": name,
                    "회원번호": number,
                    "휴대폰번호": phone,
                    "계보도": lineage
                }.items():
                    if key in headers and value:
                        sheet.update_cell(i + 2, headers.index(key) + 1, value)
                return jsonify({"message": f"{name} 기존 회원 정보 수정 완료"}), 200

        new_row = [''] * len(headers)
        for key, value in {
            "회원명": name,
            "회원번호": number,
            "휴대폰번호": phone,
            "계보도": lineage
        }.items():
            if key in headers and value:
                new_row[headers.index(key)] = value

        sheet.insert_row(new_row, 2)
        return jsonify({"message": f"{name} 회원 신규 등록 완료"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



