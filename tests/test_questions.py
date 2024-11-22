from fastapi.testclient import TestClient
from app.main import app
from app.services.validation_service import validate_question

client = TestClient(app)

def test_validate_question_success():
    # question = "서울시 아파트 공사 현장은 어떤게 있을까?";
    # is_valid, reason = validate_question(question);
    # assert is_valid == True

    # question1 = "서울시 아파트 공사 현황을 알려줘."
    # success, response1, memory = validate_question(question1)
    # print(response1)
    #
    # # 두 번째 질문 (메모리 전달)
    # question2 = "그 중 가장 큰 프로젝트는 무엇이야?"
    # success, response2, memory = validate_question(question2, memory)
    # print(response2)
    # 연속된 질문 처리

    while True:
        question = input("사용자: ")
        valid, answer, conversation_chain = validate_question(question, conversation_chain)
        print(f"AI 어시스턴트: {answer}")

#
# def test_validate_question_failure():
#     response = client.post("/questions/validate", json={"text": ""})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Question cannot be empty."


