import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.ingestion.chunker import split_documents
from src.ingestion.embeddings import get_embeddings
from src.ingestion.ocr_extractor import extract_ocr_text
from src.ingestion.table_extractor import extract_tables


from src.config.settings import CHROMA_PATH
DATA_PATH = "data"


def load_documents():

    documents = []

    if not os.path.exists(DATA_PATH):
        return documents

    for file in os.listdir(DATA_PATH):

        if not file.endswith(".pdf"):
            continue

        file_path = os.path.join(DATA_PATH, file)

        # -----------------------------
        # NORMAL PDF EXTRACTION
        # -----------------------------

        try:

            loader = PyPDFLoader(file_path)

            docs = loader.load()

            for doc in docs:

                doc.metadata["source"] = file

            documents.extend(docs)

        except Exception as e:

            print(f"PDF Extraction Error: {e}")

        # -----------------------------
        # OCR EXTRACTION
        # -----------------------------

        try:

            ocr_text = extract_ocr_text(file_path)

            if ocr_text.strip():

                documents.append(
                    Document(
                        page_content=ocr_text,
                        metadata={
                            "source": file,
                            "type": "ocr"
                        }
                    )
                )

        except Exception as e:

            print(f"OCR Error: {e}")

        # -----------------------------
        # TABLE EXTRACTION
        # -----------------------------

        try:

            tables = extract_tables(file_path)

            for table in tables:

                documents.append(
                    Document(
                        page_content=table,
                        metadata={
                            "source": file,
                            "type": "table"
                        }
                    )
                )

        except Exception as e:

            print(f"Table Extraction Error: {e}")

    return documents


def initialize_vectorstore():

    embedding_function = get_embeddings()

    # -----------------------------
    # LOAD EXISTING DB
    # -----------------------------

    if os.path.exists(CHROMA_PATH):

        vectordb = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function
        )

        return vectordb

    # -----------------------------
    # CREATE NEW DB
    # -----------------------------

    documents = load_documents()

    chunks = split_documents(documents)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=CHROMA_PATH
    )

    return vectordb