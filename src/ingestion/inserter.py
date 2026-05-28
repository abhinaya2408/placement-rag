def insert_context(docs):

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    return context