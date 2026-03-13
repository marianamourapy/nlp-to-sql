import logging
from pathlib import Path
from core.config import DEBUG_MODE

LOG_LEVEL = logging.DEBUG if DEBUG_MODE else logging.WARNING
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(LOG_DIR / "app_log", encoding="utf-8")
file_handler.setFormatter(formatter)

logging.basicConfig(level=LOG_LEVEL, handlers=[console_handler, file_handler])


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)