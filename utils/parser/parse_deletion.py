# utils/parser/parse_deletion.py

import re

def parse_deletion_request(text: str):
    """
    예시:
    - 입력: "이태수 카드번호, 주소 지워줘"
    - 출력: ("이태수", ["카드번호", "주소"])
    """

    # 1. 회원명 추출 (맨 앞 2~5글자의 한글 이름)
    name_match = re.match(r'^([가-힣]{2,5})', text)
    name = name_match.group(1) if name_match else None

    # 2. 삭제 가능한 필드 목록 정의
    delete_keywords = [
        "카드번호", "주소", "전화번호", "휴대폰번호", "비밀번호",
        "생년월일", "계보도", "소개한분", "카드사", "유효기간",
        "비번", "회원번호", "직업", "메모", "카드주인"
    ]
