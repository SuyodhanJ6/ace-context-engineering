"""Qdrant-based vector store implementation."""

import os
import re
from typing import List, Tuple, Optional
import numpy as np
from ace.vectorstores.base import VectorStoreBase

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    QDRANT_AVAILABLE = True
except ImportError:
    QDRANT_AVAILABLE = False
    QdrantClient = None
    Distance = None
    VectorParams = None
    PointStruct = None


class QdrantVectorStore(VectorStoreBase):
    """Qdrant-based vector store for semantic search.
    
    Stores vectors externally in Qdrant server (Docker or Cloud).
    Playbook metadata is stored locally, but all vector operations
    go to the external Qdrant server.
    """
    
    def __init__(
        self, 
        storage_path: str, 
        dimension: int = 1536,
        url: str = "http://localhost:6333",
        api_key: Optional[str] = None,
        collection_name: str = "ace_playbook"
    ):
        """Initialize Qdrant vector store.
        
        Args:
            storage_path: Required for interface compatibility (not used for Qdrant storage)
            dimension: Dimension of embedding vectors (default: 1536)
            url: Qdrant server URL (default: http://localhost:6333)
            api_key: Optional API key for Qdrant Cloud
            collection_name: Name of the Qdrant collection
            
        Raises:
            ImportError: If qdrant-client is not installed
        """
        if not QDRANT_AVAILABLE:
            raise ImportError(
                "Qdrant client is not installed. Install it with: pip install qdrant-client"
            )
        
        super().__init__(storage_path, dimension)
        
        # Initialize Qdrant client
        if api_key:
            # Cloud mode: requires both URL and API key
            self.client = QdrantClient(url=url, api_key=api_key)
        else:
            # Local mode: URL only (no API key)
            self.client = QdrantClient(url=url)
        
        self.url = url
        self.api_key = api_key
        self.collection_name = self._sanitize_collection_name(collection_name)
        
        # Maintain ID to index mapping (for search results)
        # This maps bullet IDs to their position in the bullets list
        self.id_to_index: dict = {}
        
        # Maintain mapping from bullet_id to qdrant_point_id
        # Qdrant requires integer or UUID point IDs, but we use string bullet IDs
        self.bullet_id_to_point_id: dict = {}
        self.point_id_to_bullet_id: dict = {}
        
        # Ensure collection exists
        self.load()
    
    def _sanitize_collection_name(self, name: str) -> str:
        """Sanitize collection name for Qdrant.
        
        Qdrant collection names must be valid identifiers.
        Convert to lowercase and replace invalid chars with underscore.
        
        Args:
            name: Original collection name
            
        Returns:
            Sanitized collection name
        """
        # Convert to lowercase
        name = name.lower()
        # Replace invalid characters with underscore
        name = re.sub(r'[^a-z0-9_-]', '_', name)
        # Remove consecutive underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading/trailing underscores
        name = name.strip('_')
        # Ensure it's not empty
        if not name:
            name = "ace_playbook"
        return name
    
    def _bullet_id_to_point_id(self, bullet_id: str) -> int:
        """Convert bullet ID to Qdrant point ID.
        
        Qdrant requires point IDs to be unsigned integers or UUIDs.
        We use a consistent hash to convert string bullet IDs to integers.
        
        Args:
            bullet_id: Bullet ID string (e.g., "ctx-e015e61b")
            
        Returns:
            Integer point ID for Qdrant
        """
        if bullet_id in self.bullet_id_to_point_id:
            return self.bullet_id_to_point_id[bullet_id]
        
        # Use hash to convert to integer (consistent for same input)
        # Use abs and modulo to ensure positive integer within reasonable range
        point_id = abs(hash(bullet_id)) % (2**63 - 1)  # Max int64
        
        # Store mapping
        self.bullet_id_to_point_id[bullet_id] = point_id
        self.point_id_to_bullet_id[point_id] = bullet_id
        
        return point_id
    
    def add_embeddings(
        self, 
        texts: List[str], 
        embeddings: np.ndarray, 
        ids: List[str]
    ) -> None:
        """Add embeddings to Qdrant collection.
        
        Args:
            texts: List of text content (stored as payload)
            embeddings: Numpy array of embeddings (shape: [n, dimension])
            ids: List of unique bullet IDs for each embedding
        """
        # Normalize embeddings for cosine similarity
        normalized_embeddings = self._normalize_embeddings(embeddings)
        
        # Convert to list format for Qdrant
        vectors = normalized_embeddings.tolist()
        
        # Convert bullet IDs to Qdrant point IDs
        point_ids = [self._bullet_id_to_point_id(bullet_id) for bullet_id in ids]
        
        # Create points with payload
        # Store both text and the original bullet_id in payload for reference
        points = [
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"text": text, "bullet_id": bullet_id}
            )
            for point_id, vector, text, bullet_id in zip(point_ids, vectors, texts, ids)
        ]
        
        # Upsert to Qdrant collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    def search(
        self, 
        query_embedding: np.ndarray, 
        top_k: int = 10
    ) -> Tuple[List[float], List[int]]:
        """Search for similar embeddings using Qdrant.
        
        Args:
            query_embedding: Query embedding vector (shape: [dimension])
            top_k: Number of results to return
            
        Returns:
            Tuple of (scores, indices) where:
                - scores: List of similarity scores
                - indices: List of indices (mapped from bullet IDs)
        """
        # Normalize query embedding
        normalized_query = self._normalize_embeddings(
            query_embedding.reshape(1, -1)
        )[0]
        
        # Search Qdrant collection
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=normalized_query.tolist(),
            limit=top_k,
            with_payload=True
        )
        
        if not results:
            return [], []
        
        # Extract scores, point IDs, and convert to bullet IDs
        scores = []
        bullet_ids = []
        
        for hit in results:
            point_id = hit.id
            score = hit.score
            
            # Convert point ID to bullet ID
            if point_id in self.point_id_to_bullet_id:
                bullet_id = self.point_id_to_bullet_id[point_id]
            elif hit.payload and "bullet_id" in hit.payload:
                # Fallback: get from payload and update mapping
                bullet_id = hit.payload["bullet_id"]
                self.point_id_to_bullet_id[point_id] = bullet_id
                self.bullet_id_to_point_id[bullet_id] = point_id
            else:
                # Skip if we can't find bullet ID
                continue
            
            bullet_ids.append(bullet_id)
            scores.append(score)
        
        # Map bullet IDs to indices using the mapping
        indices = []
        valid_scores = []
        for bullet_id, score in zip(bullet_ids, scores):
            if bullet_id in self.id_to_index:
                indices.append(self.id_to_index[bullet_id])
                valid_scores.append(score)
        
        return valid_scores, indices
    
    def update_id_mapping(self, id_to_index: dict) -> None:
        """Update the ID to index mapping.
        
        This should be called by PlaybookManager after loading bullets
        to ensure correct mapping.
        
        Args:
            id_to_index: Dictionary mapping bullet IDs to indices
        """
        self.id_to_index = id_to_index
    
    def delete(self, ids: List[str]) -> None:
        """Delete embeddings by bullet IDs from Qdrant collection.
        
        Args:
            ids: List of bullet IDs to delete
        """
        if ids:
            from qdrant_client.models import PointIdsList
            # Convert bullet IDs to Qdrant point IDs
            point_ids = [self._bullet_id_to_point_id(bullet_id) for bullet_id in ids]
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=PointIdsList(points=point_ids)
            )
            
            # Clean up mappings
            for bullet_id in ids:
                if bullet_id in self.bullet_id_to_point_id:
                    point_id = self.bullet_id_to_point_id.pop(bullet_id)
                    self.point_id_to_bullet_id.pop(point_id, None)
    
    def save(self) -> None:
        """Persist Qdrant collection.
        
        Note: Qdrant auto-persists data, but we ensure collection exists.
        """
        # Ensure collection exists
        self.load()
    
    def load(self) -> bool:
        """Load/verify Qdrant collection exists.
        
        Creates collection if it doesn't exist.
        Also rebuilds point_id to bullet_id mapping from existing points.
        
        Returns:
            True if collection exists or was created, False otherwise
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                # Create collection if it doesn't exist
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.dimension,
                        distance=Distance.COSINE
                    )
                )
                return True
            
            # Rebuild point_id to bullet_id mapping from existing points
            # This is needed when loading an existing collection
            try:
                # Scroll through all points to rebuild mapping
                scroll_result = self.client.scroll(
                    collection_name=self.collection_name,
                    limit=10000,  # Adjust if you have more points
                    with_payload=True
                )
                
                for point in scroll_result[0]:  # scroll_result is (points, next_page_offset)
                    if point.payload and "bullet_id" in point.payload:
                        bullet_id = point.payload["bullet_id"]
                        point_id = point.id
                        self.bullet_id_to_point_id[bullet_id] = point_id
                        self.point_id_to_bullet_id[point_id] = bullet_id
            except Exception as e:
                # If scrolling fails, mappings will be rebuilt as points are accessed
                print(f"Warning: Could not rebuild point ID mappings: {e}")
            
            return True
        except Exception as e:
            print(f"Warning: Failed to load/create Qdrant collection: {e}")
            return False
    
    def get_count(self) -> int:
        """Get total number of vectors in Qdrant collection.
        
        Returns:
            Number of vectors
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception:
            return 0
    
    def clear(self) -> None:
        """Clear all vectors from Qdrant collection."""
        try:
            # Delete collection and recreate it
            self.client.delete_collection(self.collection_name)
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=Distance.COSINE
                )
            )
        except Exception as e:
            print(f"Warning: Failed to clear Qdrant collection: {e}")
    
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

