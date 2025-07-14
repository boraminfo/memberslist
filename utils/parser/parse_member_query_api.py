import re

def parse_member_query_api(text: str) -> dict:
    # intent 파싱 로직 예시
    FIELD_KEYWORDS = {
        "주소": "주소",
        "전화번호": "휴대폰번호",
        "번호": "휴대폰번호",
        "카드번호": "카드번호",
        "생일": "생년월일",
        "비번": "비밀번호",
    }

    result = {"intent": "조회", "회원명": None, "필드": None}

    import re
    name_match = re.match(r"([가-힣]{2,4})(님|씨|선생님)?", text)
    if name_match:
        result["회원명"] = name_match.group(1)

    for keyword, field in FIELD_KEYWORDS.items():
        if keyword in text:
            result["필드"] = field
            break

    return result
