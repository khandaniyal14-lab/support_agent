from app.rag.ingestion import (
    ingest_knowledge_base,
)


def main() -> None:

    result = ingest_knowledge_base()

    print("\n" + "=" * 60)
    print("KNOWLEDGE BASE INGESTION COMPLETE")
    print("=" * 60)

    print(
        f"Documents : {result['documents']}"
    )

    print(
        f"Chunks    : {result['chunks']}"
    )

    print(
        f"Collection: {result['collection']}"
    )


if __name__ == "__main__":
    main()