# llm.py

def llama_prompt(user_input: str, state: dict) -> dict:
    """
    Rule-driven conversational controller.
    This simulates LLM structured output.
    """

    if not state["campaign_name"]:
        return {
            "agent_message": "What is your campaign name?",
            "reasoning": "Campaign name is required and must be at least 3 characters.",
            "next_expected_field": "campaign_name",
            "conversation_state": state
        }

    if not state["objective"]:
        return {
            "agent_message": "What is your campaign objective? (Traffic or Conversions)",
            "reasoning": "Objective determines music requirements and submission rules.",
            "next_expected_field": "objective",
            "conversation_state": state
        }

    if not state["text"]:
        return {
            "agent_message": "Enter ad text (max 100 characters)",
            "reasoning": "Ad text is mandatory and limited by TikTok Ads policy.",
            "next_expected_field": "text",
            "conversation_state": state
        }

    if not state["cta"]:
        return {
            "agent_message": "Enter CTA (e.g., Shop Now, Learn More)",
            "reasoning": "CTA is required to drive user action.",
            "next_expected_field": "cta",
            "conversation_state": state
        }

    if state["music_choice"] is None:
        return {
            "agent_message": "Choose music option (existing / upload / none)",
            "reasoning": (
                "Music is optional for Traffic campaigns "
                "but mandatory for Conversion campaigns."
            ),
            "next_expected_field": "music_choice",
            "conversation_state": state
        }

    return {
        "agent_message": "All inputs collected. Ready to submit.",
        "reasoning": "All required fields and business rules are satisfied.",
        "next_expected_field": None,
        "conversation_state": state
    }
