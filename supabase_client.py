import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

supabase: Client | None = None

if url and key:
    supabase = create_client(url, key)

def get_supabase() -> Client:
    if not supabase:
        raise ValueError("Supabase URL or Key not set. Please set SUPABASE_URL and SUPABASE_KEY in .env")
    return supabase
