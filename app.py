import streamlit as st

from src.vectorstore.vectorstore import initialize_vectorstore
from src.pipeline import run_pipeline
# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Placement Intelligence RAG",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stChatMessage {
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}

.stExpander {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🚀 Placement Intelligence RAG Assistant")

st.caption(
    "Enterprise Placement Intelligence RAG Assistant"
)

st.divider()

# ---------------------------------------------------
# SESSION CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# ---------------------------------------------------
# INITIALIZE VECTORSTORE
# ---------------------------------------------------

with st.spinner("Initializing vector database..."):

    vectordb = initialize_vectorstore()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("⚙️ Pipeline Stages")

    stages = [
        "Rewrite",
        "Retrieve",
        "Rerank",
        "Refine",
        "Insert",
        "Generate"
    ]

    for stage in stages:

        st.success(stage)

    st.divider()

    st.header("📌 Features")

    features = [
        "Persistent ChromaDB",
        "Hybrid Retrieval",
        "Conversation Memory",
        "Cross Encoder Reranking",
        "Grounded Generation",
        "Hallucination Control",
        "Source Citations",
        "Modular Architecture"
    ]

    for feature in features:

        st.info(feature)

    st.divider()

    st.header("📊 System Info")

    st.metric(
        label="Vector DB",
        value="ChromaDB"
    )

    st.metric(
        label="Retriever",
        value="Hybrid"
    )

    st.metric(
        label="LLM",
        value="Llama 3.1"
    )

# ---------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

# ---------------------------------------------------
# EXAMPLE QUESTIONS
# ---------------------------------------------------

if len(st.session_state.messages) == 0:

    st.info(
        "Ask placement related questions like eligibility, packages, hiring trends, interview rounds, and company comparisons."
    )

    st.subheader("💡 Example Questions")

    st.markdown("""
    - Which companies allow 2 backlogs?
    - Compare Amazon and TCS eligibility
    - Which company offers highest package?
    - What is Amazon package?
    - Does Microsoft allow backlogs?
    """)

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

query = st.chat_input(
    "Ask placement related questions..."
)

# ---------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------

if query:

    # STORE USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # DISPLAY USER MESSAGE

    with st.chat_message("user"):

        st.write(query)

    # RUN PIPELINE

    with st.spinner("Running enterprise RAG pipeline..."):

        result = run_pipeline(
            query=query,
            vectordb=vectordb
        )

    # REWRITTEN QUERY

    with st.expander("🔄 Rewritten Query"):

        st.write(result["rewritten_query"])

# RETRIEVED CHUNKS

    with st.expander("📚 Retrieved Chunks"):

        if (
            result["docs"]
            and "Information not available"
            not in result["answer"]
        ):

            shown_chunks = 0

            for i, doc in enumerate(result["docs"], start=1):

                content = doc.page_content.strip()

            # SKIP VERY SHORT / NOISY CHUNKS

                if len(content) < 80:
                    continue

            # SKIP BENCHMARK CHUNKS

                bad_patterns = [
                "rag challenge",
                "difficulty",
                "multi-row filter",
                "text retrieval",
                "evaluation query",
                "m1",
                "e1",
                "h1"
                ]

                lower_content = content.lower()

                skip = False

                for pattern in bad_patterns:

                    if pattern in lower_content:

                        skip = True
                        break

                if skip:
                    continue

                shown_chunks += 1

                st.markdown(f"### Chunk {shown_chunks}")

                st.write(content[:1000])

                st.divider()

            if shown_chunks == 0:

                st.info(
                    "No meaningful chunks retrieved."
                )

        else:

            st.info(
                "No relevant chunks retrieved."
            )

    # STORE ASSISTANT MESSAGE

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"]
    })

    # DISPLAY ASSISTANT MESSAGE

    with st.chat_message("assistant"):

        st.write(result["answer"])

    # ---------------------------------------------------
    # CONFIDENCE SCORE
    # ---------------------------------------------------

    st.markdown(
        f"### ✅ Confidence Score: {result['confidence']}%"
    )
    # SOURCES

    with st.expander("📌 Sources"):

        if result["sources"]:

            for source in result["sources"]:

                st.success(source)

        else:

            st.warning(
                "No sources available."
            )