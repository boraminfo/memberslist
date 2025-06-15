from fastapi import APIRouter

router = APIRouter()

@router.post("/delete_order")
async def delete_order_handler():
    return {"message": "This is the delete_order route."}