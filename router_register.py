from fastapi import FastAPI

# ---------------------- 회원(Member) ----------------------
from routes.member.find_member import router as find_member_router
from routes.common.get_sheet_values import router as get_sheet_values_router



# ---------------------- 공통(Common) / 도구(Tools) ----------------------

# ---------------------- 의도(Intent) ----------------------


# ---------------------- 자연어 파싱(Parse) ----------------------



# ---------------------- 디버그 및 도구(Debug / Tools) ----------------------
 # 환경 설정 상태 확인
    # 날짜 유틸리티 관련 API
  # 의도 감지 테스트 API
          # Google Sheets 데이터 확인용

# ---------------------- 회원(Member) 추가 기능 ----------------------
      # 회원 관련 의도 파싱
        # 시트 값 확인 API




# 추가
















def register_routers(app: FastAPI):
    # ---------------------- 회원(Member) ----------------------
    app.include_router(find_member_router)  # 회원 조회 기능
    app.include_router(get_sheet_values_router) 

    
    # ---------------------- 공통(Common) / 도구(Tools) ----------------------
    # (현재 생략되어 있으나, 추후 필요시 추가 가능)

    # ---------------------- 의도(Intent) ----------------------
     # 자연어 문장 기반 intent 처리

    # ---------------------- 자연어 파싱(Parse) ----------------------
      # 상담일지용 자연어 파싱
         # 회원 정보 삭제 파싱
               # 제품 주문용 자연어 파싱
         # 회원 등록용 자연어 파싱
    # 회원 정보 수정용 자연어 파싱

    # ---------------------- 디버그 및 도구(Debug / Tools) ----------------------
       # 설정 확인 API
         # 날짜 변환/테스트 API
      # 의도 감지 전용 API
            # 시트 내용 확인 API

    # ---------------------- 회원(Member) 추가 기능 ----------------------
 # 회원 관련 요청 intent 파싱 API
       # 시트 행 데이터 출력 API



# 추가
 



    