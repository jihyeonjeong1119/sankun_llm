from fastapi import FastAPI, Request
from app.api.endpoints.llm import router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# FastAPI 앱 생성
app = FastAPI(
    title="Sankun LLM API",
    description="API for LLM functionalities including validation, RAG, and verification.",
    version="1.0.0"
)
# 라우터 등록
app.include_router(router, prefix="/api", tags=["Validation"])


# 루트 엔드포인트


######## 화면 테스트용

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
