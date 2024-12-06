from langchain.memory import ConversationBufferMemory
from app.common.db_handler import initialize_chat_history


def get_memory(session_id: str, user_id: str, user_name: str, company_name: str, step_id: str):
    """ConversationBufferMemory 초기화."""
    chat_history = initialize_chat_history(session_id, user_id, user_name, company_name, step_id)
    return ConversationBufferMemory(chat_memory=chat_history, return_messages=True)

