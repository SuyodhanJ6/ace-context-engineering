"""ChromaDB-based vector store implementation."""

import os
from typing import List, Tuple
import numpy as np
from ace.vectorstores.base import VectorStoreBase

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None


class ChromaDBVectorStore(VectorStoreBase):
    """ChromaDB-based vector store for semantic search.
    
    Provides persistent storage with metadata support.
    """
    
    def __init__(self, storage_path: str, dimension: int = 1536, collection_name: str = "ace_playbook"):
        """Initialize ChromaDB vector store.
        
        Args:
            storage_path: Directory path for storing ChromaDB data
            dimension: Dimension of embedding vectors (default: 1536)
            collection_name: Name of the ChromaDB collection
            
        Raises:
            ImportError: If chromadb is not installed
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError(
                "ChromaDB is not installed. Install it with: pip install chromadb"
            )
        
        super().__init__(storage_path, dimension)
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(
            path=storage_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"dimension": dimension}
        )
    
    def add_embeddings(
        self, 
        texts: List[str], 
        embeddings: np.ndarray, 
        ids: List[str]
    ) -> None:
        """Add embeddings to ChromaDB collection.
        
        Args:
            texts: List of text content
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            ids: List of unique IDs for each embedding
        """
        # Convert numpy array to list for ChromaDB
        embeddings_list = embeddings.tolist()
        
        # Add to ChromaDB collection
        self.collection.add(
            embeddings=embeddings_list,
            documents=texts,
            ids=ids
        )
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 10
    ) -> Tuple[List[float], List[int]]:
        """Search for similar embeddings using ChromaDB.
        
        Args:
            query_embedding: Query embedding vector (shape: [dimension])
            top_k: Number of results to return
            
        Returns:
            Tuple of (scores, indices)
            Note: ChromaDB returns IDs, not indices. We convert IDs to indices.
        """
        if self.collection.count() == 0:
            return [], []
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, self.collection.count())
        )
        
        # Extract distances and IDs
        if results['distances'] and results['ids']:
            # ChromaDB returns distances (lower is more similar)
            # Convert to similarity scores (higher is more similar)
            distances = results['distances'][0]
            scores = [1.0 / (1.0 + d) for d in distances]
            
            # ChromaDB returns IDs, we need to map them to indices
            # For simplicity, we'll return the IDs as string indices
            # The caller needs to handle ID-to-index mapping
            ids = results['ids'][0]
            
            # Create pseudo-indices from IDs (extract number from ctx-XXXXX format)
            indices = []
            for id_str in ids:
                try:
                    # Try to extract index from ID (e.g., "ctx-00123" -> 123)
                    if '-' in id_str:
                        idx = int(id_str.split('-')[-1])
                    else:
                        idx = hash(id_str) % 1000000
                    indices.append(idx)
                except:
                    indices.append(hash(id_str) % 1000000)
            
            return scores, indices
        
        return [], []
    
    def delete(self, ids: List[str]) -> None:
        """Delete embeddings by IDs from ChromaDB.
        
        Args:
            ids: List of IDs to delete
        """
        if ids:
            self.collection.delete(ids=ids)
    
    def save(self) -> None:
        """Save ChromaDB collection.
        
        ChromaDB automatically persists data, so this is a no-op.
        """
        # ChromaDB persists automatically with PersistentClient
        pass
    
    def load(self) -> bool:
        """Load ChromaDB collection.
        
        ChromaDB automatically loads data from persistent storage.
        
        Returns:
            True if collection exists, False otherwise
        """
        try:
            collections = self.client.list_collections()
            return any(c.name == self.collection_name for c in collections)
        except:
            return False
    
    def get_count(self) -> int:
        """Get total number of vectors in ChromaDB collection.
        
        Returns:
            Number of vectors
        """
        return self.collection.count()
    
    def clear(self) -> None:
        """Clear all vectors from ChromaDB collection."""
        # Delete the collection and recreate it
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"dimension": self.dimension}
        )

