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
        vector_store: Type of vector store ("faiss" or "chromadb")
        storage_path: Custom storage path (default: ~/.ace/playbooks/{playbook_name})
        chat_model: Model name for chat operations (LangChain format: "provider:model")
        embedding_model: Model name for embeddings (LangChain format: "provider:model")
        temperature: Temperature for LLM calls
        top_k: Number of relevant bullets to retrieve
        deduplication_threshold: Cosine similarity threshold for deduplication
        max_epochs: Maximum number of learning epochs
    
    Example:
        >>> config = ACEConfig(
        ...     playbook_name="my_app",
        ...     vector_store="faiss",
        ...     chat_model="openai:gpt-4o-mini"
        ... )
    """
    playbook_name: str = "default"
    vector_store: str = "faiss"  # "faiss" or "chromadb"
    storage_path: Optional[str] = None
    chat_model: str = "openai:gpt-4o-mini"
    embedding_model: str = "openai:text-embedding-3-small"
    temperature: float = 0.3
    top_k: int = 10
    deduplication_threshold: float = 0.9
    max_epochs: int = 5
    enable_tracing: bool = False
    log_level: str = "INFO"
    
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
        if self.vector_store not in ["faiss", "chromadb"]:
            raise ValueError(
                f"Invalid vector_store: {self.vector_store}. Must be 'faiss' or 'chromadb'"
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
