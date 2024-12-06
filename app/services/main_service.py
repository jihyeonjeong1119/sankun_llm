from app.common.memory_handler import get_memory
from app.tools.retriever_tool import get_data_search_tool


def handle_request(question: str, session_id: str, user_id: str, user_name: str, company_name: str) -> str:
    memory = get_memory(session_id, user_id, user_name, company_name, "1")
    user_profile = {
        "company": company_name,
        "revenue": "500 billion KRW",
        "industry": "Civil Engineering and Plant Construction",
        "role": "Team Leader",
        "department": "Site Management",
        "recent_searches": ["Bidding success rate analysis", "Project risk management"]
    }
    response = get_data_search_tool(question, memory, user_profile)
    #
    # classification = validate_question(question, memory, user_profile)
    # # 분기 처리
    # if classification == "D":
    #     print("Accessing construction-specific RAG database for data retrieval...")
    # elif classification == "G":
    #     print("Accessing external resources for general question...")
    #     result = general_question(question, memory, user_profile)
    #     print(result)
    # elif classification == "T":
    #     print("Accessing Data ID for general question...")
    #     result = general_question(question, memory, user_profile)
    #     print(result)
    # else:
    #     print("Uncertain response. Re-analyzing the question...")
        # result = general_question(question, memory, user_profile)
        # print(result)
    # 결과 반환
    return response


# handle_request("산군은 어떤회사야?, company_id만 알려줘", "session_id_35", "1", "강준혁", "산군");
# handle_request("내 방금 질문은 뭐였어?", "session_id_3", "1", "강준혁", "산군");
