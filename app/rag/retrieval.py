from langchain_core.documents import Document

from app.rag.schemas import RetrievalResult
from app.rag.vector_store import VectorStore


class Retriever:

    def __init__(
        self,
        vector_store: VectorStore | None = None,
    ) -> None:

        self.vector_store = (
            vector_store
            or VectorStore()
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        store = self.vector_store.get_store()

        results = (
            store.similarity_search_with_score(
                query,
                k=top_k,
            )
        )

        return [
            self._convert_result(
                document,
                score,
            )
            for document, score in results
        ]

    @staticmethod
    def _convert_result(
        document: Document,
        score: float,
    ) -> RetrievalResult:

        metadata = document.metadata

        return RetrievalResult(
            chunk_id=str(
                metadata.get(
                    "chunk_id",
                    "",
                )
            ),
            document_id=str(
                metadata.get(
                    "document_id",
                    "",
                )
            ),
            source=str(
                metadata.get(
                    "source",
                    "",
                )
            ),
            category=str(
                metadata.get(
                    "category",
                    "",
                )
            ),
            content=document.page_content,
            score=float(score),
        )