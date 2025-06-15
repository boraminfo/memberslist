from fastapi import APIRouter, Request
from utils.sheets import get_worksheet

router = APIRouter()

@router.post("/find_member")
async def find_member(request: Request):
    data = await request.json()
    name = data.get("회원명", "").strip()
    number = data.get("회원번호", "").strip()

    if not name and not number:
        return {"error": "회원명 또는 회원번호를 입력해야 합니다."}

    sheet = get_worksheet("DB")
    if not sheet:
        return {"error": "DB 시트를 찾을 수 없습니다."}

    db = sheet.get_all_records()
    for row in db:
        if row.get("회원명") == name or row.get("회원번호") == number:
            return row

    return {"error": "해당 회원 정보를 찾을 수 없습니다."}
    





    