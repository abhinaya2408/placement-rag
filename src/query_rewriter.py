from src.memory import get_last_context

FOLLOWUP_WORDS = [
    "eligibility",
    "package",
    "backlogs",
    "bond",
    "rounds",
    "salary",
    "cgpa"
]

def rewrite_query(query):

    query = query.strip()

    last_context = get_last_context()

    # FOLLOW-UP QUERY DETECTION

    if (
        len(query.split()) <= 3
        or query.lower() in FOLLOWUP_WORDS
    ):

        if last_context:

            return f"{last_context} {query}"

    return query