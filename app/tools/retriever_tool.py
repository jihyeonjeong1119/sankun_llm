from vertexai.generative_models import grounding, Tool
from typing import Optional
from langchain_google_community import VertexAISearchRetriever
from langchain.tools.retriever import create_retriever_tool
from app.common.vertex_ai_setup import get_agent
from app.tools.search_tool import get_search_tool


def get_retriever_tool(data_store_id: str, tool_name: str, description: str) -> (VertexAISearchRetriever, Tool):
    retriever = VertexAISearchRetriever(
        project_id="sankun-df577",
        data_store_id=data_store_id,
        location_id="global",
        engine_data_type=1,
        max_documents=5,
    )
    tool = create_retriever_tool(
        retriever=retriever,
        name=tool_name,
        description=description
    )
    return retriever, tool


def get_data_search_tool(question: str, memory, user_profile=None) -> str:
    company_retriever, company_tool = get_retriever_tool("ds-cpn-master_1731904786984", "company_tool",
                                                         "회사 정보를 검색하는 도구입니다. 회사 관련 질문에만 사용하세요.")
    site_retriever, site_tool = get_retriever_tool("ds-site-master_1731904876362", "site_tool",
                                                   "건설 현장 정보를 검색하는 도구입니다. 현장 관련 질문에만 사용하세요.")
    project_retriever, project_tool = get_retriever_tool("ds-cpn-project_1731904843260", "project_tool",
                                                         "건설 수주, 프로젝트 정보를 검색하는 도구입니다. 수주, 프로젝트 관련 질문에만 사용하세요.")
    bid_retriever, bid_tool = get_retriever_tool("ds-bid-master_1731904756784", "bid_tool",
                                                 "건설 입찰 정보를 검색하는 도구입니다. 입찰 관련 질문에만 사용하세요.")
    news_retriever, news_tool = get_retriever_tool("ds-news-detail_1731904958755", "news_tool",
                                                   "건설 뉴스 정보를 검색하는 도구입니다. 뉴스 관련 질문에만 사용하세요.")

    retrieved_docs_company = company_retriever.get_relevant_documents(question)
    retrieved_docs_site = site_retriever.get_relevant_documents(question)
    retrieved_docs_project = project_retriever.get_relevant_documents(question)
    retrieved_docs_bid = bid_retriever.get_relevant_documents(question)
    retrieved_docs_news = news_retriever.get_relevant_documents(question)

    decode_and_display_results(retrieved_docs_company)
    decode_and_display_results(retrieved_docs_site)
    decode_and_display_results(retrieved_docs_project)
    decode_and_display_results(retrieved_docs_bid)
    decode_and_display_results(retrieved_docs_news)

    agent = get_agent(
        model_name="gemini-1.5-flash-001",
        tools=[site_tool, company_tool],
        chat_history=lambda: memory.chat_memory,
        max_output_tokens=500,  # 충분히 상세한 응답을 제공
        temperature=0.0
    )
    response = agent.query(input=question)
    if memory.chat_memory.messages:
        last_message = memory.chat_memory.messages[-1]  # 마지막 메시지 가져오기
        print("Last Response from History:", last_message)
    else:
        print("No messages found in history.")
    classification = response.get('output', '').strip()
    return classification


import json


def decode_and_display_results(results):
    """
    Decode and display multiple results in a human-readable format.

    Args:
        results (list): List of retrieved documents.

    Returns:
        list: Decoded results in a readable format.
    """
    if not results:
        print("No results found.")
        return []

    decoded_results = []
    for idx, result in enumerate(results):
        try:
            # Decode the JSON content from page_content
            page_content = json.loads(result.page_content)
            answer = page_content.get("answer", "No answer available.")
            question_text = page_content.get("question", "No question available.")
            metadata = result.metadata
            # Display the result
            print(f"Result {idx + 1}:")
            print(f"  - Question: {question_text}")
            print(f"  - Answer: {answer}")
            print(f"  - Metadata: {metadata}\n")
            # Store the result in a structured format
            decoded_results.append({
                "question": question_text,
                "answer": answer,
                "metadata": metadata
            })
        except json.JSONDecodeError:
            print(f"Result {idx + 1}: Unable to decode page_content.")
            print(f"  - Raw Content: {result.page_content}")
            print(f"  - Metadata: {result.metadata}\n")
            decoded_results.append({
                "question": "Decoding failed",
                "answer": result.page_content,
                "메타데이터": result.metadata
            })

    return decoded_results
