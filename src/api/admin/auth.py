from flask import Blueprint, request, session
from src.config import ADMIN_PASSWORD

bp = Blueprint(
    "admin_auth",
    __name__,
    url_prefix="/api/admin"
)

# 로그인
@bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    if data.get("password") == ADMIN_PASSWORD:
        session["is_admin"] = True
        return {"message": "login success"}, 200
    return {"message": "login fail"}, 401

@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return {"message": "logout success"}, 200
