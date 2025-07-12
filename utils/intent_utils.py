import re

def detect_intent(text: str) -> str:
    """
    자연어 문장에서 의도를 추출합니다.
    반환값: 등록 / 수정 / 삭제 / 조회 / 주문 / 기타
    """
    text = text.strip()

    if "회원메모" in text and any(word in text for word in ["저장", "수정"]):
        return "수정"  # ✅ 회원메모 관련 요청은 수정 분기로 처리
    elif re.match(r"회원등록\s", text):
        return "등록"
    elif any(word in text for word in ["수정", "바꿔", "바꿔줘", "변경", "바꾸기"]):
        return "수정"
    elif re.match(r"\S+\s+삭제", text):   # 예: "이판주 삭제"
        return "삭제"
    elif re.search(r"(상세정보|조회|기본정보|정보|알려줘)", text):
        return "조회"
    elif any(word in text for word in ["주문", "제품주문", "결제", "구매"]):  # 🔥 추가된 부분
        return "주문"
    else:
        return "기타"
