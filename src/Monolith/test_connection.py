import os
from supabase import create_client
from core.utils.env import load_environment

# Load environment configuration securely from .env
load_environment()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY_OLD")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY_OLD must be set in the environment variables.")

supabase = create_client(url, key)

data = supabase.table("profiles").select("*").limit(1).execute()
print(data)
