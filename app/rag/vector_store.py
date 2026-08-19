from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from app.rag.config import (
    COLLECTION_NAME,
    QDRANT_HOST,
    QDRANT_PORT,
)
from app.rag.embeddings import get_embeddings


class VectorStore:

    def __init__(self) -> None:

        self.client = QdrantClient(
            host=QDRANT_HOST,
            port=QDRANT_PORT,
        )

        self.embeddings = get_embeddings()

    def collection_exists(self) -> bool:

        collections = (
            self.client.get_collections()
        )

        return any(
            collection.name
            == COLLECTION_NAME
            for collection
            in collections.collections
        )

    def create_store(
        self,
        documents=None,
    ):

        if documents:

            store = (
                QdrantVectorStore.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    url=(
                        f"http://"
                        f"{QDRANT_HOST}:"
                        f"{QDRANT_PORT}"
                    ),
                    collection_name=COLLECTION_NAME,
                )
            )

            return store

        return QdrantVectorStore(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
        )

    def get_store(self):

        return QdrantVectorStore(
            client=self.client,
            collection_name=COLLECTION_NAME,
            embedding=self.embeddings,
        )

    def delete_collection(self) -> None:

        if self.collection_exists():

            self.client.delete_collection(
                collection_name=COLLECTION_NAME
            )