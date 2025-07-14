from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.parser.parse_update_and_request import parse_update_and_request

router = APIRouter()

@router.post("/parse_update_and_request")
async def parse_update_and_request_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "입력된 요청문이 없습니다."})

        name, updates = parse_update_and_request(text)

        if not name:
            return JSONResponse(status_code=400, content={"error": "회원명을 추출하지 못했습니다."})

        if not updates:
            return JSONResponse(status_code=400, content={"error": "수정할 필드를 추출하지 못했습니다."})

        return JSONResponse(status_code=200, content={
            "회원명": name,
            "수정사항": updates
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
