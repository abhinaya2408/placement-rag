from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src.table_extractor import extract_tables
from src.ocr_extractor import extract_ocr_text

import os


PERSIST_DIRECTORY = "chroma_db_new"


def initialize_vectorstore():

    pdf_path = "data/Placement_RAG_Dataset_Enhanced.pdf"

    # ---------------------------------------------------
    # LOAD NORMAL PDF TEXT
    # ---------------------------------------------------

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    # ---------------------------------------------------
    # TABLE EXTRACTION
    # ---------------------------------------------------

    table_docs = extract_tables(
        pdf_path
    )

    documents.extend(table_docs)

    # ---------------------------------------------------
    # OCR EXTRACTION
    # ---------------------------------------------------

    ocr_docs = extract_ocr_text(
        pdf_path
    )

    documents.extend(ocr_docs)

    # ---------------------------------------------------
    # SMART CHUNKING
    # ---------------------------------------------------

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " "
        ]
    )

    split_docs = text_splitter.split_documents(
        documents
    )

    # ---------------------------------------------------
    # METADATA TAGGING
    # ---------------------------------------------------

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

    for doc in split_docs:

        content = doc.page_content.lower()

        found_company = None

        for company in companies:

            if company.lower() in content:

                found_company = company

                break

        doc.metadata["company"] = (
            found_company
            if found_company
            else "Unknown"
        )

    # ---------------------------------------------------
    # EMBEDDINGS
    # ---------------------------------------------------

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ---------------------------------------------------
    # CREATE CHROMADB
    # ---------------------------------------------------

    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    return vectordb