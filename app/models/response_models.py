from pydantic import BaseModel
from typing import Optional

class ValidationResponse(BaseModel):
    is_valid: bool
    reason: Optional[str] = None

class AnswerResponse(BaseModel):
    answer: str