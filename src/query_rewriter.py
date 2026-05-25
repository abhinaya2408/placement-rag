def rewrite_query(query):

    query = query.strip()

    if len(query.split()) < 3:

        return f"Explain in detail about {query}"

    return query