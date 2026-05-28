from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank(query, docs):

    if not docs:
        return []

    pairs = [
        (query, doc.page_content)
        for doc in docs
    ]

    scores = model.predict(pairs)

    scored_docs = list(
        zip(scores, docs)
    )

    scored_docs.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    reranked_docs = [
        doc for _, doc in scored_docs
    ]

    return reranked_docs