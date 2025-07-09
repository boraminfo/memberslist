import re

def parse_request_and_update(text: str, member: dict) -> tuple:
    """
    자연어 문장에서 수정할 필드와 값을 추출하여 member 딕셔너리를 수정합니다.
    반환: (수정된 member 딕셔너리, 수정된 필드 목록)
    """
    updated_fields = {}

    field_map = {
        "회원명": "회원명",
        "휴대폰번호": "휴대폰번호",
        "회원번호": "회원번호",
        "계보도": "계보도",
        "비밀번호": "비밀번호",
        "주소": "주소",
        "직업": "근무처",
        "직장": "근무처",
        "메모": "메모",
    }

    # ✅ 계보도 패턴 우선 적용
    lineage_pattern = re.search(r"계보도[를은는]?\s*([가-힣]{2,})\s*(좌측|우측|왼쪽|오른쪽|라인)?", text)
    if lineage_pattern:
        name_part = lineage_pattern.group(1)
        direction = lineage_pattern.group(2) or ""
        value = f"{name_part} {direction}".strip()
        member["계보도"] = value
        updated_fields["계보도"] = value

    # ✅ 일반 필드 패턴 처리
    for keyword, field in field_map.items():
        pattern = rf"{keyword}(?:를|은|는|이|:|：)?\s*(?P<value>[\w가-힣\d\-@!#%^&*.]+)"
        for match in re.finditer(pattern, text):
            value = match.group("value").strip()
            if field == "휴대폰번호":
                phone_match = re.search(r"010[-]?\d{3,4}[-]?\d{4}", value)
                value = phone_match.group(0) if phone_match else value
            elif field == "회원번호":
                value = re.sub(r"[^\d]", "", value)
            elif field == "계보도":
                continue  # 위에서 이미 처리됨

            member[field] = value
            updated_fields[field] = value

    return member, updated_fields


