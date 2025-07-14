from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.config import (
    GOOGLE_SHEET_TITLE,
    GOOGLE_SHEET_KEY,
    GOOGLE_CREDENTIALS_PATH,
    OPENAI_API_KEY
)

router = APIRouter()

@router.get("/config_status")
async def config_status():
    return JSONResponse(content={
        "GOOGLE_SHEET_TITLE": GOOGLE_SHEET_TITLE,
        "GOOGLE_SHEET_KEY": "✅ 설정됨" if GOOGLE_SHEET_KEY else "❌ 없음",
        "GOOGLE_CREDENTIALS_PATH": GOOGLE_CREDENTIALS_PATH,
        "OPENAI_API_KEY": "✅ 설정됨" if OPENAI_API_KEY else "❌ 없음"
    })
