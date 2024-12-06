import os
from langchain_google_vertexai import ChatVertexAI
from vertexai.generative_models import Tool
from vertexai.preview import reasoning_engines
from vertexai import init
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain.memory import ConversationBufferMemory

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/junhyukkang/Desktop/DEV/sankun-df577-5ef289163f0b.json"

# Vertex AI 초기화
init(
    project=os.getenv("GCP_PROJECT", "sankun-df577"),
    staging_bucket=os.getenv("GCP_BUCKET", "gs://sankun_llm_data"),
    location=os.getenv("GCP_LOCATION", "us-central1"),
)

DEFAULT_MODEL = "gemini-1.5-flash-001"

safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}


def get_agent(
        model_name=DEFAULT_MODEL,
        tools=None,
        chat_history=None,
        **kwargs
):
    """
    Langchain Agent 생성 및 반환.

    Args:
        model_name (str): 사용할 모델 이름. 기본값은 `DEFAULT_MODEL`.
        tools (list): 사용할 도구 리스트. 기본값은 빈 리스트.
        chat_history: 대화 히스토리. 기본값은 `None`.
        **kwargs: 모델 파라미터.

    Returns:
        Langchain Agent
    """
    model_kwargs = {
        "temperature": kwargs.get("temperature", 0.28),
        "max_output_tokens": kwargs.get("max_output_tokens", 1000),
        "top_p": kwargs.get("top_p", 0.95),
        "top_k": kwargs.get("top_k", None),
        "safety_settings": kwargs.get("safety_settings", safety_settings),
    }

    # LangchainAgent 생성
    return reasoning_engines.LangchainAgent(
        model=model_name,
        tools=tools or [],  # 기본 도구 설정
        model_kwargs=model_kwargs,
        chat_history=chat_history,  # 대화 히스토리 설정
    )
