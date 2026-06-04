"""
settings.py  –  Short Descriptive Title
==========================================
Application settings and environment loading.

Author  : Kevin JAMART / Red Unicorn
Version : 1.0.0
Python  : 3.12+
"""

from dotenv import load_dotenv
import os
from core.utils.logger import logger

load_dotenv()

SUPABASE_KEY = (os.getenv("SUPABASE_KEY_OLD") or "").strip()
SUPABASE_URL = (os.getenv("SUPABASE_URL") or "").strip()

logger.debug("Environment variables loaded successfully")

APP_NAME: str = "Monolith"
APP_VERSION: str = "1.0.0"

MAX_DESCRIPTION_LENGTH: int = 200

REGISTRY = {"countries": {}, "sectors": {}, "document_categories": {}, "file_types": {}}
