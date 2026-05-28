from src.vectorstore.vectorstore import (
    initialize_vectorstore
)


class MetadataRetriever:

    def __init__(self, vectordb):

        self.vectordb = vectordb

    def retrieve(self, query, company=None):

        # -----------------------------------------
        # RETRIEVE DOCUMENTS
        # -----------------------------------------

        results = self.vectordb.similarity_search_with_score(
            query,
            k=10
        )

        filtered_docs = []

        query_lower = query.lower()

        # -----------------------------------------
        # BOOLEAN / ELIGIBILITY QUERIES
        # -----------------------------------------

        important_keywords = [
            "backlog",
            "bond",
            "cgpa",
            "package",
            "offers",
            "eligibility",
            "allow"
        ]

        relaxed_mode = False

        for keyword in important_keywords:

            if keyword in query_lower:

                relaxed_mode = True
                break

        # -----------------------------------------
        # FILTER SCORES
        # -----------------------------------------

        for doc, score in results:

            # LOWER SCORE = BETTER

            if relaxed_mode:

                # KEEP MORE DOCS
                if score < 15:

                    filtered_docs.append(doc)

            else:

                if score < 8:

                    filtered_docs.append(doc)

        # -----------------------------------------
        # COMPANY FILTER
        # -----------------------------------------

        if company:

            company_docs = []

            for doc in filtered_docs:

                content = doc.page_content.lower()

                if company.lower() in content:

                    company_docs.append(doc)

            if company_docs:

                filtered_docs = company_docs

        return filtered_docs


def retrieve_documents(query, company=None):

    vectordb = initialize_vectorstore()

    retriever = MetadataRetriever(vectordb)

    docs = retriever.retrieve(
        query=query,
        company=company
    )

    return docs