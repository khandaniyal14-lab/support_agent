from app.rag.chunker import split_documents
from app.rag.config import KNOWLEDGE_BASE_PATH
from app.rag.loaders import load_documents
from app.rag.vector_store import VectorStore


def ingest_knowledge_base() -> dict:

    documents = load_documents(
        KNOWLEDGE_BASE_PATH
    )

    if not documents:
        raise ValueError(
            "No knowledge-base documents found."
        )

    chunks = split_documents(
        documents
    )

    if not chunks:
        raise ValueError(
            "No document chunks were created."
        )

    vector_store = VectorStore()

    vector_store.delete_collection()

    vector_store.create_store(
        documents=chunks
    )

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "collection": "customer_support_knowledge",
    }