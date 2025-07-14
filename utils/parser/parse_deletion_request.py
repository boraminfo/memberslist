from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse



router = APIRouter()

@router.post("/parse_deletion_request")
async def parse_deletion_request_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "입력 문장이 비어 있습니다."})

        name, fields = parse_deletion_request(text)
        if not name:
            return JSONResponse(status_code=400, content={"error": "회원명을 추출할 수 없습니다."})
        if not fields:
            return JSONResponse(status_code=400, content={"error": "삭제할 필드가 감지되지 않았습니다."})

        return JSONResponse(status_code=200, content={
            "회원명": name,
            "삭제필드": fields
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
