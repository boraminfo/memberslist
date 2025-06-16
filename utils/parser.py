import re

# ✅ 필드 매핑 정의
field_map = {
    "휴대폰번호": "휴대폰번호",
    "주소": "주소",
    "비밀번호": "비밀번호"
}

# ✅ 자연어 요청문에서 회원명 + 수정할 필드 추출
def parse_text_to_fields(text: str):
    name = ""
    updates = {}

    for field in field_map:
        if field in text:
            match = re.match(rf"(.+?)\s+(수정|변경)\s+{field}\s+(.+)", text)
            if match:
                name = match.group(1).strip()
                value = match.group(3).strip()
                updates[field_map[field]] = value
                break
    return name, updates
