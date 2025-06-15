from fastapi import APIRouter, Request
from utils.sheets import get_worksheet
import uuid

router = APIRouter()

@router.post("/register")
async def register_member(request: Request):
    data = await request.json()
    name = data.get("회원명", "").strip()
    number = data.get("회원번호", "").strip()

    if not name:
        return {"error": "회원명은 필수입니다."}

    if not number:
        number = str(uuid.uuid4())[:8]

    sheet = get_worksheet("DB")
    if not sheet:
        return {"error": "DB 시트를 불러올 수 없습니다."}

    headers = sheet.row_values(1)
    data_rows = sheet.get_all_records()
    for i, row in enumerate(data_rows):
        if row.get("회원명") == name:
            for key, value in {"회원명": name, "회원번호": number}.items():
                if key in headers:
                    sheet.update_cell(i + 2, headers.index(key) + 1, value)
            return {"message": f"{name} 기존 회원 정보 수정 완료"}

    new_row = [''] * len(headers)
    for key, value in {"회원명": name, "회원번호": number}.items():
        if key in headers:
            new_row[headers.index(key)] = value
    sheet.append_row(new_row)
    return {"message": f"{name} 회원 등록 완료"}