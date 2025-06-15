from fastapi import APIRouter, Request
from utils.sheets import get_worksheet

router = APIRouter()

@router.post("/delete_member")
async def delete_member(request: Request):
    data = await request.json()
    name = data.get("회원명", "").strip()
    print(f"[삭제 요청 수신] 회원명: {name}")

    if not name:
        return {"error": "회원명을 입력해야 삭제할 수 있습니다."}

    sheet = get_worksheet("DB")
    if not sheet:
        return {"error": "DB 시트를 찾을 수 없습니다."}

    header_row = sheet.row_values(1)
    print(f"[시트 헤더] {header_row}")

    try:
        name_col_index = header_row.index("회원명") + 1  # 1-based index
    except ValueError:
        return {"error": "'회원명' 열을 찾을 수 없습니다."}

    name_column = sheet.col_values(name_col_index)[1:]  # exclude header
  

    for i, cell_value in enumerate(name_column):
        if cell_value.strip() == name:
            row_to_delete = i + 2  # +2: 0-based → 실제 시트 행 번호
            sheet.delete_rows(row_to_delete)
            print(f"[삭제 완료] {name} (행 {row_to_delete})")
            return {"message": f"{name} 회원 삭제 완료"}

    return {"error": f"{name} 회원을 찾을 수 없습니다."}
