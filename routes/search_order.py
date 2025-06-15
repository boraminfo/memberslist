from fastapi import APIRouter, Request
from utils.sheets import get_worksheet
from datetime import datetime

router = APIRouter()

@router.post("/search_memo_by_tags")
async def search_memo_by_tags(request: Request):
    data = await request.json()
    tags = data.get("tags", [])
    if not tags:
        return {"error": "태그가 없습니다."}

    sheet = get_worksheet("개인메모")
    rows = sheet.get_all_values()[1:]
    results = []

    for row in rows:
        if len(row) < 3:
            continue
        name, date_str, content = row[0], row[1], row[2]
        match_count = sum(1 for tag in tags if tag in content)
        if match_count > 0:
            results.append({
                "회원명": name,
                "날짜": date_str,
                "내용": content,
                "일치_태그수": match_count
            })

    results.sort(key=lambda x: (-x["일치_태그수"], x["날짜"]))
    return {"검색결과": results[:10]}