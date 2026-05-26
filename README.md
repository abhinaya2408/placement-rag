# Placement-RAG-Assistant

Placement-RAG-Assistant is an advanced Retrieval-Augmented Generation (RAG) based placement intelligence system designed to help students retrieve placement-related information from placement datasets and documents using conversational AI.

The system combines semantic retrieval, OCR-based extraction, conversational memory, metadata filtering, conflict detection, grounded response generation, and confidence scoring to provide accurate and document-aware placement insights with source citations.

---

# Key Features

- Advanced PDF Document Processing
- OCR Support for Scanned PDFs
- Multi-Document Retrieval
- Semantic Search using ChromaDB
- Conversational Context Memory
- Metadata-Based Retrieval Filtering
- Conflict Detection
- Confidence Scoring
- Hybrid Retrieval Pipeline
- Grounded Prompting & Hallucination Reduction
- Source Citations with Page References
- Persistent Vector Storage
- HuggingFace Embeddings
- Groq LLM Integration
- Real-Time Vector Database Refresh
- Chat-Based User Interface
- Advanced Table Extraction
- Deduplication & Retrieval Filtering

---

# System Workflow

The application follows a complete Retrieval-Augmented Generation (RAG) pipeline for placement document understanding and conversational question answering.

## Workflow Steps

1. User uploads placement PDF documents through the Streamlit interface.
2. PDF Loader extracts document content.
3. OCR pipeline extracts text from scanned PDFs.
4. Advanced table extraction retrieves structured tabular data.
5. Metadata enrichment attaches:
   - company name
   - page number
   - document source
6. RecursiveCharacterTextSplitter performs intelligent chunking.
7. HuggingFace sentence-transformers generate embeddings.
8. Embeddings are stored in ChromaDB Vector Database.
9. User submits placement-related queries.
10. Query rewriting improves conversational understanding.
11. Metadata retrieval filters company-specific information.
12. Semantic retrieval searches relevant chunks using vector similarity.
13. Cross-encoder reranking improves retrieval quality.
14. Deduplication and retrieval filtering remove noisy chunks.
15. Conversational memory maintains previous chat context.
16. Conflict detection identifies inconsistent records.
17. Prompt construction combines:
    - retrieved chunks
    - conversational context
    - metadata
    - user query
18. Grounded prompting reduces hallucinations.
19. Groq LLM generates grounded placement-aware responses.
20. Confidence scoring estimates retrieval reliability.
21. Source citations with page references are attached to final responses.

---

# Architecture Components

## Ingestion Pipeline

- PDF Document Loader
- OCR Extraction
- Advanced Table Extraction
- Metadata Enrichment
- RecursiveCharacterTextSplitter
- HuggingFace Embeddings

## Vector & Retrieval Layer

- ChromaDB Vector Database
- Semantic Retrieval
- Metadata Filtering
- Cross-Encoder Reranking
- Persistent Local Vectorstore

## Retrieval & Generation Layer

- Conversational Memory
- Query Rewriting
- Conflict Detection
- Prompt Construction
- Grounded Prompting
- Groq LLM

## Response Layer

- Confidence Scoring
- Source Citations
- Chat Interface
- Final Grounded Response

---

# Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Framework | LangChain |
| LLM | Groq |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Database | ChromaDB |
| OCR Engine | Tesseract OCR |
| Programming Language | Python |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Placement-RAG-Assistant.git
cd Placement-RAG-Assistant
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```
---

# Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_api_key
```
---

# OCR Setup

## Install Tesseract OCR

Download and install Tesseract OCR:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki

### Linux

```bash
sudo apt install tesseract-ocr
```

---

## Install Poppler

Required for scanned PDF OCR processing.

### Windows
Download Poppler and add `Library/bin` folder path.

### Linux

```bash
sudo apt install poppler-utils
```

---

# Run Application

```bash
streamlit run app.py
```

---

# Project Structure

```text
Placement-RAG-Assistant/
│
├── app.py
├── requirements.txt
├── .env
├── chroma_db/
├── uploads/
├── src/
│   ├── pipeline.py
│   ├── vectorstore.py
│   ├── generator.py
│   ├── retriever.py
│   ├── query_rewriter.py
│   ├── conflict_detector.py
│   ├── ocr_extractor.py
│   ├── retrieval_filter.py
│   ├── table_extractor.py
│   └── memory.py
│
├── architecture.png
└── .gitignore
```

---

# Challenges Faced

- OCR extraction from scanned PDFs produced noisy text
- Table extraction required custom preprocessing
- Hallucination reduction required strict grounded prompting
- Conflict detection required metadata normalization
- Conversational memory caused aggressive query rewriting
- Large PDFs increased retrieval latency
- Retrieval filtering needed balancing between noise removal and information retention
- Cross-document retrieval caused duplicate chunk issues

---

# Future Improvements

- Multimodal Chart & Graph Understanding
- Pinecone / Weaviate Integration
- Advanced Semantic Chunking
- RAGAS Evaluation Framework
- Voice-Based Querying
- Deployment using AWS/GCP/Azure
- Fine-Tuned Placement LLM
- Real-Time Placement Analytics Dashboard
- Multi-Language Support

---

# Author

**Abhinaya Sri Daggula**
