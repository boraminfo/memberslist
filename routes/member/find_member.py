from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.sheets import get_worksheet

router = APIRouter()

class MemberRequest(BaseModel):
    회원명: str

@router.post("/find", tags=["회원"])
async def find_member(request: MemberRequest):
    name = request.회원명

    try:
        sheet = get_worksheet("DB")
        rows = sheet.get_all_records()

        for row in rows:
            if row.get("회원명") == name:
                return JSONResponse(content={"회원명": name, "정보": row})

        return JSONResponse(content={"message": f"{name} 회원을 찾을 수 없습니다."})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
