from fastapi import APIRouter, Request
from utils.sheets import get_worksheet, now_kst

router = APIRouter()

@router.post("/add_activity")
async def add_activity(request: Request):
    data = await request.json()
    name = data.get("회원명", "")
    content = data.get("내용", "")

    sheet = get_worksheet("활동일지")
    sheet.insert_row([now_kst().strftime('%Y-%m-%d %H:%M'), name, content], index=2)
    return {"message": f"{name}님의 활동일지 저장 완료"}