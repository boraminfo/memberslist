import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_register import register_routers



# ✅ 환경변수 로드 (로컬에서만 작동)
if os.getenv("RENDER") is None:
    dotenv_path = os.path.abspath(".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

# ✅ FastAPI 인스턴스 생성
app = FastAPI(
    title="회원관리 시스템 API",
    description="회원, 주문, 메모, 상담일지 등을 관리하는 FastAPI 기반 백엔드",
    version="1.0.0"
)

# ✅ CORS 설정 (프론트 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://members-list-boram.onrender.com"],  # ✅ 허용할 프론트 도메인
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)




# ✅ 라우터 등록
register_routers(app)

# ✅ 루트 경로 (기본 상태 확인용)
@app.get("/")
def root():
    return {"message": "FastAPI 서버가 실행 중입니다."}



