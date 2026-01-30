from pydantic import BaseModel, Field
from typing import Optional


class Creative(BaseModel):
    text: str = Field(..., max_length=100)
    cta: str
    music_id: Optional[str] = None


class AdPayload(BaseModel):
    campaign_name: str = Field(..., min_length=3)
    objective: str
    creative: Creative
