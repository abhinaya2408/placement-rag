from rank_bm25 import BM25Okapi

class HybridRetriever:

    def __init__(self, vectordb, chunks):

        self.vectordb = vectordb

        self.text_chunks = [
            doc.page_content
            for doc in chunks
        ]

        tokenized_chunks = [
            text.split()
            for text in self.text_chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def semantic_search(self, query, k=5):

        return self.vectordb.similarity_search(
            query,
            k=k
        )

    def keyword_search(self, query, k=5):

        scores = self.bm25.get_scores(
            query.split()
        )

        ranked = sorted(
            zip(self.text_chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:k]