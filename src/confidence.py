def calculate_confidence(docs):

    if not docs:
        return 0

    total_docs = len(docs)

    confidence = min(
        95,
        50 + (total_docs * 10)
    )

    return confidence