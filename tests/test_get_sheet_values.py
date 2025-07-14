import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from unittest.mock import patch, MagicMock

from routes.common.get_sheet_values import router

app = FastAPI()
app.include_router(router)

@pytest.mark.asyncio
async def test_get_sheet_values_success():
    mock_sheet = MagicMock()
    mock_sheet.get_all_values.return_value = [
        ["이름", "나이"],
        ["홍길동", "30"]
    ]

    # ✅ 정확한 patch 대상 경로
    with patch("routes.common.get_sheet_values.get_worksheet", return_value=mock_sheet):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/sheet_values?sheet_name=DB")

    assert response.status_code == 200
    assert response.json() == {
        "rows": [["이름", "나이"], ["홍길동", "30"]]
    }

@pytest.mark.asyncio
async def test_get_sheet_values_error():
    with patch("routes.common.get_sheet_values.get_worksheet", side_effect=Exception("시트 없음")):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/sheet_values?sheet_name=없는시트")

    assert response.status_code == 500

    # ✅ 누락된 부분 추가
    json_body = response.json()
    assert "error" in json_body
    assert json_body["error"] == "시트 없음"
