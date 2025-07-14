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
    assert response.json() == {
        "회원명": "이태수",
        "정보": {"회원번호": "001", "휴대폰번호": "010-1234-5678"}
    }

def test_find_nonexistent_member():
    response = client.post("/find", json={"회원명": "없는사람"})
    assert response.status_code == 200
    assert response.json() == {"message": "없는사람 회원을 찾을 수 없습니다."}
