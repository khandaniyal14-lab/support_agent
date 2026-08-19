from pathlib import Path

KNOWLEDGE_BASE_PATH = Path("data/knowledge")

COLLECTION_NAME = "customer_support_knowledge"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTOR_SIZE = 384

CHUNK_SIZE = 700

CHUNK_OVERLAP = 100

DEFAULT_TOP_K = 5

QDRANT_HOST = "localhost"

QDRANT_PORT = 6333