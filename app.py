from flask import Flask, request, session, jsonify, redirect, send_from_directory, abort
from functools import wraps
import subprocess
import os

from src.db.connect import get_connection
from src.config import UI_DIR, CSS_DIR, JS_DIR

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "local-admin")

# 관리자 인증
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            abort(403, description="admin only")
        return fn(*args, **kwargs)
    return wrapper

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

# 로그인
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    if data.get("password") == ADMIN_PASSWORD:
        session["is_admin"] = True
        return {"message": "login success"}, 200
    return {"message": "login fail"}, 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return {"message": "logout success"}, 200

# 관리자 페이지
@app.route("/admin")
def admin_page():
    if not session.get("is_admin"):
        return redirect("/login")
    return send_from_directory(UI_DIR, "admin.html")


if __name__ == "__main__":
    print(os.path.exists(os.path.join(UI_DIR, "index.html")))
    app.run(debug=True)
