# tiktok_api.py

import uuid


def validate_music_id(music_id: str):
    if not music_id:
        return False, {
            "error": "Missing music ID",
            "explanation": "No music ID was provided.",
            "suggested_action": "Provide a music ID or choose another music option.",
            "retry_possible": False
        }

    if music_id.startswith("bad"):
        return False, {
            "error": "Invalid music ID",
            "explanation": "Music ID not found or unauthorized.",
            "suggested_action": "Provide a valid music ID or upload custom music.",
            "retry_possible": True
        }

    if music_id.startswith("geo"):
        return False, {
            "error": "Geo-restricted music",
            "explanation": "Music is not available in the selected region.",
            "suggested_action": "Select different music or remove music.",
            "retry_possible": True
        }

    return True, None


def upload_music():
    return f"music_{uuid.uuid4().hex[:8]}"


def submit_ad(payload: dict, token: str):

    if token != "mock_access_token":
        return {
            "error": "OAuth token expired",
            "explanation": "Access token is invalid, expired, or revoked.",
            "suggested_action": "Re-authenticate using OAuth.",
            "retry_possible": True
        }

    if payload.get("campaign_name") == "no_permission":
        return {
            "error": "Missing Ads permission",
            "explanation": "OAuth token does not have ads.write permission.",
            "suggested_action": "Reauthorize with ads.write scope.",
            "retry_possible": False
        }

    music_id = payload.get("creative", {}).get("music_id")
    if music_id and music_id.startswith("bad"):
        return {
            "error": "Invalid music ID",
            "explanation": "Music validation failed during submission.",
            "suggested_action": "Select or upload a different music track.",
            "retry_possible": True
        }

    return {
        "status": "success",
        "ad_id": "ad_123456",
        "submitted_payload": payload
    }
