"""Configuration classes for ACE Framework."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
import os
from ace.utils.paths import get_default_storage_path, ensure_path_exists


@dataclass
class ACEConfig:
    """Main configuration for ACE components.
    
    This configuration follows LangChain best practices with production-ready defaults.
    Users can customize storage paths, vector stores, and models.
    
    Args:
        playbook_name: Name of the playbook (used for storage path)
        vector_store: Type of vector store ("faiss", "chromadb", "qdrant", or "qdrant-cloud")
        storage_path: Custom storage path (default: ~/.ace/playbooks/{playbook_name})
        chat_model: Model name for chat operations (LangChain format: "provider:model")
        embedding_model: Model name for embeddings (LangChain format: "provider:model")
        temperature: Temperature for LLM calls
        top_k: Number of relevant bullets to retrieve
        deduplication_threshold: Cosine similarity threshold for deduplication
        max_epochs: Maximum number of learning epochs
        enable_tracing: Enable tracing for debugging
        log_level: Logging level
        qdrant_url: Qdrant server URL (default: "http://localhost:6333" for local Docker)
        qdrant_api_key: Qdrant API key (required for "qdrant-cloud", optional for "qdrant")
    
    Defaults:
        playbook_name: "default"
        vector_store: "faiss"
        storage_path: None (auto-generated as ~/.ace/playbooks/{playbook_name})
        chat_model: "openai:gpt-4o-mini"
        embedding_model: "openai:text-embedding-3-small"
        temperature: 0.3
        top_k: 10
        deduplication_threshold: 0.9
        max_epochs: 5
        enable_tracing: False
        log_level: "INFO"
        qdrant_url: "http://localhost:6333"
        qdrant_api_key: None (loaded from QDRANT_API_KEY env var for qdrant-cloud if not provided)
    
    Note:
        For Qdrant vector stores:
        - Playbook metadata (JSON files) → Stored LOCALLY in playbook_dir
        - Vector embeddings → Stored EXTERNALLY in Qdrant server
        - For "qdrant-cloud": qdrant_api_key is required (from config or QDRANT_API_KEY env var)
    
    Example:
        >>> # FAISS (local vectors)
        >>> config = ACEConfig(
        ...     playbook_name="my_app",
        ...     vector_store="faiss",
        ...     chat_model="openai:gpt-4o-mini"
        ... )
        >>> 
        >>> # Qdrant local (Docker)
        >>> config = ACEConfig(
        ...     playbook_name="my_app",
        ...     vector_store="qdrant",
        ...     qdrant_url="http://localhost:6333"
        ... )
        >>> 
        >>> # Qdrant Cloud
        >>> config = ACEConfig(
        ...     playbook_name="my_app",
        ...     vector_store="qdrant-cloud",
        ...     qdrant_url="https://your-cluster.qdrant.io",
        ...     qdrant_api_key="your-api-key"
        ... )
    """
    playbook_name: str = "default"
    vector_store: str = "faiss"  # "faiss", "chromadb", "qdrant", or "qdrant-cloud"
    storage_path: Optional[str] = None
    chat_model: str = "openai:gpt-4o-mini"
    embedding_model: str = "openai:text-embedding-3-small"
    temperature: float = 0.3
    top_k: int = 10
    deduplication_threshold: float = 0.9
    max_epochs: int = 5
    enable_tracing: bool = False
    log_level: str = "INFO"
    qdrant_url: Optional[str] = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    
    def __post_init__(self):
        """Set up storage path and validate configuration."""
        # Set up storage path
        if self.storage_path is None:
            self._storage_path = get_default_storage_path(self.playbook_name)
        else:
            self._storage_path = Path(self.storage_path)
        
        # Ensure storage path exists
        ensure_path_exists(self._storage_path)
        
        # Validate vector store type
        valid_stores = ["faiss", "chromadb", "qdrant", "qdrant-cloud"]
        if self.vector_store not in valid_stores:
            raise ValueError(
                f"Invalid vector_store: {self.vector_store}. Must be one of {valid_stores}"
            )
        
        # Handle Qdrant Cloud API key from environment
        if self.vector_store == "qdrant-cloud" and self.qdrant_api_key is None:
            self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
            if self.qdrant_api_key is None:
                raise ValueError(
                    "qdrant_api_key is required for 'qdrant-cloud'. "
                    "Provide it in config or set QDRANT_API_KEY environment variable."
                )
    
    @property
    def storage_path_obj(self) -> Path:
        """Get storage path as Path object.
        
        Returns:
            Path object for storage directory
        """
        return self._storage_path
    
    def get_storage_path(self) -> str:
        """Get storage path as string.
        
        Returns:
            String path to storage directory
        """
        return str(self._storage_path)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ACEConfig":
        """Create config from dictionary.
        
        Args:
            config_dict: Dictionary of configuration parameters
            
        Returns:
            ACEConfig instance
        """
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary.
        
        Returns:
            Dictionary representation of configuration
        """
        return {
            "playbook_name": self.playbook_name,
            "vector_store": self.vector_store,
            "storage_path": str(self._storage_path),
            "chat_model": self.chat_model,
            "embedding_model": self.embedding_model,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "deduplication_threshold": self.deduplication_threshold,
            "max_epochs": self.max_epochs,
            "enable_tracing": self.enable_tracing,
            "log_level": self.log_level,
            "qdrant_url": self.qdrant_url,
            "qdrant_api_key": self.qdrant_api_key,
        }


@dataclass
class ModelConfig:
    """Configuration for a model (legacy support).
    
    This is kept for backwards compatibility with existing code.
    New code should use ACEConfig instead.
    """
    name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: int = 30
    
    def __post_init__(self):
        """Set default API key from environment if not provided."""
        if not self.api_key:
            if "openai" in self.name.lower():
                self.api_key = os.getenv("OPENAI_API_KEY")
            elif "anthropic" in self.name.lower():
                self.api_key = os.getenv("ANTHROPIC_API_KEY")
