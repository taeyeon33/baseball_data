from flask import Flask, request, session, jsonify, redirect, send_from_directory, abort
from functools import wraps
# import subprocess
import os

from src.db.connect import get_connection
from src.config import UI_DIR, CSS_DIR, JS_DIR

from src.services.admin_service import get_all_tables, get_all_players, insert_data

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

# 테이블 목록 데이터
@app.route("/api/admin/tables", methods=["POST"])
@admin_required
def api_admin_tables():
    tables = get_all_tables()
    return jsonify(tables)

# 선수 목록 데이터
@app.route("/api/admin/players", methods=["POST"])
@admin_required
def api_admin_players():
    players = get_all_players()
    return jsonify(players)

@app.route("/api/admin/insert", methods=["POST"])
@admin_required
def api_admin_insert():
    data = request.json
    if not data or "table" not in data:
        return jsonify({"message": "데이터 형식이 올바르지 않습니다."}), 400

    result = insert_data(data)
    return {"message": result}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
