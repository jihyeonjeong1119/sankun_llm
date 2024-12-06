from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.models.response_models import ValidationResponse
from app.services.main_service import handle_request

# APIRouter 생성
router = APIRouter()


class ValidationResponse(BaseModel):
    is_valid: bool
    reason: str | None
    answer: str | None


@router.get("/handle_request", response_model=ValidationResponse)
async def validate_question_endpoint(question: str = Query(..., description="검증할 질문을 입력하세요"),
                                     session_id: str = Query(..., description="세션 ID를 입력하세요"),
                                     user_id: str = Query(..., description="사용자 ID를 입력하세요"),
                                     user_name: str = Query(..., description="사용자 이름을 입력하세요"),
                                     company_name: str = Query(..., description="회사 이름을 입력 하세요")):
    response = handle_request(question, session_id, user_id, user_name, company_name)
    # if not is_valid:
    #     raise HTTPException(status_code=400, detail=reason)
    return ValidationResponse(is_valid=True, reason=None, answer=response)
