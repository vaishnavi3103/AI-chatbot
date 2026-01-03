from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    status: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
