from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.sheets import get_worksheet
from fastapi.responses import JSONResponse  # ⛳ 빠진 부분!

router = APIRouter()




@router.post("/find", tags=["회원"])
async def find_member(request: Request):
    try:
        data = await request.json()
        name = data.get("회원명")

        if not name:
            return JSONResponse(status_code=400, content={"error": "회원명을 입력해주세요."})

        sheet = get_worksheet("DB")
        rows = sheet.get_all_records()  # 첫 줄은 헤더로 자동 처리됨

        for row in rows:
            if row.get("회원명") == name:
                return JSONResponse(content={"회원명": name, "정보": row})

        return JSONResponse(content={"message": f"{name} 회원을 찾을 수 없습니다."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
