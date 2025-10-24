"""FAISS-based vector store implementation."""

import os
from typing import List, Tuple
import numpy as np
import faiss
from ace.vectorstores.base import VectorStoreBase


class FAISSVectorStore(VectorStoreBase):
    """FAISS-based vector store for fast similarity search.
    
    Uses Inner Product index for cosine similarity with normalized vectors.
    """
    
    def __init__(self, storage_path: str, dimension: int = 1536):
        """Initialize FAISS vector store.
        
        Args:
            storage_path: Directory path for storing FAISS index
            dimension: Dimension of embedding vectors (default: 1536 for text-embedding-3-small)
        """
        super().__init__(storage_path, dimension)
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize FAISS index (Inner Product for cosine similarity)
        self.index = faiss.IndexFlatIP(dimension)
        self.index_file = os.path.join(storage_path, "faiss_index.bin")
        
        # Load existing index if available
        self.load()
    
    def add_embeddings(
        self, 
        texts: List[str], 
        embeddings: np.ndarray, 
        ids: List[str]
    ) -> None:
        """Add embeddings to FAISS index.
        
        Args:
            texts: List of text content (not used in FAISS, kept for interface compatibility)
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            ids: List of unique IDs (not used in FAISS, indices are used instead)
        """
        # Normalize embeddings for cosine similarity
        normalized_embeddings = self._normalize_embeddings(embeddings)
        
        # Add to FAISS index
        self.index.add(normalized_embeddings.astype(np.float32))
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 10
    ) -> Tuple[List[float], List[int]]:
        """Search for similar embeddings using FAISS.
        
        Args:
            query_embedding: Query embedding vector (shape: [dimension])
            top_k: Number of results to return
            
        Returns:
            Tuple of (scores, indices)
        """
        if self.index.ntotal == 0:
            return [], []
        
        # Normalize query embedding
        normalized_query = self._normalize_embeddings(
            query_embedding.reshape(1, -1)
        )
        
        # Search FAISS index
        k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(
            normalized_query.astype(np.float32), 
            k
        )
        
        return scores[0].tolist(), indices[0].tolist()
    
    def delete(self, ids: List[str]) -> None:
        """Delete embeddings by IDs.
        
        Note: FAISS IndexFlatIP doesn't support deletion.
        This would require rebuilding the index or using IDMap wrapper.
        For now, this is a placeholder.
        
        Args:
            ids: List of IDs to delete
        """
        # FAISS IndexFlatIP doesn't support deletion
        # To implement deletion, we would need to:
        # 1. Use IndexIDMap wrapper, or
        # 2. Rebuild the index without deleted items
        pass
    
    def save(self) -> None:
        """Save FAISS index to disk."""
        faiss.write_index(self.index, self.index_file)
    
    def load(self) -> bool:
        """Load FAISS index from disk.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if os.path.exists(self.index_file):
            try:
                self.index = faiss.read_index(self.index_file)
                return True
            except Exception as e:
                print(f"Warning: Failed to load FAISS index: {e}")
                self.index = faiss.IndexFlatIP(self.dimension)
                return False
        return False
    
    def get_count(self) -> int:
        """Get total number of vectors in FAISS index.
        
        Returns:
            Number of vectors
        """
        return self.index.ntotal
    
    def count(self) -> int:
        """Alias for get_count() for convenience.
        
        Returns:
            Number of vectors
        """
        return self.get_count()
    
    def clear(self) -> None:
        """Clear all vectors from FAISS index."""
        self.index.reset()
    
    def _normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """Normalize embeddings for cosine similarity.
        
        Args:
            embeddings: Embeddings to normalize
            
        Returns:
            Normalized embeddings
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms = np.where(norms > 0, norms, 1.0)
        return embeddings / norms

