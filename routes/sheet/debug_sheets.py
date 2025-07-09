from flask import Blueprint, jsonify
from utils.sheets import get_gspread_client
import os

sheet_bp = Blueprint('sheet', __name__)

@sheet_bp.route('/debugSheets', methods=['GET'])
def debug_sheets():
    client = get_gspread_client()
    sheet = client.open(os.getenv("GOOGLE_SHEET_TITLE"))
    worksheets = sheet.worksheets()
    sheet_names = [ws.title for ws in worksheets]
    return jsonify(sheet_names)
