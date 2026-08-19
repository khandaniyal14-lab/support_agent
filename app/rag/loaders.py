from pathlib import Path

from langchain_core.documents import Document

SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
}


def load_documents(
    knowledge_base_path: Path,
) -> list[Document]:

    documents: list[Document] = []

    for path in knowledge_base_path.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        content = path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        relative_path = path.relative_to(
            knowledge_base_path
        )

        parts = relative_path.parts

        category = (
            parts[0]
            if len(parts) > 1
            else "general"
        )

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "document_id": str(
                        relative_path
                    ),
                    "source": str(
                        relative_path
                    ),
                    "category": category,
                },
            )
        )

    return documents