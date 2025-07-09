from datetime import datetime, timedelta
import pytz
import re

KST = pytz.timezone("Asia/Seoul")

def now_kst() -> datetime:
    """현재 한국 시간 반환"""
    return datetime.now(KST)

def parse_date_string(text: str) -> str:
    """
    자연어 또는 날짜 문자열에서 YYYY-MM-DD 형식으로 반환
    허용 입력: 오늘, 어제, 내일, 2024-07-01, 2024.07.01, 2024/07/01
    """
    text = text.strip()

    if "오늘" in text:
        return now_kst().strftime("%Y-%m-%d")
    elif "어제" in text:
        return (now_kst() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif "내일" in text:
        return (now_kst() + timedelta(days=1)).strftime("%Y-%m-%d")

    # 날짜 패턴: YYYY-MM-DD or YYYY.MM.DD or YYYY/MM/DD
    match = re.search(r"(20\d{2})[./-](\d{1,2})[./-](\d{1,2})", text)
    if match:
        try:
            year, month, day = map(int, match.groups())
            dt = datetime(year, month, day, tzinfo=KST)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    # 기본값: 오늘
    return now_kst().strftime("%Y-%m-%d")

def get_kst_timestamp() -> str:
    """
    현재 한국 시간의 타임스탬프 문자열 반환
    예: 2025-07-09 12:34
    """
    return now_kst().strftime("%Y-%m-%d %H:%M")







def parse_korean_datetime(text: str) -> str:
    """
    '오늘', '어제', '내일' 등의 한국어 날짜 문장을 YYYY-MM-DD HH:MM 형식으로 반환
    """
    if "오늘" in text:
        dt = now_kst()
    elif "어제" in text:
        dt = now_kst() - timedelta(days=1)
    elif "내일" in text:
        dt = now_kst() + timedelta(days=1)
    else:
        dt = now_kst()

    return dt.strftime("%Y-%m-%d %H:%M")
