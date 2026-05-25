from src.memory import get_last_context

FOLLOWUP_WORDS = [
    "eligibility",
    "package",
    "packages",
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

def contains_company(query):

    query = query.lower()

    for company in COMPANIES:

        if company in query:
            return True

    return False

def rewrite_query(query):

    query = query.strip().lower()

    last_context = get_last_context()

    # ---------------------------------------------------
    # COMPANY QUERY
    # ---------------------------------------------------

    if contains_company(query):

        return query

    # ---------------------------------------------------
    # PACKAGE FOLLOW-UP
    # ---------------------------------------------------

    if "highest package" in query or "high package" in query:

        return "companies with highest packages"

    if "avg package" in query or "average package" in query:

        return "average packages of all companies"

    # ---------------------------------------------------
    # SHORT FOLLOW-UP
    # ---------------------------------------------------

    if len(query.split()) <= 2:

        if last_context:

            # SMART REPLACEMENT

            if "package" in query:

                return query

            return f"{last_context} {query}"

    # ---------------------------------------------------
    # NORMAL QUERY
    # ---------------------------------------------------

    return query