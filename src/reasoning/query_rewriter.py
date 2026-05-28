from src.memory.memory import get_last_query

def rewrite_query(query):

    query = query.strip()

    lower_query = query.lower()

    # -----------------------------------------
    # FOLLOW-UP SHORT QUERIES
    # -----------------------------------------

    short_followups = [
        "package",
        "salary",
        "cgpa",
        "cutoff",
        "backlog",
        "offers",
        "eligibility",
        "what about",
        "in tcs",
        "in amazon",
        "in google"
    ]

    # -----------------------------------------
    # ONLY USE MEMORY
    # FOR VERY SHORT QUERIES
    # -----------------------------------------

    if len(query.split()) <= 3:

        for word in short_followups:

            if word in lower_query:

                previous_query = get_last_query()

                if previous_query:

                    return (
                        previous_query
                        + " "
                        + query
                    )

    # -----------------------------------------
    # OTHERWISE RETURN ORIGINAL QUERY
    # -----------------------------------------

    return query