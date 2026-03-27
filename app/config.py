from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "farmfresh.db"

ADMIN_USERNAME = "abhisheksajjan5@gmail.com"
ADMIN_PASSWORD = "admin123"
ADMIN_TOKEN = "admin-token"

JWT_SECRET = "change-this-secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60
