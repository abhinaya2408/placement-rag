def generate_citations(docs):

    citations = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown Source"
        )

        if source not in citations:

            citations.append(source)

    return citations


def extract_sources(docs):

    sources = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "Unknown Source"
        )

        if source not in sources:

            sources.append(source)

    return sources