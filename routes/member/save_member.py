from flask import Blueprint, request, jsonify
from utils.sheets import get_member_sheet
from utils.parser.parse_registration import parse_registration

save_member_bp = Blueprint("save_member", __name__)




@save_member_bp.route("/save_member", methods=["POST"])
def save_member():
    try:
        req = request.get_json()
        요청문 = req.get("요청문")
        회원명 = req.get("회원명")

        if not 요청문 and not 회원명:
            return jsonify({"error": "요청문 또는 회원명이 필요합니다."}), 400

        # 요청문이 없으면 생성
        if not 요청문 and 회원명:
            요청문 = f"{회원명} 회원등록"

        # ✅ 회원명 명시되어 있으면 넘겨줌 (정규식 무시)
        return save_member_from_text(요청문, override_name=회원명)

    except Exception as e:
        return jsonify({"error": str(e)}), 500









# ✅ intent_router에서 직접 호출되는 함수
import re
from flask import jsonify


def extract_member_name(text: str):
    print(f"[extract_member_name 진입] 원본: {text}")
    for keyword in ["회원등록", "신규등록"]:
        text = text.replace(keyword, "")
    name = text.strip()
    print(f"[정제 후 name] = {name}")
    if re.fullmatch(r"[가-힣]{2,5}", name):
        return name
    return None

















def save_member_from_text(text: str, override_name: str = None):
    try:
        print(f"[요청문] text = {text}")
        print(f"[override_name] = {override_name}")

        if not re.search(r"(회원등록|신규등록)", text):
            return jsonify({"error": "'회원등록' 또는 '신규등록' 문구가 포함된 요청만 처리합니다."}), 400

        name = override_name or extract_member_name(text)
        print(f"[추출된 회원명] name = {name}")

        name_from_parser, number, phone, lineage = parse_registration(text)
        print(f"[parse_registration 결과] name_from_parser = {name_from_parser}, number = {number}, phone = {phone}, lineage = {lineage}")

        if not name or name in ["회원등록", "신규등록"]:
            return jsonify({"error": "회원명을 추출할 수 없습니다."}), 400


        # ✅ 시트 처리
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






