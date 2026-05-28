from src.generation.llm import get_llm
from src.generation.prompts import ANSWER_PROMPT


def generate_answer(query, context):

    llm = get_llm()

    prompt = ANSWER_PROMPT.format(
        context=context,
        query=query
    )

    response = llm.invoke(prompt)

    return response.content