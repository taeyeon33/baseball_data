from functools import wraps
from flask import session, abort

# 관리자 인증
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            abort(403, description="admin only")
        return fn(*args, **kwargs)
    return wrapper