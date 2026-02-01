from flask import Blueprint, request, jsonify
from src.api.admin._decorators import admin_required
from src.services.admin_service import get_all_tables, get_data_list

bp = Blueprint(
    "admin_tables",
    __name__,
    url_prefix="/api/admin"
)

# 테이블 목록 데이터
@bp.route("/tables", methods=["POST"])
@admin_required
def api_admin_tables():
    try:
        tables = get_all_tables()
        return jsonify(tables)
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500

# 선수 목록 데이터
@bp.route("/datalist", methods=["POST"])
@admin_required
def api_admin_dataList():
    data = request.json
    if not data or "table" not in data:
        return jsonify({"message": "데이터 형식이 올바르지 않습니다."}), 400
    
    try:
        dataList = get_data_list(data)
        return jsonify(dataList)
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500
