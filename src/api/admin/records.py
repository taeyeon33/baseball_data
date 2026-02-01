from flask import Blueprint, request, jsonify
from src.api.admin._decorators import admin_required
from src.services.admin_service import insert_data, update_data, delete_data

bp = Blueprint(
    "admin_records",
    __name__,
    url_prefix="/api/admin"
)

@bp.route("/insert", methods=["POST"])
@admin_required
def api_admin_insert():
    data = request.json
    if not data or "table" not in data:
        return jsonify({"message": "데이터 형식이 올바르지 않습니다."}), 400

    try:
        result = insert_data(data)
        return {"message": result}
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500

@bp.route("/update", methods=["POST"])
@admin_required
def api_admin_update():
    data = request.json
    if not data or "table" not in data:
        return jsonify({"message": "데이터 형식이 올바르지 않습니다."}), 400
    
    try:
        result = update_data(data)
        return {"message": result}
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500

@bp.route("/delete", methods=["POST"])
@admin_required
def api_admin_delete():
    data = request.json
    if not data or "table" not in data:
        return jsonify({"message": "데이터 형식이 올바르지 않습니다."}), 400
    
    try:
        result = delete_data(data)
        return {"message": result}
    
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "알 수 없는 오류가 발생했습니다."}), 500