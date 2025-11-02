"""Integration tests for ACE package."""

import pytest
import os
from ace import ACEConfig, PlaybookManager, Reflector, Curator
from ace.playbook.bullet import Bullet


class TestACEIntegration:
    """Integration tests for ACE components."""
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required"
    )
    def test_playbook_manager_with_api(self, temp_storage_path):
        """Test PlaybookManager with real API."""
        playbook = PlaybookManager(
            playbook_dir=str(temp_storage_path),
            vector_store="faiss",
            embedding_model="openai:text-embedding-3-small"
        )
        
        # Add bullets
        bullet_id = playbook.add_bullet(
            content="Always validate inputs",
            section="Security"
        )
        
        assert bullet_id is not None
        assert len(playbook.bullets) == 1
        
        # Get stats
        stats = playbook.get_stats()
        assert stats["total_bullets"] == 1
        assert "Security" in stats["sections"]
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required"
    )
    def test_reflector_initialization(self, temp_storage_path):
        """Test Reflector initialization."""
        reflector = Reflector(
            model="openai:gpt-4o-mini",
            storage_path=str(temp_storage_path),
            max_refinement_iterations=2
        )
        
        assert reflector.max_refinement_iterations == 2
        # Just check it initialized correctly
        assert str(reflector.storage_path) == str(temp_storage_path)
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required for embedding model"
    )
    def test_curator_initialization(self, temp_storage_path):
        """Test Curator initialization."""
        playbook = PlaybookManager(
            playbook_dir=str(temp_storage_path),
            vector_store="faiss",
            embedding_model="openai:text-embedding-3-small"
        )
        
        curator = Curator(
            playbook_manager=playbook,
            storage_path=str(temp_storage_path)
        )
        
        # Just check it initialized correctly
        assert str(curator.storage_path) == str(temp_storage_path)
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required for embedding model"
    )
    def test_config_to_playbook_flow(self, temp_storage_path):
        """Test creating PlaybookManager from ACEConfig."""
        config = ACEConfig(
            playbook_name="test_app",
            storage_path=str(temp_storage_path),
            vector_store="faiss",
            top_k=5
        )
        
        playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store=config.vector_store,
            embedding_model=config.embedding_model
        )
        
        assert str(playbook.playbook_dir) == str(config.get_storage_path())


class TestBulletWorkflow:
    """Test complete bullet workflow."""
    
    def test_bullet_lifecycle(self):
        """Test complete bullet lifecycle."""
        # Create
        bullet = Bullet.create(
            content="Test strategy",
            section="Testing"
        )
        
        assert bullet.helpful_count == 0
        assert bullet.is_neutral
        
        # Mark helpful
        bullet.mark_helpful()
        bullet.mark_helpful()
        assert bullet.is_helpful
        
        # Mark harmful
        bullet.mark_harmful()
        assert bullet.net_score == 1
        
        # Serialize
        data = bullet.to_dict()
        
        # Deserialize
        restored = Bullet.from_dict(data)
        assert restored.net_score == bullet.net_score
        assert restored.content == bullet.content

