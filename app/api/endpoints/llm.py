from fastapi import APIRouter, HTTPException
from app.models.request_models import QuestionRequest
from app.models.response_models import ValidationResponse
from app.services.validation_service import validate_question

router = APIRouter()

@router.post("/validate", response_model=ValidationResponse)
async def validate_question_endpoint(question: QuestionRequest):
    is_valid, reason = validate_question(question.text)
    if not is_valid:
        raise HTTPException(status_code=400, detail=reason)
    return ValidationResponse(is_valid=True, reason=None)