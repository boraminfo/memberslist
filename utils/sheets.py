import os, json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import pytz
from datetime import datetime

load_dotenv()

GOOGLE_SHEET_TITLE = os.getenv("GOOGLE_SHEET_TITLE")
GOOGLE_SHEET_KEY = os.getenv("GOOGLE_SHEET_KEY")

def get_worksheet(sheet_name: str):
    try:
        keyfile_dict = json.loads(GOOGLE_SHEET_KEY)
        keyfile_dict["private_key"] = keyfile_dict["private_key"].replace("\n", "\n")
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = Credentials.from_service_account_info(keyfile_dict, scopes=scopes)
        gc = gspread.authorize(credentials)
        return gc.open(GOOGLE_SHEET_TITLE).worksheet(sheet_name)
    except Exception as e:
        print(f"[시트 접근 오류] {e}")
        return None

def now_kst():
    return datetime.now(pytz.timezone("Asia/Seoul"))