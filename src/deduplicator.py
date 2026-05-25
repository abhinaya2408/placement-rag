def deduplicate_docs(docs):

    unique_contents = set()

    unique_docs = []

    for doc in docs:

        content = doc.page_content.strip()

        # SKIP DUPLICATE CHUNKS

        if content in unique_contents:
            continue

        unique_contents.add(content)

        unique_docs.append(doc)

    return unique_docs