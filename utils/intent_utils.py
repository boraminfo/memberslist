# utils/intent_utils.py

def detect_intent(text: str) -> str:
    """간단한 키워드 기반 intent 판별 함수"""
    if "조회" in text:
        return "조회"
    elif "등록" in text:
        return "등록"
    elif "수정" in text:
        return "수정"
    elif "삭제" in text:
        return "삭제"
    else:
        return "기타"
