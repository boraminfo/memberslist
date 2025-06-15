from fastapi import APIRouter, Request
from utils.sheets import get_worksheet, now_kst
import re

router = APIRouter()

@router.post("/add_counseling")
async def add_counseling(request: Request):
    data = await request.json()
    text = data.get("요청문", "").strip()

    match = re.search(r"([가-힣]{2,3})\s*(상담일지)", text)
    if not match:
        return {"error": "회원명 또는 상담일지 키워드를 찾을 수 없습니다."}

    name = match.group(1)
    sheet = get_worksheet("상담일지")
    if not sheet:
        return {"error": "상담일지 시트를 찾을 수 없습니다."}

    text = re.sub(rf"{name}\s*상담일지", "", text).strip()
    sheet.insert_row([now_kst().strftime('%Y-%m-%d %H:%M'), name, text], index=2)
    return {"message": f"{name}님의 상담일지 저장 완료"}