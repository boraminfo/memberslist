import re

def normalize_sheet_keywords(text: str) -> str:
    """
    시트 관련 키워드를 표준화합니다.
    """
    replacements = {
        "개인 메모": "개인메모",
        "상담 일지": "상담일지",
        "활동 일지": "활동일지",
        "회원 메모": "회원메모",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def parse_counseling_command(text: str) -> tuple:
    """
    자연어 문장에서 회원명, 시트명, 본문을 추출합니다.
    반환: (회원명, 시트명, 본문)
    """
    text = normalize_sheet_keywords(text)
    sheet_keywords = ["상담일지", "개인메모", "활동일지", "회원메모"]
    action_keywords = ["저장", "기록", "입력"]

    matched_sheet = next((kw for kw in sheet_keywords if kw in text), None)
    if not matched_sheet:
        raise ValueError("시트명을 찾을 수 없습니다.")

    # 회원명 추출
    match = re.search(r"([가-힣]{2,3})\s*" + matched_sheet, text)
    if not match:
        raise ValueError("회원명을 찾을 수 없습니다.")
    member_name = match.group(1)

    # 본문 정리
    cleaned = text
    for kw in sheet_keywords + action_keywords:
        cleaned = cleaned.replace(f"{member_name}{kw}", "")
        cleaned = cleaned.replace(f"{member_name} {kw}", "")
        cleaned = cleaned.replace(kw, "")
    cleaned = re.sub(r'^[:：]\s*', '', cleaned).strip()

    return member_name, matched_sheet, cleaned

