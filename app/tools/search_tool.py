from vertexai.generative_models import grounding, Tool


def get_search_tool() -> Tool:
    """검색 도구를 초기화."""
    google_search = grounding.GoogleSearchRetrieval()
    return Tool.from_google_search_retrieval(google_search)
