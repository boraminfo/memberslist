import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from routes.intent.intent_router import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_detect_intent_success():
    with patch("routes.intent.intent_router.detect_intent", return_value="회원조회"):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/intent/detect", json={"text": "홍길동 전화번호 알려줘"})

    assert response.status_code == 200
    assert response.json() == {"intent": "회원조회"}

@pytest.mark.asyncio
async def test_detect_intent_missing_text():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/intent/detect", json={})

    assert response.status_code == 400
    assert response.json()["error"] == "텍스트가 제공되지 않았습니다."

@pytest.mark.asyncio
async def test_detect_intent_exception():
    with patch("routes.intent.intent_router.detect_intent", side_effect=Exception("의도 분석 실패")):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/intent/detect", json={"text": "에러 발생해봐"})

    assert response.status_code == 500
    assert "error" in response.json()
    assert response.json()["error"] == "의도 분석 실패"
