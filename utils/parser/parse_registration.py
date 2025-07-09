import re

def parse_registration(text: str):
    """
    자연어 문장에서 회원 등록 정보를 추출합니다.
    반환: (회원명, 회원번호, 휴대폰번호, 계보도)
    """
    text = text.replace("\n", " ").replace("\r", " ").replace("\xa0", " ").strip()

    name = number = phone = lineage = ""

    # ✅ 휴대폰번호 추출 (010-xxxx-xxxx 또는 010xxxxxxxx)
    phone_match = re.search(r"010[-]?\d{4}[-]?\d{4}", text)
    if phone_match:
        phone = phone_match.group(0)

    # ✅ 회원번호 추출 (숫자 6자리 이상)
    number_match = re.search(r"\b회원번호\s*[:\-]?\s*(\d{6,})\b", text)
    if number_match:
        number = number_match.group(1)
    else:
        # fallback: 회원번호 없이도 등록 문장 내에 숫자 추출
        fallback_number = re.search(r"\b(\d{6,})\b", text)
        if fallback_number:
            number = fallback_number.group(1)

    # ✅ 한글 이름 추출 (회원명 또는 첫 번째 한글 단어)
    korean_words = re.findall(r"[가-힣]{2,}", text)
    if korean_words:
        name = korean_words[0]

    # ✅ 계보도 추출 (예: 강소희 우측, 임채영 좌측 등)
    lineage_match = re.search(r"계보도[를은는]?\s*([가-힣]{2,})\s*(좌측|우측|왼쪽|오른쪽|라인)?", text)
    if lineage_match:
        lineage_name = lineage_match.group(1)
        direction = lineage_match.group(2) or ""
        lineage = f"{lineage_name} {direction}".strip()

    # ✅ fallback 계보도 (예: 강소희우측 → 강소희 우측)
    if not lineage:
        for word in korean_words:
            if any(d in word for d in ["좌측", "우측", "왼쪽", "오른쪽"]):
                lineage = re.sub(r"(좌측|우측|왼쪽|오른쪽)", r" \1", word).strip()

    return name or None, number or None, phone or None, lineage or None

