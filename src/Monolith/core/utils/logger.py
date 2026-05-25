import logging
from pathlib import Path

from core.utils.paths import find_project_root

# ── LOG DIRECTORY ──────────────────────────────────────────────
PROJECT_ROOT = find_project_root("main.py")

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "monolith.log"

# ── LOGGER CONFIGURATION ───────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("monolith")