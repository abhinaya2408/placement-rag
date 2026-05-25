class MetadataRetriever:

    def __init__(self, vectordb):

        self.vectordb = vectordb

    def retrieve(self, query, company=None):

        # -----------------------------------
        # METADATA FILTER RETRIEVAL
        # -----------------------------------

        if company:

            docs = self.vectordb.similarity_search(
                query,
                k=5,
                filter={
                    "company": company
                }
            )

            # FALLBACK TO NORMAL SEARCH

            if len(docs) == 0:

                docs = self.vectordb.similarity_search(
                    query,
                    k=5
                )

        # -----------------------------------
        # NORMAL RETRIEVAL
        # -----------------------------------

        else:

            docs = self.vectordb.similarity_search(
                query,
                k=5
            )

        return docs