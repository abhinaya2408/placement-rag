def refine_documents(docs):

    refined_docs = []

    for doc in docs:

        content = doc.page_content.strip()

        # REMOVE EMPTY CONTENT

        if not content:
            continue

        # REMOVE VERY SMALL CHUNKS

        if len(content) < 30:
            continue

        refined_docs.append(doc)

    return refined_docs