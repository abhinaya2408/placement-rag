from src.query_rewriter import rewrite_query
from src.reranker import rerank
from src.refiner import refine_documents
from src.inserter import insert_context
from src.generator import generate_answer
from src.citations import extract_sources
from src.cache_manager import get_cache, set_cache
from src.fallback import fallback_response
from src.memory import save_memory
from src.retriever import MetadataRetriever
from src.formatter import format_response
from src.deduplicator import deduplicate_docs

def run_pipeline(query, vectordb):

    # ---------------------------------------------------
    # CACHE CHECK
    # ---------------------------------------------------

    cached_response = get_cache(query)

    if cached_response:

        return {
            "rewritten_query": query,
            "docs": [],
            "answer": cached_response,
            "sources": []
        }

    # ---------------------------------------------------
    # QUERY REWRITE
    # ---------------------------------------------------

    rewritten_query = rewrite_query(query)

    # ---------------------------------------------------
    # METADATA RETRIEVAL
    # ---------------------------------------------------

    retriever = MetadataRetriever(vectordb)

    company = None

    companies = [
        "Amazon",
        "TCS",
        "Infosys",
        "Google",
        "Microsoft",
        "Wipro",
        "Flipkart",
        "Deloitte",
        "IBM",
        "HCL",
        "Qualcomm",
        "Samsung",
        "Oracle",
        "Adobe",
        "SAP",
        "Tech Mahindra",
        "Capgemini",
        "Cognizant",
        "Accenture"
    ]

    # DETECT COMPANY

    for c in companies:

        if c.lower() in rewritten_query.lower():

            company = c

            break

    # ---------------------------------------------------
    # RETRIEVE DOCUMENTS
    # ---------------------------------------------------

    docs = retriever.retrieve(
        rewritten_query,
        company=company
    )

    # ---------------------------------------------------
    # NO DOCUMENTS
    # ---------------------------------------------------

    if not docs:

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": fallback_response(),
            "sources": []
        }

    # ---------------------------------------------------
    # RERANK
    # ---------------------------------------------------

    reranked_docs = rerank(
        rewritten_query,
        docs
    )

    # ---------------------------------------------------
    # REFINE
    # ---------------------------------------------------

    refined_docs = refine_documents(
        reranked_docs
    )

    # ---------------------------------------------------
    # DEDUPLICATION
    # ---------------------------------------------------

    refined_docs = deduplicate_docs(
        refined_docs
    )

    # ---------------------------------------------------
    # INSERT CONTEXT
    # ---------------------------------------------------

    context = insert_context(
        refined_docs
    )

    # ---------------------------------------------------
    # EMPTY CONTEXT
    # ---------------------------------------------------

    if not context.strip():

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": fallback_response(),
            "sources": []
        }

    # ---------------------------------------------------
    # GENERATE RAW ANSWER
    # ---------------------------------------------------

    raw_answer = generate_answer(
        rewritten_query,
        context
    )

    # ---------------------------------------------------
    # FORMAT ANSWER
    # ---------------------------------------------------

    answer = format_response(
        raw_answer
    )

    # ---------------------------------------------------
    # SAVE MEMORY
    # ---------------------------------------------------

    save_memory(
        rewritten_query,
        answer
    )

    # ---------------------------------------------------
    # SAVE CACHE
    # ---------------------------------------------------

    set_cache(
        query,
        answer
    )

    # ---------------------------------------------------
    # SOURCES
    # ---------------------------------------------------

    sources = extract_sources(
        refined_docs
    )

    # ---------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------

    return {
        "rewritten_query": rewritten_query,
        "docs": refined_docs,
        "answer": answer,
        "sources": sources
    }