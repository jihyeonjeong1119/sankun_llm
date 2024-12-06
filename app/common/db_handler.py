import os
from psycopg import connect
from langchain_postgres import PostgresChatMessageHistory

# PostgreSQL 연결 정보
DB_USER = os.getenv("DB_USER", "postgres")  # PostgreSQL 사용자 이름
DB_PASSWORD = os.getenv("DB_PASSWORD", "Sankun365!")  # PostgreSQL 비밀번호
DB_HOST = os.getenv("DB_HOST", "34.121.122.234")  # PostgreSQL 호스트
DB_PORT = os.getenv("DB_PORT", "5432")  # PostgreSQL 포트
DB_NAME = os.getenv("DB_NAME", "langchain_memory")  # 데이터베이스 이름

conn_info = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_db_connection():
    """PostgreSQL 동기 연결 생성."""
    return connect(conn_info)


def initialize_chat_history(
    session_id: str,
    user_id: str,
    user_name: str,
    company_name: str,
    step_id: str,
    table_name: str = "chat_history",
):
    """PostgresChatMessageHistory 초기화."""
    connection = get_db_connection()
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        user_id,
        user_name,
        company_name,
        step_id,
        sync_connection=connection,
    )
