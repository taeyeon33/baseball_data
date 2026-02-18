from flask import Blueprint, request, jsonify
from src.api.admin._decorators import admin_required
from src.services.crawl_service import start_game_crawler
from src.repositories.crawl_job_repositories import CrawlJobRepositories

bp = Blueprint(
    "admin_crawl",
    __name__,
    url_prefix="/api/admin"
)

@bp.route("/crawl/games", methods=["POST"])
@admin_required
def crawl_games():
    data = request.get_json(silent=True) or {}
    
    league = "NPB"
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    try:
        job_id = start_game_crawler(league, start_date, end_date)
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
    
@bp.route("/crawl/job_status/<int:job_id>", methods=["GET"])
@admin_required
def crawl_job_status(job_id):
    try:
        job = CrawlJobRepositories.get_job(job_id)
        if not job:
            return jsonify({f"message": "존재하지 않는 job_id: {job_id} 입니다."}), 404
        
        success_count =  CrawlJobRepositories.count_success_items(job_id)
        total_count = CrawlJobRepositories.count_total_items(job_id)

        percent = int((success_count / total_count) * 100) if total_count else 0
        completed = job["status"] in ("completed", "skipped", "failed")
        message = f"{success_count}/{total_count} 게임 처리됨"

        return jsonify({
            "job_id": job_id,
            "percent": percent,
            "count": success_count,
            "total": total_count,
            "message": message,
            "completed": completed
        }), 200
    
    except Exception as e:
        return jsonify({"message": "진행률 조회 중 오류가 발생했습니다.", "error": str(e)}), 500