from dotenv import load_dotenv
from pathlib import Path
from core.utils.paths import find_project_root


def load_environment():
    """
    Loads .env from project root using deterministic path resolution.
    """
    project_root = find_project_root("main.py")
    env_path = project_root / ".env"

    if env_path.exists():
        load_dotenv(env_path)
    else:
        raise FileNotFoundError(f".env not found at {env_path}")