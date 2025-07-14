from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.sheets import get_worksheet  # ✅ 핵심 유틸 함수 import

router = APIRouter()

@router.get("/sheet_values", tags=["시트"])
async def get_sheet_values(sheet_name: str):
    try:
        sheet = get_worksheet(sheet_name)
        rows = sheet.get_all_values()
        return JSONResponse(content={"rows": rows})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
