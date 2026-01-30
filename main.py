# main.py
from fastapi import FastAPI, HTTPException
from conversation import conversation_state, missing_fields, is_complete
from llm import llama_prompt
from rules import validate_music
from tiktok_api import validate_music_id, upload_music, submit_ad
from schemas import AdPayload

app = FastAPI(title="TikTok AI Ads Agent", version="0.1.5")

ACCESS_TOKEN = "mock_access_token"


@app.post("/chat")
def chat(user_input: str):
    """
    Step-by-step conversational slot filling with validation
    """

    # 1️⃣ Ask LLM what field is expected next
    agent_response = llama_prompt(user_input, conversation_state)
    field = agent_response["next_expected_field"]

    # 2️⃣ Assign user input to the expected field
    if field:
        if field == "campaign_name":
            if len(user_input.strip()) < 3:
                raise HTTPException(
                    status_code=400,
                    detail="Campaign name must be at least 3 characters."
                )
            conversation_state["campaign_name"] = user_input.strip()

        elif field == "objective":
            if user_input not in ["Traffic", "Conversions"]:
                raise HTTPException(
                    status_code=400,
                    detail="Objective must be 'Traffic' or 'Conversions'."
                )
            conversation_state["objective"] = user_input

        elif field == "text":
            if len(user_input) > 100:
                raise HTTPException(
                    status_code=400,
                    detail="Ad text exceeds 100 characters."
                )
            conversation_state["text"] = user_input.strip()

        elif field == "cta":
            if not user_input.strip():
                raise HTTPException(
                    status_code=400,
                    detail="CTA cannot be empty."
                )
            conversation_state["cta"] = user_input.strip()

    # 3️⃣ Return structured response
    return {
        "agent_message": agent_response["agent_message"],
        "reasoning": agent_response.get(
            "reasoning",
            "Guides the user to provide missing fields in order."
        ),
        "next_expected_field": field,
        "conversation_state": conversation_state
    }


@app.post("/music")
def music(choice: str, music_id: str | None = None):
    """
    Handles music logic: existing / upload / none
    """

    choice_lower = choice.lower()
    conversation_state["music_choice"] = choice_lower

    if choice_lower == "existing":
        if not music_id:
            raise HTTPException(
                status_code=400,
                detail="music_id is required for existing music."
            )

        ok, err = validate_music_id(music_id)
        if not ok:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": err["error"],
                    "suggested_action": err["suggested_action"]
                }
            )

        conversation_state["music_id"] = music_id
        return {"music_status": "selected", "music_id": music_id}

    elif choice_lower == "upload":
        mid = upload_music()
        conversation_state["music_id"] = mid
        return {"music_status": "uploaded", "music_id": mid}

    elif choice_lower == "none":
        # Only allowed if objective is Traffic
        if conversation_state["objective"] == "Conversions":
            raise HTTPException(
                status_code=400,
                detail="Cannot select 'none' music for Conversions objective."
            )
        conversation_state["music_id"] = None
        return {"music_status": "none"}

    raise HTTPException(status_code=400, detail="Invalid music choice.")


@app.post("/submit")
def submit():
    """
    Validates conversation state and submits the ad payload.
    """

    # 1️⃣ Check missing fields
    missing = missing_fields()
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Missing required fields",
                "missing_fields": missing
            }
        )

    # 2️⃣ Enforce music business rules before submission
    ok, err = validate_music(
        conversation_state["objective"],
        conversation_state["music_choice"]
    )
    if not ok:
        raise HTTPException(
            status_code=400,
            detail={
                "error": err[0],
                "suggestion": err[1]
            }
        )

    # 3️⃣ Build validated payload
    payload = AdPayload(
        campaign_name=conversation_state["campaign_name"],
        objective=conversation_state["objective"],
        creative={
            "text": conversation_state["text"],
            "cta": conversation_state["cta"],
            "music_id": conversation_state["music_id"]
        }
    )

    # 4️⃣ Submit to TikTok API (mocked)
    result = submit_ad(payload.dict(), ACCESS_TOKEN)

    # 5️⃣ Interpret API failures
    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail={
                "error": result["error"],
                "suggestion": result.get("suggested_action"),
                "retry": result.get("retry_possible", False)
            }
        )

    return result
