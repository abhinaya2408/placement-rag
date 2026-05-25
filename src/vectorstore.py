import os

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.embeddings import load_embeddings

DB_PATH = "vectorstore/chroma_db"

PDF_PATH = "data/Placement_RAG_Dataset_Enhanced.pdf"

def initialize_vectorstore():

    embeddings = load_embeddings()

    if os.path.exists(DB_PATH):

        vectordb = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )

        return vectordb

    loader = PyPDFLoader(PDF_PATH)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    vectordb.persist()

    return vectordb