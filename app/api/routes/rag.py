from fastapi import APIRouter, HTTPException

from app.rag.retrieval import Retriever
from app.rag.schemas import (
    RAGSearchRequest,
    RAGSearchResponse,
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


retriever = Retriever()


@router.post(
    "/search",
    response_model=RAGSearchResponse,
)
def search_knowledge_base(
    request: RAGSearchRequest,
):

    try:

        results = retriever.search(
            query=request.query,
            top_k=request.top_k,
        )

        return RAGSearchResponse(
            query=request.query,
            results=results,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail="Knowledge base search failed.",
        ) from exc