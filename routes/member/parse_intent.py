from fastapi import APIRouter, Request
from utils.parser.parse_member_query_api import parse_member_query_api

router = APIRouter()

@router.post("/parse-intent", tags=["회원"])
async def parse_intent(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return {"error": "text 필드를 보내주세요."}

    result = parse_member_query_api(text)
    return result
