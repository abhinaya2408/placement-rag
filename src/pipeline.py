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
from src.retrieval_filter import filter_retrieved_docs

from src.reasoning import (
    is_reasoning_query,
    run_reasoning
)

from src.conflict_detector import detect_conflicts
from src.confidence import calculate_confidence


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
            "sources": [],
            "confidence": 95
        }

    # ---------------------------------------------------
    # QUERY REWRITE
    # ---------------------------------------------------

    rewritten_query = rewrite_query(query)

    if not rewritten_query.strip():

        rewritten_query = query

    # ---------------------------------------------------
    # METADATA RETRIEVAL
    # ---------------------------------------------------

    retriever = MetadataRetriever(vectordb)

    company = None

    companies = {
        "amazon": "Amazon",
        "tcs": "TCS",
        "infosys": "Infosys",
        "google": "Google",
        "microsoft": "Microsoft",
        "wipro": "Wipro",
        "flipkart": "Flipkart",
        "deloitte": "Deloitte",
        "ibm": "IBM",
        "hcl": "HCL",
        "qualcomm": "Qualcomm",
        "samsung": "Samsung",
        "oracle": "Oracle",
        "adobe": "Adobe",
        "sap": "SAP",
        "tech mahindra": "Tech Mahindra",
        "mahindra": "Tech Mahindra",
        "cognizant": "Cognizant",
        "capgemini": "Capgemini",
        "accenture": "Accenture"
    }

    # ---------------------------------------------------
    # DETECT COMPANY
    # ---------------------------------------------------

    for alias, actual_name in companies.items():

        if alias in rewritten_query.lower():

            company = actual_name

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
            "sources": [],
            "confidence": 0
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
    # RETRIEVAL FILTERING
    # ---------------------------------------------------

    refined_docs = filter_retrieved_docs(
        refined_docs
    )

    # ---------------------------------------------------
    # EMPTY AFTER FILTER
    # ---------------------------------------------------

    if not refined_docs:

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": fallback_response(),
            "sources": [],
            "confidence": 0
        }

    # ---------------------------------------------------
    # CONFLICT DETECTION
    # ---------------------------------------------------

    conflicts = detect_conflicts(
        rewritten_query,
        refined_docs
    )

    # ---------------------------------------------------
    # REASONING ENGINE
    # ---------------------------------------------------

    if is_reasoning_query(rewritten_query):

        reasoning_context = run_reasoning(
            rewritten_query,
            refined_docs
        )

        if reasoning_context:

            context = reasoning_context

        else:

            context = insert_context(
                refined_docs
            )

    else:

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
            "sources": [],
            "confidence": 0
        }

    # ---------------------------------------------------
    # GENERATE ANSWER
    # ---------------------------------------------------

    raw_answer = generate_answer(
        rewritten_query,
        context
    )

    # ---------------------------------------------------
    # FORMAT RESPONSE
    # ---------------------------------------------------

    answer = format_response(
        raw_answer
    )

    # ---------------------------------------------------
    # APPEND CONFLICT WARNINGS
    # ---------------------------------------------------

    if conflicts:

        answer += "\n\n⚠️ Conflicting records detected:\n"

        for conflict in conflicts:

            answer += (
                f"\n• {conflict['company']} "
                f"has multiple values: "
                f"{conflict['values']}"
            )

    # ---------------------------------------------------
    # CONFIDENCE SCORE
    # ---------------------------------------------------

    confidence = calculate_confidence(
        refined_docs
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
        "sources": sources,
        "confidence": confidence
    }