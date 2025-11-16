import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SERVICE_ROLE_KEY")
    return create_client(url, key)

def get_unapproved_polls() -> List[Dict[str, Any]]:
    """
    Return all polls/tasks that are not approved yet
    (where the 'public' flag is false).
    """
    supabase = get_supabase()

    result = (
        supabase
        .table("polls")
        .select("id, title, description, created_at, ends_at, public")
        .eq("public", False)
        .order("created_at", desc=False)
        .execute()
    )
    return result.data or []

def approve_poll(poll_id: int) -> Dict[str, Any]:
    """
    Set public = True for the poll with the given id.
    Returns the updated poll row.
    Raises ValueError if no poll is found.
    """
    supabase = get_supabase()

    response = (
        supabase
        .table("polls")
        .update({"public": True})
        .eq("id", poll_id)
        .select("id, title, description, created_at, ends_at, public")
        .execute()
    )

    data = response.data or []
    if not data:
        raise ValueError(f"No poll found with id {poll_id}")

    return data[0]
