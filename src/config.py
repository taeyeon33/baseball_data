from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASE_DIR = "."

UI_DIR = f"{BASE_DIR}/src/ui/templates"

CSS_DIR = f"{BASE_DIR}/src/ui/static/css"
JS_DIR = f"{BASE_DIR}/src/ui/static/js"

DB_PATH = f"{BASE_DIR}/db/test.db"
TEST_DB_PATH = f"{BASE_DIR}/db/test.db"

DEFEAULT_HEADERS = {"User-Agent": "Mozilla/5.0"}

REQUEST_TIMEOUT = 10

ENCODING = "utf-8"

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "local-admin")