"""
PlaybookManager - Manages ACE playbooks with vector store abstraction.

Refactored to use LangChain patterns and support both FAISS and ChromaDB.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import numpy as np

from langchain.embeddings import init_embeddings
from ace.playbook.bullet import Bullet
from ace.vectorstores.base import VectorStoreBase
from ace.vectorstores.faiss import FAISSVectorStore
from ace.utils.paths import get_playbook_path, get_metadata_path


class PlaybookManager:
    """Manages playbook with vector store abstraction for semantic retrieval.
    
    Supports both FAISS and ChromaDB backends with LangChain embeddings.
    
    Args:
        playbook_dir: Directory for storing playbook data
        vector_store: Type of vector store ("faiss" or "chromadb")
        embedding_model: Model name for embeddings (LangChain format)
        embedding_dim: Dimension of embeddings (default: 1536 for text-embedding-3-small)
    
    Example:
        >>> from ace.config import ACEConfig
        >>> config = ACEConfig(playbook_name="my_app", vector_store="faiss")
        >>> manager = PlaybookManager(
        ...     playbook_dir=config.get_storage_path(),
        ...     vector_store=config.vector_store,
        ...     embedding_model=config.embedding_model
        ... )
    """
    
    def __init__(
        self,
        playbook_dir: Optional[str] = None,
        vector_store: str = "faiss",
        embedding_model: str = "openai:text-embedding-3-small",
        embedding_dim: int = 1536,
        qdrant_url: Optional[str] = None,
        qdrant_api_key: Optional[str] = None
    ):
        """Initialize PlaybookManager with vector store and embeddings.
        
        Args:
            playbook_dir: Directory for storing playbook data
            vector_store: Type of vector store ("faiss", "chromadb", "qdrant", or "qdrant-cloud")
            embedding_model: Model name for embeddings (LangChain format)
            embedding_dim: Dimension of embeddings (default: 1536)
            qdrant_url: Qdrant server URL (required for qdrant/qdrant-cloud)
            qdrant_api_key: Qdrant API key (required for qdrant-cloud, optional for qdrant)
        """
        # Set up storage path
        if playbook_dir is None:
            playbook_dir = str(Path.home() / ".ace" / "playbooks" / "default")
        
        self.playbook_dir = Path(playbook_dir)
        self.playbook_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model using LangChain
        print(f" Initializing embedding model: {embedding_model}")
        self.embedding_model = init_embeddings(embedding_model)
        self.embedding_dim = embedding_dim
        
        # Initialize vector store based on type
        print(f" Initializing {vector_store} vector store...")
        if vector_store == "faiss":
            self.vector_store: VectorStoreBase = FAISSVectorStore(
                storage_path=str(self.playbook_dir),
                dimension=embedding_dim
            )
        elif vector_store == "chromadb":
            # ChromaDB is optional dependency
            try:
                from ace.vectorstores.chromadb import ChromaDBVectorStore
                self.vector_store = ChromaDBVectorStore(
                    storage_path=str(self.playbook_dir),
                    dimension=embedding_dim
                )
            except ImportError:
                raise ImportError(
                    "ChromaDB is not installed. Install with: pip install chromadb"
                )
        elif vector_store in ["qdrant", "qdrant-cloud"]:
            # Qdrant is optional dependency
            try:
                from ace.vectorstores.qdrant import QdrantVectorStore
                
                # Extract collection name from playbook directory
                collection_name = self._extract_collection_name()
                
                # Get Qdrant URL (use provided or default)
                qdrant_url_value = qdrant_url or "http://localhost:6333"
                
                # For qdrant-cloud, API key is required
                if vector_store == "qdrant-cloud" and not qdrant_api_key:
                    raise ValueError(
                        "qdrant_api_key is required for 'qdrant-cloud'. "
                        "Provide it or set QDRANT_API_KEY environment variable."
                    )
                
                self.vector_store = QdrantVectorStore(
                    storage_path=str(self.playbook_dir),
                    dimension=embedding_dim,
                    url=qdrant_url_value,
                    api_key=qdrant_api_key,
                    collection_name=collection_name
                )
                
                # Note: Playbook metadata (bullets JSON) is stored locally,
                # but vector embeddings are stored externally in Qdrant server
            except ImportError:
                raise ImportError(
                    "Qdrant client is not installed. Install with: pip install qdrant-client"
                )
        else:
            raise ValueError(
                f"Unsupported vector store: {vector_store}. "
                f"Must be one of: 'faiss', 'chromadb', 'qdrant', 'qdrant-cloud'"
            )
        
        # Bullet storage
        self.bullets: List[Bullet] = []
        self.bullet_id_to_index: Dict[str, int] = {}
        
        # File paths
        self.playbook_file = get_playbook_path(self.playbook_dir)
        self.metadata_file = get_metadata_path(self.playbook_dir)
        
        print(f" Playbook directory: {self.playbook_dir}")
        print(f" Loading existing playbook...")
        
        # Load existing playbook
        self.load_playbook()
        
        # Update ID mapping for Qdrant (if using Qdrant)
        if vector_store in ["qdrant", "qdrant-cloud"]:
            self._update_qdrant_id_mapping()
        
        print(f" PlaybookManager initialized with {len(self.bullets)} bullets")
    
    def add_bullet(self, content: str, section: str = "General") -> str:
        """Add new bullet to playbook.
        
        Args:
            content: Bullet content
            section: Section name
            
        Returns:
            Bullet ID
        """
        # Create bullet
        bullet = Bullet.create(content=content, section=section)
        bullet_id = bullet.id
        
        print(f" Creating bullet {bullet_id} in section '{section}'")
        
        # Add to list
        self.bullets.append(bullet)
        self.bullet_id_to_index[bullet_id] = len(self.bullets) - 1
        
        # Generate embedding
        embedding = self._get_embedding(content)
        
        # Add to vector store
        self.vector_store.add_embeddings(
            texts=[content],
            embeddings=embedding.reshape(1, -1),
            ids=[bullet_id]
        )
        
        # Update ID mapping for Qdrant (if using Qdrant)
        if hasattr(self.vector_store, 'update_id_mapping'):
            self.vector_store.update_id_mapping(self.bullet_id_to_index)
        
        # Save updated playbook
        self.save_playbook()
        
        print(f" Added bullet {bullet_id}")
        return bullet_id
    
    def update_counters(self, bullet_id: str, helpful: bool = True) -> bool:
        """Update helpful/harmful counters for a bullet.
        
        Args:
            bullet_id: Bullet ID
            helpful: True for helpful, False for harmful
            
        Returns:
            True if successful
        """
        if bullet_id not in self.bullet_id_to_index:
            return False
        
        index = self.bullet_id_to_index[bullet_id]
        bullet = self.bullets[index]
        
        if helpful:
            bullet.mark_helpful()
        else:
            bullet.mark_harmful()
        
        bullet.last_used = datetime.now().isoformat()
        
        # Save updated playbook
        self.save_playbook()
        
        return True
    
    def retrieve_relevant(self, query: str, top_k: int = 10) -> List[Bullet]:
        """Retrieve most relevant bullets for a query.
        
        Args:
            query: Search query
            top_k: Number of bullets to return
            
        Returns:
            List of relevant bullets
        """
        if not self.bullets:
            print(" Playbook is empty, no bullets to retrieve")
            return []
        
        print(f" Searching playbook for: '{query[:50]}...'")
        
        # Get query embedding
        query_embedding = self._get_embedding(query)
        
        # Search vector store
        scores, indices = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=min(top_k, len(self.bullets))
        )
        
        # Get bullets
        relevant_bullets = []
        for score, idx in zip(scores, indices):
            if 0 <= idx < len(self.bullets):
                bullet = self.bullets[idx]
                # Only return bullets that are more helpful than harmful
                if bullet.helpful_count >= bullet.harmful_count:
                    relevant_bullets.append(bullet)
        
        print(f" Found {len(relevant_bullets)} relevant bullets")
        return relevant_bullets[:top_k]
    
    def deduplicate(self, similarity_threshold: float = 0.9) -> int:
        """Remove duplicate bullets based on semantic similarity.
        
        Args:
            similarity_threshold: Cosine similarity threshold
            
        Returns:
            Number of bullets removed
        """
        if len(self.bullets) < 2:
            return 0
        
        print(f" Deduplicating playbook (threshold: {similarity_threshold})...")
        
        duplicates_removed = 0
        bullets_to_remove = set()
        
        # Compare all pairs
        for i in range(len(self.bullets)):
            if i in bullets_to_remove:
                continue
            
            for j in range(i + 1, len(self.bullets)):
                if j in bullets_to_remove:
                    continue
                
                bullet_i = self.bullets[i]
                bullet_j = self.bullets[j]
                
                # Get embeddings
                emb_i = self._get_embedding(bullet_i.content)
                emb_j = self._get_embedding(bullet_j.content)
                
                # Calculate cosine similarity
                similarity = self._cosine_similarity(emb_i, emb_j)
                
                if similarity >= similarity_threshold:
                    # Merge bullets (keep the one with better ratio)
                    ratio_i = bullet_i.helpful_count / max(bullet_i.harmful_count, 1)
                    ratio_j = bullet_j.helpful_count / max(bullet_j.harmful_count, 1)
                    
                    if ratio_i >= ratio_j:
                        # Merge j into i
                        bullet_i.helpful_count += bullet_j.helpful_count
                        bullet_i.harmful_count += bullet_j.harmful_count
                        bullets_to_remove.add(j)
                    else:
                        # Merge i into j
                        bullet_j.helpful_count += bullet_i.helpful_count
                        bullet_j.harmful_count += bullet_i.harmful_count
                        bullets_to_remove.add(i)
                        break
        
        # Remove duplicates
        if bullets_to_remove:
            self.bullets = [
                bullet for i, bullet in enumerate(self.bullets) 
                if i not in bullets_to_remove
            ]
            duplicates_removed = len(bullets_to_remove)
            
            # Rebuild vector store
            self._rebuild_vector_store()
            
            # Save updated playbook
            self.save_playbook()
            
            print(f" Removed {duplicates_removed} duplicate bullets")
        
        return duplicates_removed
    
    def get_bullet(self, bullet_id: str) -> Optional[Bullet]:
        """Get specific bullet by ID.
        
        Args:
            bullet_id: Bullet ID
            
        Returns:
            Bullet or None
        """
        if bullet_id in self.bullet_id_to_index:
            index = self.bullet_id_to_index[bullet_id]
            return self.bullets[index]
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get playbook statistics.
        
        Returns:
            Dictionary of statistics
        """
        if not self.bullets:
            return {
                "total_bullets": 0,
                "sections": {},
                "helpful_ratio": 0.0,
                "recent_bullets": 0,
                "total_helpful": 0,
                "total_harmful": 0
            }
        
        sections = {}
        total_helpful = 0
        total_harmful = 0
        recent_count = 0
        now = datetime.now()
        
        for bullet in self.bullets:
            # Count by section
            if bullet.section not in sections:
                sections[bullet.section] = 0
            sections[bullet.section] += 1
            
            # Count helpful/harmful
            total_helpful += bullet.helpful_count
            total_harmful += bullet.harmful_count
            
            # Count recent bullets (last 7 days)
            try:
                created = datetime.fromisoformat(bullet.created_at)
                if (now - created).days <= 7:
                    recent_count += 1
            except:
                pass
        
        helpful_ratio = total_helpful / max(total_helpful + total_harmful, 1)
        
        return {
            "total_bullets": len(self.bullets),
            "sections": sections,
            "helpful_ratio": helpful_ratio,
            "recent_bullets": recent_count,
            "total_helpful": total_helpful,
            "total_harmful": total_harmful
        }
    
    def save_playbook(self):
        """Save playbook to files."""
        print(" Saving playbook...")
        
        # Save metadata
        metadata = {
            "bullets": [bullet.to_dict() for bullet in self.bullets],
            "last_updated": datetime.now().isoformat(),
            "total_bullets": len(self.bullets)
        }
        
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save markdown playbook
        with open(self.playbook_file, 'w') as f:
            f.write("# ACE Playbook\n\n")
            f.write(f"Last updated: {datetime.now().isoformat()}\n")
            f.write(f"Total bullets: {len(self.bullets)}\n\n")
            
            # Group by section
            sections = {}
            for bullet in self.bullets:
                if bullet.section not in sections:
                    sections[bullet.section] = []
                sections[bullet.section].append(bullet)
            
            for section, bullets in sections.items():
                f.write(f"## {section}\n\n")
                for bullet in bullets:
                    f.write(f"{bullet.to_markdown()}\n\n")
        
        # Save vector store
        self.vector_store.save()
        
        print(f" Playbook saved with {len(self.bullets)} bullets")
    
    def load_playbook(self):
        """Load playbook from files."""
        if not self.metadata_file.exists():
            print("ℹ  No existing playbook found, starting fresh")
            return
        
        print(f" Loading playbook from {self.metadata_file}")
        
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Load bullets
            self.bullets = []
            for bullet_data in metadata.get("bullets", []):
                bullet = Bullet.from_dict(bullet_data)
                self.bullets.append(bullet)
            
            # Rebuild bullet_id_to_index mapping
            self.bullet_id_to_index = {}
            for i, bullet in enumerate(self.bullets):
                self.bullet_id_to_index[bullet.id] = i
            
            print(f" Loaded {len(self.bullets)} bullets from metadata")
            
            # Load vector store
            loaded = self.vector_store.load()
            if not loaded and self.bullets:
                print("  Vector store not found, rebuilding...")
                self._rebuild_vector_store()
            
        except Exception as e:
            print(f" Error loading playbook: {e}")
            self.bullets = []
            self.bullet_id_to_index = {}
    
    def _extract_collection_name(self) -> str:
        """Extract collection name from playbook directory.
        
        Extracts the last directory name from playbook_dir and sanitizes it
        for use as a Qdrant collection name.
        
        Returns:
            Sanitized collection name
        """
        # Get the last directory name (e.g., /path/to/playbooks/my_app -> my_app)
        collection_name = self.playbook_dir.name
        
        # Sanitize: lowercase and replace invalid chars
        import re
        collection_name = collection_name.lower()
        collection_name = re.sub(r'[^a-z0-9_-]', '_', collection_name)
        collection_name = re.sub(r'_+', '_', collection_name)
        collection_name = collection_name.strip('_')
        
        # Ensure it's not empty
        if not collection_name:
            collection_name = "ace_playbook"
        
        return collection_name
    
    def _update_qdrant_id_mapping(self) -> None:
        """Update ID to index mapping in QdrantVectorStore.
        
        This ensures that Qdrant search results can map bullet IDs back to
        indices in the bullets list.
        """
        if hasattr(self.vector_store, 'update_id_mapping'):
            self.vector_store.update_id_mapping(self.bullet_id_to_index)
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text using LangChain.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            embedding = self.embedding_model.embed_query(text)
            return np.array(embedding, dtype=np.float32)
        except Exception as e:
            print(f" Error getting embedding: {e}")
            return np.zeros(self.embedding_dim, dtype=np.float32)
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Cosine similarity score
        """
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a > 0 and norm_b > 0:
            return float(np.dot(a, b) / (norm_a * norm_b))
        return 0.0
    
    def _rebuild_vector_store(self):
        """Rebuild vector store from current bullets."""
        print(" Rebuilding vector store...")
        
        # Clear existing vector store
        self.vector_store.clear()
        
        # Re-add all bullets
        for i, bullet in enumerate(self.bullets):
            self.bullet_id_to_index[bullet.id] = i
            embedding = self._get_embedding(bullet.content)
            self.vector_store.add_embeddings(
                texts=[bullet.content],
                embeddings=embedding.reshape(1, -1),
                ids=[bullet.id]
            )
        
        # Save vector store
        self.vector_store.save()
        
        print(f" Vector store rebuilt with {len(self.bullets)} bullets")
