from fastapi import APIRouter, Request
from utils.sheets import get_worksheet

router = APIRouter()

@router.post("/update_member")
async def update_member(request: Request):
    data = await request.json()
    name = data.get("회원명", "").strip()
    print(f"[수정 요청 수신] 회원명: {name}")

    if not name:
        return {"error": "회원명은 필수입니다."}

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
            updated_fields = []

            for field, value in data.items():
                if field in headers and field != "회원명":  # 회원명은 수정하지 않음
                    col_index = headers.index(field) + 1
                    sheet.update_cell(row_to_update, col_index, value)
                    updated_fields.append(field)

            if updated_fields:
                return {"message": f"{name} 회원 정보 수정 완료", "수정필드": updated_fields}
            else:
                return {"message": f"{name} 회원 정보 중 수정할 필드가 없습니다."}

    return {"error": f"{name} 회원을 찾을 수 없습니다."}
