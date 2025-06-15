from fastapi import APIRouter, Request
from utils.sheets import get_worksheet

router = APIRouter()

@router.post("/delete_member")
async def delete_member(request: Request):
    data = await request.json()
    name = data.get("회원명", "").strip()
    if not name:
        return {"error": "회원명을 입력해야 합니다."}

    sheet = get_worksheet("DB")
    db = sheet.get_all_records()

    for i, row in enumerate(db):
        if row.get("회원명") == name:
            sheet.delete_rows(i + 2)
            return {"message": f"{name} 회원 삭제 완료"}
    return {"error": f"{name} 회원을 찾을 수 없습니다."}