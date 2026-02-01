from flask import Blueprint, request, jsonify
from src.api.admin._decorators import admin_required
from src.services.admin_service import start_games_crawl

from datetime import datetime

bp = Blueprint(
    "admin_crawl",
    __name__,
    url_prefix="/api/admin"
)

@bp.route("/crawls/games", methods=["POST"])
@admin_required
def crawl_games():
    data = request.get_json(silent=True) or {}

    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    try:
        job_id = start_games_crawl(start_date, end_date)
        return jsonify({
            "job_id": job_id,
            "status": "running",
            "range": {
                "start": start_date,
                "end": end_date
            }
        }), 201
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500