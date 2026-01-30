def validate_music(objective: str, music_choice: str):
    if music_choice == "none" and objective == "Conversions":
        return False, {
            "error": "Music required",
            "explanation": "Conversion campaigns require background music.",
            "suggested_action": "Upload music or choose existing music."
        }
    return True, None
