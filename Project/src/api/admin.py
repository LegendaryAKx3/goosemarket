from flask import jsonify, request
from database import get_supabase
from tags import get_or_create_tag
from typing import List, Dict, Any, Optional
def get_unapproved_polls() -> List[Dict[str, Any]]:
    """
    Return all polls/tasks that are not approved yet
    (where the 'public' flag is false).

    Returns:
    {
        "polls": [
            {
                "id": <poll id>,
                "title": <title>,
                "description": <description>,
                "created_at": datetime,
                "ends_at": datetime, # This is nullable
                "creator": <user id>,
                "tags": ["tag1", "tag2", ...]
            }
        ]
    }
    """
    if not current_user_is_admin():
        return jsonify({"error": "User does not have permission to access admin functions"}), 400
    
    try:
        supabase = get_supabase()

        if not supabase:
            return jsonify({"error": "Database connection not available"}), 503

        result = (
            supabase
            .table("polls")
            .select("id, title, description, created_at, ends_at, creator")
            .eq("public", False)
            .eq("deleted", False)
            .order("created_at", desc=False)
            .execute()
        )
        polls = result.data

        if not polls:
            # No unapproved polls
            return jsonify({"polls": []}), 200

        poll_ids = [p["id"] for p in polls]
        poll_tags = (supabase.table("poll_tags").select("poll_id", "tag_id").in_("poll_id", poll_ids).execute()).data

        # Get all tag <-> tag id pairs
        tag_ids = list({row["tag_id"] for row in poll_tags})
        tag_rows = (supabase.table("tags").select("id", "name").in_("id", tag_ids).execute()).data
        tag_lookup = {t["id"]: t["name"] for t in tag_rows}

        poll_tags_map = {pid: [] for pid in poll_ids}
        for row in poll_tags:
            poll_id = row["poll_id"]
            tag_id = row["tag_id"]
            tag_name = tag_lookup.get(tag_id)
            if tag_name:
                #Add all tags to each poll
                poll_tags_map[poll_id].append(tag_name)
        
        for poll in polls:
            poll["tags"] = poll_tags_map.get(poll["id"], [])

        return jsonify({"polls": result.data}), 200
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

def approve_poll():
    """
    Set public = True for the poll with the given id.
    Raises ValueError if no poll is found.

    Expected JSON:
    {
        "poll_id": <id>
    }
    """
    if not current_user_is_admin():
        return jsonify({"error": "User does not have permission to access admin functions"}), 400
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        poll_id = data.get("poll_id")

        try:
            poll_id = int(poll_id)
        except (ValueError, TypeError):
            return jsonify({"error": "Poll ID must be a valid integer"}), 400

        supabase = get_supabase()

        if not supabase:
            return jsonify({"error": "Database connection not available"}), 503

        response = (
            supabase
            .table("polls")
            .update({"public": True})
            .eq("id", poll_id)
            .execute()
        )
        if not response.data:
            return jsonify({"error": f"No poll found with id {poll_id}"}), 404
        
        return jsonify({"message": "Succesfully approved poll"}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


def update_poll() -> None:
    """
    Update fields of a poll (e.g. title, description, ends_at).
    Only fields that are not None will be updated.
    Raises ValueError if no poll is found or no fields are provided.

    Expected JSON: 
    {
        "poll_id": <id>,
        "title": <Title>, # Optional
        "description": <desc>, # Optional
        "tags": ["tag1", "tag2", ...] # Optional
        "ends_at": datetime, # Optional
    }
    """
    if not current_user_is_admin():
        return jsonify({"error": "User does not have permission to access admin functions"}), 400

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        poll_id = data.get("poll_id")

        #Validate poll id
        if not poll_id:
            return jsonify({"error": "Poll ID is a required field"}), 400

        try:
            poll_id = int(poll_id)
        except:
            return jsonify({"error": "Poll ID must be a valid integer"}), 400

        supabase = get_supabase()

        if not supabase:
            return jsonify({"error": "Database connection not available"}), 503

        title = data.get("title")
        desc = data.get("description")
        ends_at = data.get("ends_at")
        # Update Tags
        incoming_tags = data.get("tags", [])  # ["sports", "hockey", ...]
        incoming_tags = [t.strip() for t in incoming_tags if t.strip()]

        incoming_tag_ids = { get_or_create_tag(name, supabase) for name in incoming_tags }

        current_rows = supabase.table("poll_tags")\
            .select("tag_id")\
            .eq("poll_id", poll_id)\
            .execute()

        current_tag_ids = {row["tag_id"] for row in current_rows.data}

        to_add = incoming_tag_ids - current_tag_ids
        to_remove = current_tag_ids - incoming_tag_ids

        for tag_id in to_add:
            supabase.table("poll_tags").insert({"poll_id": poll_id, "tag_id": tag_id}).execute()

        for tag_id in to_remove:
            supabase.table("poll_tags")\
                .delete()\
                .eq("poll_id", poll_id)\
                .eq("tag_id", tag_id)\
                .execute()

        updates = {}
        if title is not None:
            updates["title"] = title.strip()

        if desc is not None:
            updates["description"] = desc.strip()

        if ends_at is not None:
            updates["ends_at"] = ends_at

        if not updates:
            return jsonify({"message": "No attributes to update"}), 200

        response = (
            supabase
            .table("polls")
            .update(updates)
            .eq("id", poll_id)
            .execute()
        )

        if not response.data:
            return jsonify({"error": f"No poll found with id {poll_id}"}), 400

        return jsonify({"message": f"Successfully updated {poll_id}"}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


def reject_poll():
    """Removes an unapproved poll from the database
    Expected JSON:
    {
        "poll_id": <id>
    }
    """

    if not current_user_is_admin():
        return jsonify({"error": "User does not have permission to access admin functions"}), 400

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        poll_id = data.get("poll_id")

        #Validate poll id
        if not poll_id:
            return jsonify({"error": "Poll ID is a required field"}), 400

        try:
            poll_id = int(poll_id)
        except:
            return jsonify({"error": "Poll ID must be a valid integer"}), 400

        supabase = get_supabase()

        if not supabase:
            return jsonify({"error": "Database connection not available"}), 503
        
        response = supabase.table("polls").update({"deleted": True}).eq("id", poll_id).eq("public", False).execute()

        if not response:
            return jsonify({"error": "Failed to delete poll"}), 500

        return jsonify({"message": "Successfully deleted poll"}), 200
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


def current_user_is_admin():
    """Internal function that returns True if the current user is an admin
    Used as a safeguard to ensure regular users cannot access admin functions"""
    token = request.cookies.get("sb-access-token")
    if not token:
        # Shouldn't ever happen, but means user isn't logged in
        return False
    
    supabase = get_supabase()
    if not supabase:
        return False
    
    try:
        claims = supabase.auth.get_user(token)
    except Exception:
        return False
    
    if not claims or not claims.user:
        return False
    
    userId = claims.user.id

    profile = supabase.table("profiles").select("admin").eq("auth_id", userId).single().execute()
    if profile.data and profile.data["admin"] is True:
        return True
    
    return False