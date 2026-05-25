from src.query_rewriter import rewrite_query
from src.reranker import rerank
from src.refiner import refine_documents
from src.inserter import insert_context
from src.generator import generate_answer
from src.citations import extract_sources
from src.cache_manager import get_cache, set_cache
from src.fallback import fallback_response
from src.memory import save_memory

def run_pipeline(query, vectordb):

    # ---------------- CACHE ----------------

    cached_response = get_cache(query)

    if cached_response:

        return {
            "rewritten_query": query,
            "docs": [],
            "answer": cached_response,
            "sources": []
        }

    # ---------------- QUERY REWRITE ----------------

    rewritten_query = rewrite_query(query)

    # ---------------- RETRIEVAL ----------------

    docs = vectordb.similarity_search(
        rewritten_query,
        k=5
    )

    # ---------------- NO DOCUMENTS ----------------

    if not docs:

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": fallback_response(),
            "sources": []
        }

    # ---------------- RERANK ----------------

    reranked_docs = rerank(
        rewritten_query,
        docs
    )

    # ---------------- REFINE ----------------

    refined_docs = refine_documents(
        reranked_docs
    )

    # ---------------- INSERT CONTEXT ----------------

    context = insert_context(
        refined_docs
    )

    # ---------------- EMPTY CONTEXT ----------------

    if not context.strip():

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": fallback_response(),
            "sources": []
        }

    # ---------------- GENERATE ----------------

    answer = generate_answer(
        rewritten_query,
        context
    )

    # ---------------- MEMORY SAVE ----------------

    save_memory(
        rewritten_query,
        answer
    )

    # ---------------- CACHE SAVE ----------------

    set_cache(query, answer)

    # ---------------- SOURCES ----------------

    sources = extract_sources(
        refined_docs
    )

    return {
        "rewritten_query": rewritten_query,
        "docs": refined_docs,
        "answer": answer,
        "sources": sources
    }