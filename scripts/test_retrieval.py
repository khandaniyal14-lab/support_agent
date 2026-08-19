from app.rag.retrieval import Retriever


def main() -> None:

    retriever = Retriever()

    queries = [
        "How long do I have to request a refund?",
        "I was charged twice for my order.",
        "My payment failed.",
        "Can I cancel an order after it has shipped?",
        "I cannot log into my account.",
    ]

    for query in queries:

        print("\n" + "=" * 70)
        print(
            f"QUERY: {query}"
        )
        print("=" * 70)

        results = retriever.search(
            query=query,
            top_k=3,
        )

        for index, result in enumerate(
            results,
            start=1,
        ):

            print(
                f"\n[{index}] "
                f"Score: {result.score:.4f}"
            )

            print(
                f"Source: {result.source}"
            )

            print(
                result.content
            )


if __name__ == "__main__":
    main()