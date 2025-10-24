"""Base abstract class for vector store implementations."""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
import numpy as np


class VectorStoreBase(ABC):
    """Abstract base class for vector store implementations.
    
    This provides a common interface for FAISS, ChromaDB, and other vector stores.
    """
    
    def __init__(self, storage_path: str, dimension: int):
        """Initialize vector store.
        
        Args:
            storage_path: Directory path for storing vector index
            dimension: Dimension of embedding vectors
        """
        self.storage_path = storage_path
        self.dimension = dimension
    
    @abstractmethod
    def add_embeddings(
        self, 
        texts: List[str], 
        embeddings: np.ndarray, 
        ids: List[str]
    ) -> None:
        """Add embeddings to the vector store.
        
        Args:
            texts: List of text content
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            ids: List of unique IDs for each embedding
        """
        pass
    
    @abstractmethod
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 10
    ) -> Tuple[List[float], List[int]]:
        """Search for similar embeddings.
        
        Args:
            query_embedding: Query embedding vector (shape: [dimension])
            top_k: Number of results to return
            
        Returns:
            Tuple of (scores, indices) where:
                - scores: List of similarity scores
                - indices: List of indices in the vector store
        """
        pass
    
    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        """Delete embeddings by IDs.
        
        Args:
            ids: List of IDs to delete
        """
        pass
    
    @abstractmethod
    def save(self) -> None:
        """Persist vector store to disk."""
        pass
    
    @abstractmethod
    def load(self) -> bool:
        """Load vector store from disk.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def get_count(self) -> int:
        """Get total number of vectors in store.
        
        Returns:
            Number of vectors
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all vectors from store."""
        pass

