from src.reasoning.query_rewriter import rewrite_query

from src.retrieval.retriever import retrieve_documents
from src.retrieval.retrieval_filter import filter_retrieved_docs
from src.retrieval.reranker import rerank
from src.retrieval.refiner import refine_documents
from src.retrieval.deduplicator import deduplicate_docs

from src.reasoning.reasoning import (
    is_reasoning_query,
    run_reasoning
)

from src.reasoning.conflict_detector import detect_conflicts

from src.generation.generator import generate_answer
from src.generation.formatter import format_response
from src.generation.fallback import fallback_response

from src.ingestion.inserter import insert_context

from src.response.confidence import calculate_confidence
from src.response.citations import extract_sources

from src.memory.memory import save_memory

from src.cache_manager import (
    get_cache,
    set_cache
)
from tools.web_tool import search_web
def run_pipeline(query, vectordb):

    # ---------------------------------------------------
    # CACHE CHECK
    # ---------------------------------------------------

    # cached_response = get_cache(query)

    # if cached_response:

    #     return {
    #         "rewritten_query": query,
    #         "docs": [],
    #         "answer": cached_response,
    #         "sources": [],
    #         "confidence": 95
    #     }

    # ---------------------------------------------------
    # QUERY REWRITE
    # ---------------------------------------------------

    rewritten_query = rewrite_query(query)

    if not rewritten_query.strip():

        rewritten_query = query

    # ---------------------------------------------------
    # DETECT COMPANY
    # ---------------------------------------------------

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

    for alias, actual_name in companies.items():

        if alias in rewritten_query.lower():

            company = actual_name

            break

    # ---------------------------------------------------
    # RETRIEVAL
    # ---------------------------------------------------

    docs = retrieve_documents(
        rewritten_query,
        company=company
    )

    # ---------------------------------------------------
    # EMPTY RETRIEVAL
    # ---------------------------------------------------

    if not docs:

        web_answer = search_web(
            rewritten_query
        )

        return {
        "rewritten_query": rewritten_query,
        "docs": [],
        "answer": web_answer,
        "sources": ["Web Search"],
        "confidence": 70
        }

    # ---------------------------------------------------
    # RERANKING
    # ---------------------------------------------------

    reranked_docs = rerank(
        rewritten_query,
        docs
    )

    # ---------------------------------------------------
    # REFINEMENT
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

        web_answer = search_web(
            rewritten_query
        )

        return {
            "rewritten_query": rewritten_query,
            "docs": [],
            "answer": web_answer,
            "sources": ["Web Search"],
            "confidence": 70
        }

    # ---------------------------------------------------
    # CONFLICT DETECTION
    # ---------------------------------------------------

    conflicts = detect_conflicts(
        rewritten_query,
        refined_docs
    )

    # ---------------------------------------------------
    # REASONING
    # ---------------------------------------------------

# ---------------------------------------------------
# REASONING
# ---------------------------------------------------

    reasoning_keywords = [
        "highest",
        "compare",
        "difference",
        "versus",
        "vs",
        "better",
        "rank"
    ]

    use_reasoning = False

    for keyword in reasoning_keywords:

        if keyword in rewritten_query.lower():

            use_reasoning = True
            break

# ---------------------------------------------------
# RUN REASONING ONLY FOR TRUE REASONING QUERIES
# ---------------------------------------------------

    if use_reasoning:

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
# LOAD MEMORY ONLY FOR GENERATION
# ---------------------------------------------------

    memory_context = ""

    try:

        from src.memory.memory import load_memory

        memory_context = load_memory()

    except:

        memory_context = ""

# ---------------------------------------------------
# GENERATE ANSWER
# MEMORY USED ONLY HERE
# ---------------------------------------------------

    generation_context = f"""
    Conversation History:
    {memory_context}

    Retrieved Context:  
    {context}

    Current Query:
    {rewritten_query}
    """

    raw_answer = generate_answer(
        rewritten_query,
        generation_context
    )

    # ---------------------------------------------------
    # FORMAT RESPONSE
    # ---------------------------------------------------

    answer = format_response(
        raw_answer
    )

    if (
        "information not available" in answer.lower()
        or
        "uploaded documents" in answer.lower()
    ):

        web_answer = search_web(
            rewritten_query
        )

        answer = web_answer

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

    # set_cache(
    #     query,
    #     answer
    # )

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