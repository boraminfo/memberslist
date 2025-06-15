from fastapi import APIRouter, Request
from utils.sheets import get_worksheet, now_kst
import re
from datetime import timedelta

router = APIRouter()

def process_order_date(raw_date: str) -> str:
    if not raw_date:
        return now_kst().strftime('%Y-%m-%d')
    raw_date = raw_date.strip()
    if "오늘" in raw_date:
        return now_kst().strftime('%Y-%m-%d')
    elif "어제" in raw_date:
        return (now_kst() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif "내일" in raw_date:
        return (now_kst() + timedelta(days=1)).strftime('%Y-%m-%d')
    return raw_date

@router.post("/add_order")
async def add_order(request: Request):
    data = await request.json()
    member_name = data.get("회원명", "").strip()
    if not member_name:
        return {"error": "회원명을 입력해야 합니다."}

    member_sheet = get_worksheet("DB")
    members = member_sheet.get_all_records()
    member_info = next((m for m in members if m.get("회원명") == member_name), None)
    if not member_info:
        return {"error": f"{member_name} 회원을 찾을 수 없습니다."}

    sheet = get_worksheet("제품주문")
    order_date = process_order_date(data.get("주문일자", ""))
    row = [
        order_date,
        member_name,
        member_info.get("회원번호", ""),
        member_info.get("휴대폰번호", ""),
        data.get("제품명", ""),
        data.get("제품가격", ""),
        data.get("PV", ""),
        data.get("결재방법", "카드"),
        data.get("주문자_고객명", ""),
        data.get("주문자_휴대폰번호", ""),
        data.get("배송처", ""),
        data.get("수령확인", "")
    ]
    sheet.insert_row(row, index=2)
    return {"message": "제품주문이 저장되었습니다."}