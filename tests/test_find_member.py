import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock

from routes.member.find_member import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_find_member_success():
    mock_rows = [
        {"회원명": "홍길동", "휴대폰번호": "010-1234-5678", "가입일자": "2024-01-01"},
        {"회원명": "이순신", "휴대폰번호": "010-0000-0000", "가입일자": "2023-12-01"},
    ]

    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = mock_rows

    with patch("routes.member.find_member.get_worksheet", return_value=mock_sheet):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/find", json={"회원명": "홍길동"})

    assert response.status_code == 200
    assert response.json() == {
        "회원명": "홍길동",
        "정보": {
            "회원명": "홍길동",
            "휴대폰번호": "010-1234-5678",
            "가입일자": "2024-01-01"
        }
    }

@pytest.mark.asyncio
async def test_find_member_not_found():
    mock_rows = [
        {"회원명": "홍길동"},
    ]

    mock_sheet = MagicMock()
    mock_sheet.get_all_records.return_value = mock_rows

    with patch("routes.member.find_member.get_worksheet", return_value=mock_sheet):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/find", json={"회원명": "김철수"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "김철수 회원을 찾을 수 없습니다."
    }

@pytest.mark.asyncio
async def test_find_member_no_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/find", json={})

    assert response.status_code == 400
    assert response.json()["error"] == "회원명을 입력해주세요."
