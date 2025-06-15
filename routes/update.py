from fastapi import APIRouter, Request
from utils.sheets import get_worksheet
from utils.field_maps import field_map
import re

router = APIRouter()

def parse_request_and_update(text: str, member: dict) -> dict:
    for keyword in field_map:
        pattern = rf"{keyword}\s*[:：]?\s*([^\s]+)"
        for match in re.finditer(pattern, text):
            value = match.group(1)
            field = field_map[keyword]
            member[field] = value
    return member

@router.post("/update_member")
async def update_member(request: Request):
    data = await request.json()
    text = data.get("요청문", "")
    if not text:
        return {"error": "요청문이 비어 있습니다."}

    sheet = get_worksheet("DB")
    db = sheet.get_all_records()
    headers = sheet.row_values(1)

    name = None
    for row in db:
        if row.get("회원명") and row["회원명"] in text:
            name = row["회원명"]
            break

    if not name:
        return {"error": "회원명을 찾을 수 없습니다."}

    for i, row in enumerate(db):
        if row.get("회원명") == name:
            updated = parse_request_and_update(text, row)
            for k, v in updated.items():
                if k in headers:
                    sheet.update_cell(i + 2, headers.index(k) + 1, v)
            return {"message": f"{name} 회원 수정 완료"}
    return {"error": f"{name} 회원을 찾을 수 없습니다."}