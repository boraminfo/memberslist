from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.parser.parse_registration import parse_registration

router = APIRouter()

@router.post("/parse_registration")
async def parse_registration_api(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text:
            return JSONResponse(status_code=400, content={"error": "입력 문장이 비어 있습니다."})

        name, number, phone, lineage = parse_registration(text)

        return JSONResponse(status_code=200, content={
            "회원명": name,
            "회원번호": number,
            "휴대폰번호": phone,
            "계보도": lineage
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
