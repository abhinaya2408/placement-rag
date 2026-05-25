from src.prompts import SYSTEM_PROMPT
from src.llm import generate_llm_response

def generate_answer(query, context):

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:
{context}

User Question:
{query}

Generate a professional answer strictly from the retrieved context.
"""

    response = generate_llm_response(prompt)

    return response