from fastapi import FastAPI
from app.api.endpoints import llm

app = FastAPI(
    title="Sankun LLM API",
    description="API for LLM functionalities including validation, RAG, and verification.",
    version="1.0.0"
)

# 라우터 포함
app.include_router(llm.router, prefix="/questions", tags=["Questions"])

# 루트 엔드포인트
@app.get("/")
async def read_root():
    return {"message": "Welcome to Sankun LLM API"}