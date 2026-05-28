from src.vectorstore.vectorstore import initialize_vectorstore


class MetadataRetriever:

    def __init__(self, vectordb):

        self.vectordb = vectordb

    def retrieve(self, query, company=None):

        retriever = self.vectordb.as_retriever(
            search_kwargs={"k": 8}
        )

        docs = retriever.invoke(query)

        # METADATA FILTERING

        if company:

            filtered_docs = []

            for doc in docs:

                content = doc.page_content.lower()

                if company.lower() in content:

                    filtered_docs.append(doc)

            if filtered_docs:

                docs = filtered_docs

        return docs


def retrieve_documents(query, company=None):

    vectordb = initialize_vectorstore()

    retriever = MetadataRetriever(vectordb)

    docs = retriever.retrieve(
        query,
        company=company
    )

    return docs