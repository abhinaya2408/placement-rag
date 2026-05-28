from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from src.config.settings import (
    EMBEDDING_MODEL
)


def get_embeddings():

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings