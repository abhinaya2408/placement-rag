from src.memory import get_last_context

FOLLOWUP_WORDS = [
    "eligibility",
    "package",
    "backlogs",
    "bond",
    "rounds",
    "salary",
    "cgpa",
    "interview",
    "criteria"
]

COMPANIES = [
    "amazon",
    "tcs",
    "infosys",
    "google",
    "microsoft",
    "wipro",
    "flipkart"
]

def is_followup_query(query):

    query = query.lower().strip()

    # VERY SHORT QUERY

    if len(query.split()) <= 2:
        return True

    # FOLLOWUP WORDS

    for word in FOLLOWUP_WORDS:

        if word in query:
            return True

    return False

def contains_company(query):

    query = query.lower()

    for company in COMPANIES:

        if company in query:
            return True

    return False

def rewrite_query(query):

    query = query.strip()

    last_context = get_last_context()

    # IF QUERY ALREADY HAS COMPANY
    # DO NOT APPEND OLD CONTEXT

    if contains_company(query):

        return query

    # FOLLOWUP DETECTION

    if is_followup_query(query):

        if last_context:

            return f"{last_context} {query}"

    # NEW TOPIC DETECTED

    return query