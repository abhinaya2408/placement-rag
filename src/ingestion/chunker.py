from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def split_documents(documents):

    from src.config.settings import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks