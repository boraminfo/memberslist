from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.parser.parse_counseling import parse_counseling_command

router = APIRouter()

@router.post("/parse_counseling")
async def parse_counseling_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "입력 텍스트가 비어 있습니다."})

        member, sheet, content = parse_counseling_command(text)

        return JSONResponse(status_code=200, content={
            "회원명": member,
            "시트명": sheet,
            "내용": content
        })

    except ValueError as ve:
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
