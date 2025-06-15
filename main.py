from fastapi import FastAPI
from routes import (
    register, update, delete_member, add_order, delete_order,
    add_counseling, add_memo, add_activity, search_order,
    find_member
)

app = FastAPI()  # ✅ FastAPI 인스턴스를 먼저 선언

app.include_router(register.router)
app.include_router(update.router)
app.include_router(delete_member.router)
app.include_router(add_order.router)
app.include_router(delete_order.router)
app.include_router(add_counseling.router)
app.include_router(add_memo.router)
app.include_router(add_activity.router)
app.include_router(search_order.router)
app.include_router(find_member.router)  



@app.get("/")
def home():
    return {"message": "FastAPI 서버가 실행 중입니다."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
    