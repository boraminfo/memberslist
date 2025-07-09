from flask import Blueprint, request, jsonify
from utils.sheets import get_worksheet

delete_member_bp = Blueprint("delete_member", __name__)

@delete_member_bp.route('/delete_member', methods=['POST'])
def delete_member():
    try:
        name = request.get_json().get("회원명", "").strip()
        if not name:
            return jsonify({"error": "회원명을 입력해야 합니다."}), 400

        sheet = get_worksheet("DB")
        data = sheet.get_all_records()

        for i, row in enumerate(data):
            if row.get('회원명') == name:
                # 백업 시트에 복사
                backup_sheet = get_worksheet("백업")
                values = [[row.get(k, '') for k in row.keys()]]
                backup_sheet.append_row(values[0])

                # 원래 시트에서 삭제
                sheet.delete_rows(i + 2)  # 헤더 포함 1행 보정
                return jsonify({"message": f"'{name}' 회원 삭제 및 백업 완료"}), 200

        return jsonify({"error": f"'{name}' 회원을 찾을 수 없습니다."}), 404

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

