def filter_retrieved_docs(docs):

    filtered = []

    seen = set()

    for doc in docs:

        content = doc.page_content.strip()

        # -----------------------------------------
        # REMOVE VERY SHORT CHUNKS
        # -----------------------------------------

        if len(content) < 30:
            continue

        # -----------------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------------

        if content in seen:
            continue

        seen.add(content)

        filtered.append(doc)

    return filtered