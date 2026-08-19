from langchain_core.tools import tool

from app.rag.retrieval import Retriever

retriever = Retriever()


@tool
def search_knowledge_base(
    query: str,
) -> list[dict]:
    """
    Search the company's knowledge base.

    Use this tool when company policies, FAQs,
    troubleshooting instructions, product information,
    refund rules, return rules, payment policies,
    or cancellation rules are required.
    """

    results = retriever.search(
        query=query,
        top_k=5,
    )

    return [
        {
            "source": result.source,
            "category": result.category,
            "content": result.content,
            "score": result.score,
        }
        for result in results
    ]