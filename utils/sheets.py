from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/sheet_values", tags=["시트"])
async def get_sheet_values(sheet_name: str):
    try:
        sheet = get_worksheet(sheet_name)
        rows = sheet.get_all_values()
        return JSONResponse(content={"rows": rows})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})



def get_worksheet(sheet_name: str):
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import os

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open(os.getenv("GOOGLE_SHEET_TITLE"))  # .env에서 읽도록
    return spreadsheet.worksheet(sheet_name)


