from fastapi import APIRouter, Request
from utils.sheets import get_worksheet
from utils.parser import parse_text_to_fields  # ✅ 자연어 파서 임포트

router = APIRouter()

@router.post("/update_member")
async def update_member(request: Request):
    data = await request.json()

    # ✅ 자연어 요청문 처리
    if "요청문" in data:
        text = data["요청문"]
        name, update_fields = parse_text_to_fields(text)
    else:
        name = data.get("회원명", "").strip()
        update_fields = {k: v for k, v in data.items() if k != "회원명"}

    print(f"[수정 요청 수신] 회원명: {name}")
    print(f"[업데이트 요청 필드] {update_fields}")

    if not name:
        return {"error": "회원명은 필수입니다."}

    # ✅ 시트 가져오기
    sheet = get_worksheet("DB")
    if not sheet:
        return {"error": "DB 시트를 찾을 수 없습니다."}

    headers = sheet.row_values(1)
    print(f"[시트 헤더] {headers}")

    try:
        name_col_index = headers.index("회원명") + 1  # 1-based
    except ValueError:
        return {"error": "'회원명' 열을 찾을 수 없습니다."}

    name_column = sheet.col_values(name_col_index)[1:]  # exclude header
    print(f"[회원명 목록] {name_column}")

    for i, cell_value in enumerate(name_column):
        if cell_value.strip() == name:
            row_to_update = i + 2  # 실제 행 번호
            print(f"[수정 대상 행 번호] {row_to_update}")

            updated_fields = []

            for field, value in update_fields.items():
                if field in headers and field != "회원명":
                    col_index = headers.index(field) + 1
                    print(f"[필드 업데이트] {field} → {value} (열 {col_index})")
                    sheet.update_cell(row_to_update, col_index, value)
                    updated_fields.append(field)

            if updated_fields:
                return {
                    "message": f"{name} 회원 정보 수정 완료",
                    "수정필드": updated_fields
                }
            else:
                return {"message": f"{name} 회원 정보 중 수정할 필드가 없습니다."}

    return {"error": f"{name} 회원을 찾을 수 없습니다."}
