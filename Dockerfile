# 1. Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필요한 파일만 복사 (requirements.txt 먼저 복사하여 종속성 캐시 활용)
COPY requirements.txt .

# 4. 의존성 설치 (캐시 방지 옵션 포함)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 프로젝트 소스 파일 복사
COPY . .

# 6. 수정된 파일만 지정 경로에 덮어쓰기
COPY venv_python3.11/custom_libs/langchain_core/chat_history.py \
     /usr/local/lib/python3.11/site-packages/langchain_core/chat_history.py
COPY venv_python3.11/custom_libs/langchain_postgres/chat_message_histories.py \
     /usr/local/lib/python3.11/site-packages/langchain_postgres/chat_message_histories.py

# 7. 실행 시점에 필요한 환경 변수 설정 (필요시 추가)
ENV PYTHONUNBUFFERED=1

# 8. FastAPI 애플리케이션 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
