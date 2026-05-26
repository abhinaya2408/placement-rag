from src.llm import get_llm


def generate_answer(query, context):

    # ---------------------------------------------------
    # EMPTY / WEAK CONTEXT CHECK
    # ---------------------------------------------------

    weak_phrases = [
        "difficulty:",
        "rag skill tested",
        "expected rag behaviour",
        "query:"
    ]

    lower_context = context.lower()

    weak_count = 0

    for phrase in weak_phrases:

        if phrase in lower_context:

            weak_count += 1

    # ---------------------------------------------------
    # STRICT FALLBACK
    # ---------------------------------------------------

    if len(context.strip()) < 100 or weak_count >= 2:

        return (
            "Information not available "
            "in uploaded documents."
        )

    # ---------------------------------------------------
    # LLM
    # ---------------------------------------------------

    llm = get_llm()

    prompt = f"""
You are a Placement RAG Assistant.

STRICT RULES:
1. Answer ONLY using provided context.
2. DO NOT use external knowledge.
3. DO NOT assume information.
4. If answer is unclear, say:
   "Information not available in uploaded documents."
5. Keep responses concise.
6. Use bullet points when possible.

QUESTION:
{query}

CONTEXT:
{context}

ANSWER:
"""

    response = llm.invoke(prompt)

    return response.content