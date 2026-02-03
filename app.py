from flask import Flask, session, redirect, send_from_directory

from src.config import UI_DIR, CSS_DIR, JS_DIR, SECRET_KEY
from src.api import ALL_BLUEPRINTS

def create_app():
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False
    app.secret_key = SECRET_KEY

    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)

    return app

app = create_app()

# index.html
@app.route("/")
def index_page():
    return send_from_directory(UI_DIR, "index.html")

# css 파일 로딩
@app.route("/static/css/<path:filename>")
def css_files(filename):
    return send_from_directory(CSS_DIR, filename)

# js 파일 로딩
@app.route("/static/js/<path:filename>")
def js_files(filename):
    return send_from_directory(JS_DIR, filename)

# 로그인 페이지
@app.route("/login")
def login_page():
    if session.get("is_admin"):
        return redirect("/admin")
    return send_from_directory(UI_DIR, "login.html")

# 관리자 페이지
@app.route("/admin")
def admin_page():
    if not session.get("is_admin"):
        return redirect("/login")
    return send_from_directory(UI_DIR, "admin.html")

# 관리자 페이지 팝업
@app.route("/admin/crawl_popup")
def admin_crawl_popup():
    if not session.get("is_admin"):
        return redirect("/login")
    return send_from_directory(UI_DIR, "crawl_popup.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
