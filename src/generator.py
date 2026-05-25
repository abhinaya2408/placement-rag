from src.prompts import SYSTEM_PROMPT
from src.llm import generate_llm_response

def generate_answer(query, context):

    prompt = f"""
    {SYSTEM_PROMPT}

    Context:
    {context}

    Question:
    {query}
    """

    response = generate_llm_response(prompt)

    return response