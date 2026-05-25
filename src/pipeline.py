from src.query_rewriter import rewrite_query
from src.reranker import rerank
from src.refiner import refine_documents
from src.inserter import insert_context
from src.generator import generate_answer
from src.citations import extract_sources
from src.cache_manager import get_cache, set_cache

def run_pipeline(query, vectordb):

    cached_response = get_cache(query)

    if cached_response:

        return {
            "rewritten_query": query,
            "docs": [],
            "answer": cached_response,
            "sources": []
        }

    rewritten_query = rewrite_query(query)

    docs = vectordb.similarity_search(
        rewritten_query,
        k=5
    )

    reranked_docs = rerank(
        rewritten_query,
        docs
    )

    refined_docs = refine_documents(
        reranked_docs
    )

    context = insert_context(
        refined_docs
    )

    answer = generate_answer(
        rewritten_query,
        context
    )

    set_cache(query, answer)

    sources = extract_sources(
        refined_docs
    )

    return {
        "rewritten_query": rewritten_query,
        "docs": refined_docs,
        "answer": answer,
        "sources": sources
    }