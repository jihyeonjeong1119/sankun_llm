from pydantic import BaseModel

class QuestionRequest(BaseModel):
    text: str

class AnswerRequest(BaseModel):
    question: str