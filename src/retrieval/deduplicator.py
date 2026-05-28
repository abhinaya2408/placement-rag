def deduplicate_docs(docs):

    unique_docs = []

    seen = set()

    for doc in docs:

        content = doc.page_content.strip()

        if content not in seen:

            seen.add(content)

            unique_docs.append(doc)

    return unique_docs