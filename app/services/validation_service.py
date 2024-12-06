from app.common.vertex_ai_setup import get_agent


def validate_question(question: str, memory, user_profile=None) -> str:
    profile_info = (
        f"User Profile:\n"
        f"- Company: {user_profile.get('company', 'N/A')}.\n"
        f"- Revenue: {user_profile.get('revenue', 'N/A')}.\n"
        f"- Industry: {user_profile.get('industry', 'N/A')}.\n"
        f"- Role: {user_profile.get('role', 'N/A')}.\n"
        f"- Department: {user_profile.get('department', 'N/A')}.\n"
        f"- Recent Searches: {user_profile.get('recent_searches', 'N/A')}.\n"
    ) if user_profile else "No user profile provided."
    prompt = f"""
        You are a construction-industry-specialized LLM trained to assist construction professionals. 
        Use the provided user profile to better understand the context of the question.
        
        {profile_info}
        
        Classify the user's question into one of the following types:
        
        1. "D" (Construction Data Needed): For questions that require access to construction-specific data, such as bidding details, project information, company performance, or construction industry news.  
           Example: "What is the bidding competition rate for this month?" or "Give me the latest project updates in the construction industry."
        
        2. "G" (General Question): For questions that can be answered using general knowledge or do not require specialized construction data.  
           Example: "What are the top construction trends in 2024?" or "How does inflation impact the construction sector."
        
        3. "T" (Data ID Lookup): For questions where the user only needs an ID for a specific entity (e.g., company, project, or person) to directly access more detailed information.  
           Example: "Can you recommend a construction company?" or "What is the representative's name for this company?"

        4. "E" (Error): For unclear questions or if the question cannot be classified into the above types.
        
        **Instructions**:
        - Respond with only one of the following letters: "D", "G", "T", or "E".
        - Do not provide explanations, context, or additional text.
        - Respond with just the letter corresponding to the classification.
        
        User Question: "{question}"
        """
    agent = get_agent(
        model_name="gemini-1.5-flash-001",
        tools=[],
        chat_history=lambda: memory.chat_memory,
        max_output_tokens=20,  # 짧은 판단 응답
        temperature=0.2  # 결정론적 응답
    )
    response = agent.query(input=prompt)  # 공백 제거
    classification = response.get('output', '').strip()
    return classification
