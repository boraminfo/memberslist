import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from routes.member.parse_intent import router  # 경로 확인 필요

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_parse_intent_success():
    with patch("routes.member.parse_intent.parse_member_query_api", return_value={"회원명": "홍길동", "휴대폰번호": "010-1234-5678"}):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/parse-intent", json={"text": "홍길동 전화번호 알려줘"})

    assert response.status_code == 200
    assert response.json() == {
        "회원명": "홍길동",
        "휴대폰번호": "010-1234-5678"
    }

@pytest.mark.asyncio
async def test_parse_intent_missing_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/parse-intent", json={})  # text 빠짐

    assert response.status_code == 200  # 기본 응답이 JSONResponse가 아니라 dict
    assert response.json() == {
        "error": "text 필드를 보내주세요."
    }
