## TikTok Ads Creation via AI Agent

## Purpose of This Project

This project demonstrates how to build a reasoning-first AI agent that helps a user create a TikTok Ad configuration through conversation.

## flowchart TD
    === User Interaction ===
    User[User Input / Commands] -->|POST /chat| Main[main.py<br/>FastAPI Orchestration]

    === main.py orchestrates everything ===
    Main --> Conversation[conversation.py<br/>Conversation State & Guards]
    Main --> LLM[llm.py<br/>Next Field Prompting]
    Main --> Rules[rules.py<br/>Business Rule Validation]
    Main --> TikTok[tiktok_api.py<br/>TikTok API Mock]
    Main --> Schemas[schemas.py<br/>Payload Validation]
    Main --> OAuth[oauth.py<br/>OAuth Token Handling]

    === Conversation logic ===
    Conversation -->|Store/Check fields| Main
    Conversation -->|Check completeness & missing fields| Rules

    === LLM prompt logic ===
    LLM -->|Determine next_expected_field| Main

    === Business rules ===
    Rules -->|Validate music, objective| Main
    Rules -->|Return error / suggestion| Main

    === TikTok API interaction ===
    TikTok -->|submit_ad, validate_music_id, upload_music| Main
    OAuth -->|Validate token, handle errors| TikTok

    === Payload validation ===
    Schemas -->|Validate AdPayload structure| Main

    === Final response to user ===
    Main -->|Structured JSON Response| User


### It focuses on:
- Prompt design with structured output
- Business rule enforcement
- External API reasoning
- Graceful handling of failures

#### What the Agent Does (High Level Flow)

1. Talks to the user step-by-step
2. Collects required ad inputs in the correct order
3. Applies TikTok business rules before submission
4. Builds a validated ad payload
5. Submits the ad (mocked TikTok Ads API)
6. Explains failures clearly and suggests fixes

### Features
- LLaMA-based conversational agent
- TikTok OAuth (mocked Authorization Code flow)
- Strict business rule enforcement
- Structured JSON output
- Robust API error interpretation

User
 ↓
/chat endpoint (conversation flow)
 ↓
conversation.py (state + guards)
 ↓
llm.py (prompt logic)
 ↓
rules.py (business rules)
 ↓
/music endpoint (music handling)
 ↓
/submit endpoint
 ↓
tiktok_api.py (mocked TikTok Ads API)



### Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
