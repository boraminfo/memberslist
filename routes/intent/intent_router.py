# routes/intent/intent_router.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.intent_utils import detect_intent  # 유틸 함수 import

router = APIRouter(
    prefix="/intent",
    tags=["Intent"],
    
)

@router.post("/detect")
async def detect_intent_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "텍스트가 제공되지 않았습니다."})

        intent = detect_intent(text)
        return JSONResponse(status_code=200, content={"intent": intent})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
