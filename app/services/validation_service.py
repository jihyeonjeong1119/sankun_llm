import os

import vertexai
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import HarmBlockThreshold, HarmCategory
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_vertexai import ChatVertexAI



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

model = "gemini-1.5-flash-001"

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

llm = ChatVertexAI(model_name=model, **model_kwargs)

# 대화 메모리 초기화
memory = ConversationBufferMemory()

# LangChain 대화 체인 생성
conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
)

# 첫 번째 질문
response_1 = conversation_chain.run("안녕하세요? 건축현장에 대해 알고싶어요")
print("Response 1:", response_1)

# 두 번째 질문 (연속된 질문)
response_2 = conversation_chain.run("제 이전 질문이 뭐였죠?")
print("Response 2:", response_2)

# 메모리 상태 확인
print("\n--- Conversation Memory ---")
print(memory.buffer)