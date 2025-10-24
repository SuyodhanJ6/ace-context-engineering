"""Tests for ACE configuration."""

import pytest
from pathlib import Path
from ace.config import ACEConfig


class TestACEConfig:
    """Test ACEConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = ACEConfig(playbook_name="test_app")
        
        assert config.playbook_name == "test_app"
        assert config.vector_store == "faiss"
        assert config.top_k == 10
        assert config.temperature == 0.3
        assert config.deduplication_threshold == 0.9
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = ACEConfig(
            playbook_name="custom_app",
            vector_store="chromadb",
            top_k=5,
            temperature=0.5
        )
        
        assert config.playbook_name == "custom_app"
        assert config.vector_store == "chromadb"
        assert config.top_k == 5
        assert config.temperature == 0.5
    
    def test_custom_storage_path(self, temp_storage_path):
        """Test custom storage path."""
        config = ACEConfig(
            playbook_name="test_app",
            storage_path=str(temp_storage_path)
        )
        
        assert Path(config.storage_path) == temp_storage_path
        assert Path(config.get_storage_path()) == temp_storage_path
    
    def test_invalid_vector_store(self):
        """Test invalid vector store raises error."""
        with pytest.raises(ValueError, match="Invalid vector_store"):
            ACEConfig(
                playbook_name="test",
                vector_store="invalid"
            )
    
    def test_model_config(self):
        """Test model configuration."""
        config = ACEConfig(
            playbook_name="test",
            chat_model="openai:gpt-4",
            embedding_model="openai:text-embedding-3-large"
        )
        
        assert config.chat_model == "openai:gpt-4"
        assert config.embedding_model == "openai:text-embedding-3-large"

