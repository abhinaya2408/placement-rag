def extract_sources(docs):

    sources = []

    seen = set()

    for doc in docs:

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        source = f"Page {page}"

        if source not in seen:

            seen.add(source)

            sources.append(source)

    return sources