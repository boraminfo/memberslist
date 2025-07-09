from flask import Flask
from dotenv import load_dotenv
import os

# ✅ 환경변수 로드 (로컬에서만)
if os.getenv("RENDER") is None:
    dotenv_path = os.path.abspath('.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

# ✅ Flask 앱 생성
app = Flask(__name__)

# ✅ Blueprint 등록 함수로 분리
def register_blueprints(app):
    # 🧩 Member 관련
    from routes.member.save_member import save_member_bp
    from routes.member.update_member import update_member_bp
    from routes.member.delete_member import delete_member_bp
    from routes.member.find_member import find_member_bp
    app.register_blueprint(save_member_bp)
    app.register_blueprint(update_member_bp)
    app.register_blueprint(delete_member_bp)
    app.register_blueprint(find_member_bp)

    # 🧩 Order 관련
    from routes.order.parse_and_save_order import parse_order_bp
    from routes.order.save_order_from_json import save_order_json_bp
    from routes.order.delete_order_request import delete_order_req_bp
    from routes.order.delete_order_confirm import delete_order_conf_bp
    app.register_blueprint(parse_order_bp)
    app.register_blueprint(save_order_json_bp)
    app.register_blueprint(delete_order_req_bp)
    app.register_blueprint(delete_order_conf_bp)

    # 🧩 Note 관련
    from routes.note.add_counseling import add_counseling_bp
    from routes.note.search_memo_by_tags import search_memo_bp
    app.register_blueprint(add_counseling_bp)
    app.register_blueprint(search_memo_bp)

    # 🧩 Sheet 디버깅
    from routes.sheet.debug_sheets import sheet_bp
    app.register_blueprint(sheet_bp)




# ✅ 홈 라우트
@app.route("/")
def home():
    return "✅ Flask 서버가 실행 중입니다."




# ✅ 앱 실행
if __name__ == "__main__":
    register_blueprints(app)
    app.run(host="0.0.0.0", port=10000)



# 변경해야 해요


