from flask import Blueprint, request, jsonify
from utils.sheets import get_worksheet, safe_update_cell, save_to_sheet
from utils.parser.parse_counseling import parse_counseling_command

add_counseling_bp = Blueprint("add_counseling_bp", __name__)









@add_counseling_bp.route("/add_counseling", methods=["POST"])
def add_counseling():
    try:
        data = request.get_json()
        text = data.get("요청문", "")

        # 파싱
        member_name, sheet_name, content = parse_counseling_command(text)

        # 회원메모는 DB 시트의 메모 필드에 저장
        if sheet_name == "회원메모":
            sheet = get_worksheet("DB")
            db = sheet.get_all_records()
            headers = [h.strip().lower() for h in sheet.row_values(1)]

            matching_rows = [i for i, row in enumerate(db) if row.get("회원명") == member_name]
            if not matching_rows:
                return jsonify({"message": f"'{member_name}' 회원을 찾을 수 없습니다."})

            row_index = matching_rows[0] + 2

            if "메모".lower() in headers:
                col_index = headers.index("메모".lower()) + 1
                success = safe_update_cell(sheet, row_index, col_index, content)
                if success:
                    return jsonify({"message": f"{member_name}님의 메모가 DB 시트에 저장되었습니다."})
                else:
                    return jsonify({"message": f"'{member_name}' 메모 저장 실패."})
            else:
                return jsonify({"message": "DB 시트에 '메모' 필드가 없습니다."})

        # 나머지 시트는 일반 시트로 저장
        if save_to_sheet(sheet_name, member_name, content):
            return jsonify({"message": f"{member_name}님의 {sheet_name} 저장이 완료되었습니다."})
        else:
            return jsonify({"message": f"같은 내용이 이미 '{sheet_name}' 시트에 저장되어 있습니다."})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
