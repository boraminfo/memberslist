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
        row_name = str(row.get("회원명", "")).strip()
        row_number = str(row.get("회원번호", "")).strip()

        # 디버깅용 로그 (원할 경우 주석 처리 가능)
        print(f"확인 중: 회원명={row_name}, 회원번호={row_number}")

        if name and number:
            if row_name == name and row_number == number:
                return row
        elif name:
            if row_name == name:
                return row
        elif number:
            if row_number == number:
                return row

    return {"error": f"'{name or number}'에 해당하는 회원 정보를 찾을 수 없습니다."}

    





    