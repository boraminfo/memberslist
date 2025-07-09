import re
from flask import Blueprint, request, jsonify
from utils.parser.parse_request_and_update import parse_request_and_update
from utils.sheets import get_member_sheet, safe_update_cell



update_member_bp = Blueprint("update_member", __name__)  # ✅ 이름이 정확히 member_bp 여야 함

@update_member_bp.route("/update_member", methods=["POST"])
def update_member():
    try:
        data = request.get_json(force=True)
        요청문 = data.get("요청문", "").strip()
        if not 요청문:
            return jsonify({"error": "요청문이 비어 있습니다."}), 400

        sheet = get_member_sheet()
        db = sheet.get_all_records()
        headers = [h.strip().lower() for h in sheet.row_values(1)]

        # 계보도 대상자 제외하고 회원명 추출
        lineage_match = re.search(r"계보도[를은는]?\s*([가-힣]{2,})(?:\s*(좌측|우측|라인|왼쪽|오른쪽))?", 요청문)

        계보도_대상 = lineage_match.group(1) if lineage_match else None

        member_names = [str(row.get("회원명", "")).strip() for row in db if row.get("회원명")]
        name = next((n for n in sorted(member_names, key=len, reverse=True) 
                     if n != 계보도_대상 and n in 요청문), None)

        if not name:
            return jsonify({"error": "유효한 회원명을 찾을 수 없습니다."}), 400

        matching_rows = [i for i, row in enumerate(db) if row.get("회원명") == name]
        if not matching_rows:
            return jsonify({"error": f"'{name}' 회원을 찾을 수 없습니다."}), 404

        row_index = matching_rows[0] + 2
        member = db[matching_rows[0]]

        updated_member, 수정된필드 = parse_request_and_update(요청문, member)

        수정결과 = []
        for key, value in updated_member.items():
            if key.endswith("_기록"):
                continue
            if key.strip().lower() in headers:
                col = headers.index(key.strip().lower()) + 1
                success = safe_update_cell(sheet, row_index, col, value)
                if success:
                    수정결과.append({"필드": key, "값": value})

        return jsonify({"status": "success", "회원명": name, "수정": 수정결과}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

