from pydantic import BaseModel, Field


class RetrievalResult(BaseModel):

    chunk_id: str

    document_id: str

    source: str

    category: str

    content: str

    score: float


class RAGSearchRequest(BaseModel):

    query: str = Field(
        min_length=1,
        max_length=5000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class RAGSearchResponse(BaseModel):

    query: str

    results: list[RetrievalResult]