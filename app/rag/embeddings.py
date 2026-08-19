from functools import lru_cache

from langchain_huggingface import (
    HuggingFaceEmbeddings,
)

from app.rag.config import EMBEDDING_MODEL


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )