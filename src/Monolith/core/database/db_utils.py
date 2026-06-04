# database.py
import os
from supabase import create_client, Client

# Initialize Supabase Client
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_records(
    search_query: str = "",
    record_type: str = "All Types",
    country: str = "All Countries",
):
    """
    Fetches records from Supabase applying database-level filters and search queries.
    """
    # Start base query selecting your table columns
    query = supabase.table("records").select(
        "ref_number, type, name_title, country, added_by, date_added"
    )

    # 1. Apply Dropdown Filters
    if record_type != "All Types":
        query = query.eq("type", record_type)

    if country != "All Countries":
        query = query.eq("country", country)

    # 2. Apply Global Search (matches reference number OR title)
    if search_query.strip():
        # Text search or simple ilike matching
        search_str = f"%{search_query}%"
        query = query.or_(
            f"ref_number.ilike.{search_str},name_title.ilike.{search_str}"
        )

    # 3. Sort by newest added
    query = query.order("date_added", descending=True)

    try:
        response = query.execute()
        return response.data  # Returns a list of dictionaries
    except Exception as e:
        print(f"Database error: {e}")
        return []
