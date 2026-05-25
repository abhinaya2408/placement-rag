def extract_sources(docs):

    sources = []

    for doc in docs:

        page = doc.metadata.get(
            "page",
            "N/A"
        )

        sources.append(
            f"Page {page}"
        )

    return sources