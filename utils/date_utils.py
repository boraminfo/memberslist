from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.date_utils import (
    now_kst, parse_date_string, get_kst_timestamp, parse_korean_datetime
)

router = APIRouter()


@router.get("/now_kst")
async def get_now_kst():
    return JSONResponse(content={
        "timestamp": now_kst().strftime("%Y-%m-%d %H:%M:%S")
    })


@router.post("/parse_date_string")
async def post_parse_date_string(request: Request):
    data = await request.json()
    text = data.get("text", "")
    date_str = parse_date_string(text)
    return JSONResponse(content={"parsed_date": date_str})


@router.post("/parse_korean_datetime")
async def post_parse_korean_datetime(request: Request):
    data = await request.json()
    text = data.get("text", "")
    datetime_str = parse_korean_datetime(text)
    return JSONResponse(content={"parsed_datetime": datetime_str})


@router.get("/kst_timestamp")
async def get_kst_time():
    return JSONResponse(content={"kst_timestamp": get_kst_timestamp()})
