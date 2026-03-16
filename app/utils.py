import random
import string
from datetime import datetime

from .config import BASE_DIR


def html_path(filename: str) -> str:
    return str(BASE_DIR / filename)


def generate_captcha_text(length: int = 5) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
