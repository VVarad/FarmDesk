from dotenv import load_dotenv
from supabase_client import get_supabase

load_dotenv()

def clean_surveys():
    supabase = get_supabase()
    try:
        # Delete all survey entries
        response = supabase.table('survey_entries').delete().neq('id', 0).execute()
        print(f"Successfully deleted all test survey entries.")
    except Exception as e:
        print(f"Error cleaning survey entries: {e}")

if __name__ == '__main__':
    clean_surveys()
