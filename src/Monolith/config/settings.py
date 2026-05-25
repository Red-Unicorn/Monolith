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

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")

APP_NAME: str = "Monolith"
APP_VERSION: str = "1.0.0"

MAX_DESCRIPTION_LENGTH: int = 200
