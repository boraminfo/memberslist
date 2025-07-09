from flask import Blueprint, request, jsonify
from utils.sheets import get_worksheet
from utils.date_utils import parse_korean_datetime
import re
from datetime import datetime

search_memo_bp = Blueprint("search_memo_bp", __name__)








def extract_nouns(text):
    return re.findall(r"[가-힣]{2,}", text)

@search_memo_bp.route("/search_memo_by_tags", methods=["GET"])
def search_memo_by_tags():
    try:
        data = request.get_json()
        input_tags = data.get("tags", [])
        limit = int(data.get("limit", 10))
        sort_by = data.get("sort_by", "date").lower()
        min_match = int(data.get("min_match", 1))

        if not input_tags:
            return jsonify({"error": "태그 리스트가 비어 있습니다."}), 400
        if sort_by not in ["date", "tag"]:
            return jsonify({"error": "sort_by는 'date' 또는 'tag'만 가능합니다."}), 400

        sheet = get_worksheet("개인메모")
        values = sheet.get_all_values()[1:]  # 헤더 제외
        results = []

        for row in values:
            if len(row) < 3:
                continue
            member, date_str, content = row[0], row[1], row[2]

            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                continue  # 날짜 형식 오류시 건너뜀

            memo_tags = extract_nouns(content)
            similarity = len(set(input_tags) & set(memo_tags))
            if similarity >= min_match:
                results.append({
                    "회원명": member,
                    "날짜": date_str,
                    "내용": content,
                    "일치_태그수": similarity,
                    "날짜_obj": parsed_date
                })

        # 정렬
        if sort_by == "tag":
            results.sort(key=lambda x: (x["일치_태그수"], x["날짜_obj"]), reverse=True)
        else:
            results.sort(key=lambda x: (x["날짜_obj"], x["일치_태그수"]), reverse=True)

        for r in results:
            del r["날짜_obj"]

        return jsonify({"검색결과": results[:limit]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
