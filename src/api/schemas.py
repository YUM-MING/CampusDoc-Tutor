from pydantic import BaseModel
from typing import List, Optional

class AskRequest(BaseModel):
    question: str

class Citation(BaseModel):
    content: str
    source: str
    page: Optional[int] = None

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
