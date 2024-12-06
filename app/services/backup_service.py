import os
from typing import Optional

import vertexai
from langchain.tools.retriever import create_retriever_tool
from langchain_google_community import VertexAISearchRetriever
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from vertexai.generative_models import grounding, Tool
from vertexai.preview import reasoning_engines

vertexai.init(
    project="sankun-df577",
    staging_bucket="gs://sankun_llm_data",
    location="us-central1",
)

model = "gemini-1.5-flash-001"

safety_settings = {
    HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/junhyukkang/Desktop/DEV/sankun-df577-5ef289163f0b.json"

model_kwargs = {
    # temperature (float): The sampling temperature controls the degree of
    # randomness in token selection.
    "temperature": 0.28,
    # max_output_tokens (int): The token limit determines the maximum amount of
    # text output from one prompt.
    "max_output_tokens": 1000,
    # top_p (float): Tokens are selected from most probable to least until
    # the sum of their probabilities equals the top-p value.
    "top_p": 0.95,
    # top_k (int): The next token is selected from among the top-k most
    # probable tokens. This is not supported by all model versions. See
    # https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#valid_parameter_values
    # for details.
    "top_k": None,
    # safety_settings (Dict[HarmCategory, HarmBlockThreshold]): The safety
    # settings to use for generating content.
    # (you must create your safety settings using the previous step first).
    "safety_settings": safety_settings,
}

from langchain_postgres import PostgresChatMessageHistory
from langchain.memory import ConversationBufferMemory

# PostgreSQL 연결 정보
DB_USER = "postgres"  # PostgreSQL 사용자 이름
DB_PASSWORD = "Sankun365!"  # PostgreSQL 비밀번호
DB_HOST = "34.121.122.234"  # Cloud SQL Proxy 사용 시 localhost
DB_PORT = "5432"  # PostgreSQL 포트
DB_NAME = "langchain_memory"  # 데이터베이스 이름
conn_info = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# 연결 문자열 생성

# PostgresChatMessageHistory 초기화
session_id = 'session_id_10'  # 고유 세션 ID 생성
table_name = "chat_history"  # 사용할 테이블 이름

# 동기 연결 예제
from psycopg import connect

sync_connection = connect(conn_info)

# 테이블 생성 (최초 실행 시)
# PostgresChatMessageHistory.create_tables(sync_connection, table_name)

# PostgresChatMessageHistory 객체 생성
chat_history = PostgresChatMessageHistory(
    table_name,
    session_id,
    '1',
    '강준혁',
    '산군',
    '2',
    sync_connection=sync_connection,
)

# 메모리 구성

memory = ConversationBufferMemory(chat_memory=chat_history, return_messages=True)

def get_exchange_rate(
        currency_from: str = "USD",
        currency_to: str = "EUR",
        currency_date: str = "latest",
):
    """Retrieves the exchange rate between two currencies on a specified date.

    Uses the Frankfurter API (https://api.frankfurter.app/) to obtain
    exchange rate data.

    Args:
        currency_from: The base currency (3-letter currency code).
            Defaults to "USD" (US Dollar).
        currency_to: The target currency (3-letter currency code).
            Defaults to "EUR" (Euro).
        currency_date: The date for which to retrieve the exchange rate.
            Defaults to "latest" for the most recent exchange rate data.
            Can be specified in YYYY-MM-DD format for historical rates.

    Returns:
        dict: A dictionary containing the exchange rate information.
            Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24",
                "rates": {"EUR": 0.95534}}
    """
    import requests
    response = requests.get(
        f"https://api.frankfurter.app/{currency_date}",
        params={"from": currency_from, "to": currency_to},
    )
    return response.json()


def generate_and_execute_code(
        query: str,
        files: Optional[list[str]] = None,
        file_gcs_uris: Optional[list[str]] = None,
) -> str:
    """Get the results of a natural language query by generating and executing
    a code snippet.

    Example queries: "Find the max in [1, 2, 5]" or "Plot average sales by
    year (from data.csv)". Only one of `file_gcs_uris` and `files` field
    should be provided.

    Args:
        query:
            The natural language query to generate and execute.
        file_gcs_uris:
            Optional. URIs of input files to use when executing the code
            snippet. For example, ["gs://input-bucket/data.csv"].
        files:
            Optional. Input files to use when executing the generated code.
            If specified, the file contents are expected be base64-encoded.
            For example: [{"name": "data.csv", "contents": "aXRlbTEsaXRlbTI="}].
    Returns:
        The results of the query.
    """
    operation_params = {"query": query}
    if files:
        operation_params["files"] = files
    if file_gcs_uris:
        operation_params["file_gcs_uris"] = file_gcs_uris

    from vertexai.preview import extensions

    # If you have an existing extension instance, you can get it here
    # i.e. code_interpreter = extensions.Extension(resource_name).
    code_interpreter = extensions.Extension.from_hub("code_interpreter")
    return extensions.Extension.from_hub("code_interpreter").execute(
        operation_id="generate_and_execute",
        operation_params=operation_params,
    )


grounded_search_tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())

retriever = VertexAISearchRetriever(
    project_id="sankun-df577",
    data_store_id="ds-cpn-project_1731904843260",
    location_id="global",
    engine_data_type=1,
    max_documents=10,
)
company_search_tool = create_retriever_tool(
    retriever=retriever,
    name="search_companies",
    description="Searches information about construction companies in South Korea.",
)

agent = reasoning_engines.LangchainAgent(
    model=model,
    tools=[
        # get_exchange_rate,         # Optional (Python function)
        # grounded_search_tool,  # Optional (Grounding Tool)
        company_search_tool,         # Optional (Langchain Tool)
        # site_search_tool,
        # generate_and_execute_code, # Optional (Vertex Extension)
    ],
    model_kwargs=model_kwargs,
    chat_history=lambda: memory.chat_memory
)

response = agent.query(input="서울에 건설사 추천좀 해줄래?")
# 대화 히스토리에서 마지막 메시지 확인 (이번 응답)
if memory.chat_memory.messages:
    last_message = memory.chat_memory.messages[-1]  # 마지막 메시지 가져오기
    print("Last Response from History:", last_message)
else:
    print("No messages found in history.")

# 현재 세션의 대화 히스토리 확인
print(memory.chat_memory.messages)
