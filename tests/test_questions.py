from fastapi.testclient import TestClient
from app.main import app
from app.services.validation_service import validate_question

client = TestClient(app)

def test_validate_question_success():
    question = "서울시 아파트 공사 현장은 어떤게 있을까?";
    is_valid, reason = validate_question(question);
    assert is_valid == True
#
# def test_validate_question_failure():
#     response = client.post("/questions/validate", json={"text": ""})
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Question cannot be empty."


