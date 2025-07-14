from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.parser.parse_order_text import parse_order_text

router = APIRouter()

@router.post("/parse_order")
async def parse_order_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "입력 문장이 비어 있습니다."})

        result = parse_order_text(text)
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
