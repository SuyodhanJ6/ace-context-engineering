"""Vector store implementations for ACE framework."""

from ace.vectorstores.base import VectorStoreBase
from ace.vectorstores.faiss import FAISSVectorStore

__all__ = ["VectorStoreBase", "FAISSVectorStore"]

# ChromaDB is optional dependency
try:
    from ace.vectorstores.chromadb import ChromaDBVectorStore
    __all__.append("ChromaDBVectorStore")
except ImportError:
    ChromaDBVectorStore = None

