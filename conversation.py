# conversation.py
# In-memory conversation store (single-session demo)

conversation_state = {
    "conversation_id": "conv_001",

    # Required fields
    "campaign_name": None,   # min 3 chars
    "objective": None,       # Traffic | Conversions
    "text": None,            # max 100 chars
    "cta": None,             # required

    # Music logic
    "music_choice": None,    # existing | upload | none
    "music_id": None         # required unless music_choice = none
}


def missing_fields():
    """
    Returns a list of missing or invalid required fields
    (used by /submit for clear error messaging)
    """
    missing = []

    # Campaign name validation
    if not conversation_state["campaign_name"]:
        missing.append("campaign_name")
    elif len(conversation_state["campaign_name"]) < 3:
        missing.append("campaign_name (min 3 chars)")

    # Objective validation
    if not conversation_state["objective"]:
        missing.append("objective")

    # Ad text validation
    if not conversation_state["text"]:
        missing.append("text")
    elif len(conversation_state["text"]) > 100:
        missing.append("text (max 100 chars)")

    # CTA validation
    if not conversation_state["cta"]:
        missing.append("cta")

    # Music choice validation
    if conversation_state["music_choice"] is None:
        missing.append("music_choice")

    # Music ID required unless explicitly 'none'
    if (
        conversation_state["music_choice"] in ["existing", "upload"]
        and not conversation_state["music_id"]
    ):
        missing.append("music_id")

    return missing


def is_complete():
    """
    Final guard before submission
    Enforces business rules
    """

    # Basic completeness & validation
    if missing_fields():
        return False

    # Business rule: Conversions MUST have music
    if (
        conversation_state["objective"] == "Conversions"
        and conversation_state["music_choice"] == "none"
    ):
        return False

    return True


def reset_conversation():
    """
    Resets conversation safely
    (prevents stale state bugs between sessions)
    """
    conversation_state["campaign_name"] = None
    conversation_state["objective"] = None
    conversation_state["text"] = None
    conversation_state["cta"] = None
    conversation_state["music_choice"] = None
    conversation_state["music_id"] = None
