import re
from utils.sheets import get_worksheet

def parse_update_request(text):
    """
    다양한 형태의 자연어에서 회원명과 수정 필드를 추출
    """
    # ✅ 회원메모 단독 처리 분기: 저장/수정 키워드 포함 시
    if "회원메모" in text and any(kw in text for kw in ["저장", "수정"]):
        return None, None  # 이후 상위 로직에서 메모 저장 분기로 처리 가능

    # 계보도 대상자 제외
    lineage_match = re.search(r"계보도[를은는]?[ ]*([가-힣]{2,})", text)
    exclude_name = lineage_match.group(1) if lineage_match else None

    sheet = get_worksheet("DB")
    db = sheet.get_all_records()
    member_names = [row.get("회원명", "").strip() for row in db if row.get("회원명")]
    member_names = sorted(set(member_names), key=len, reverse=True)

    name = next((n for n in member_names if n != exclude_name and n in text), None)

    # 기본 정규식 방식
    match = re.search(rf"{name}의\s*(\S+)\s*를\s*(.+?)\s*(으로|로)?\s*(바꿔|변경|수정)", text) if name else None
    if match:
        field = match.group(1).strip()
        value = match.group(2).strip()
        return name, {field: value}

    # ✅ 간단한 패턴 대응: "홍길동 수정 010-1234-7777"
    if name and re.search(r"수정|변경|바꿔", text):
        phone_match = re.search(r"010[-]?\d{3,4}[-]?\d{4}", text)

        if phone_match:
            return name, {"휴대폰번호": phone_match.group()}

        # 🔢 숫자만 있을 경우 → 회원번호로 간주
        num_match = re.search(r"\b\d{4,8}\b", text)
        if num_match:
            return name, {"회원번호": num_match.group()}

    # ❌ 회원명 없이 시작한 경우 → 중단
    if not name:
        return None, None  # 회원명 없음 → 중단

    return name, None
