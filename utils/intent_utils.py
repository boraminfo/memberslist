import re

def detect_intent(text: str) -> str:
    """
    자연어 문장에서 의도를 추출합니다.
    반환값: 등록 / 수정 / 삭제 / 조회 / 기타
    """
    text = text.strip()

    if re.match(r"회원등록\s", text):
        return "등록"
    elif re.match(r"\S+\s+수정\s", text):  # 예: "이판주 수정 ..."
        return "수정"
    elif re.match(r"\S+\s+삭제", text):   # 예: "이판주 삭제"
        return "삭제"
    elif re.search(r"(상세정보|조회|기본정보|정보|알려줘)", text):
        return "조회"
    else:
        return "기타"


