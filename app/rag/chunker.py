from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def split_documents(
    documents,
):
    splitter = get_text_splitter()

    chunks = splitter.split_documents(
        documents
    )

    for index, chunk in enumerate(chunks):

        chunk.metadata["chunk_index"] = index

        document_id = chunk.metadata.get(
            "document_id",
            "unknown",
        )

        chunk.metadata["chunk_id"] = (
            f"{document_id}:{index}"
        )

    return chunks