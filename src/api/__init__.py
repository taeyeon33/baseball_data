from src.api.admin.auth import bp as admin_auth_bp
from src.api.admin.tables import bp as admin_tables_bp
from src.api.admin.records import bp as admin_records_bp

ALL_BLUEPRINTS = [
    admin_auth_bp,
    admin_tables_bp,
    admin_records_bp
]