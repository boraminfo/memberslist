# tests/test_find_member.py

from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.member.find_member import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_find_existing_member():
    response = client.post("/find", json={"회원명": "이태수"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("회원명") == "이태수"
    assert "정보" in data
    assert isinstance(data["정보"], dict)

