"""Tests for utility functions."""

import pytest
from pathlib import Path
from ace.utils.paths import (
    get_default_storage_path,
    ensure_path_exists,
    get_playbook_path,
    get_metadata_path
)
from ace.utils.env import (
    get_api_key,
    check_api_keys,
    load_env
)


class TestPathUtils:
    """Test path utility functions."""
    
    def test_get_default_storage_path(self):
        """Test default storage path generation."""
        path = get_default_storage_path("test_app")
        
        assert isinstance(path, Path)
        assert path.name == "test_app"
        assert "playbooks" in str(path)
        assert ".ace" in str(path)
    
    def test_ensure_path_exists(self, temp_storage_path):
        """Test path creation."""
        test_path = temp_storage_path / "test" / "nested" / "path"
        
        result = ensure_path_exists(test_path)
        
        assert result.exists()
        assert result.is_dir()
    
    def test_get_playbook_path(self, temp_storage_path):
        """Test playbook path."""
        path = get_playbook_path(temp_storage_path)
        
        assert path.name == "playbook.md"
        assert path.parent == temp_storage_path
    
    def test_get_metadata_path(self, temp_storage_path):
        """Test metadata path."""
        path = get_metadata_path(temp_storage_path)
        
        assert path.name == "metadata.json"
        assert path.parent == temp_storage_path


class TestEnvUtils:
    """Test environment utility functions."""
    
    def test_get_api_key_openai(self, monkeypatch):
        """Test getting OpenAI API key."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        
        key = get_api_key("openai")
        
        assert key == "sk-test-key"
    
    def test_get_api_key_custom(self, monkeypatch):
        """Test getting custom API key."""
        monkeypatch.setenv("MY_CUSTOM_KEY", "custom-value")
        
        key = get_api_key("custom", "MY_CUSTOM_KEY")
        
        assert key == "custom-value"
    
    def test_get_api_key_not_set(self):
        """Test getting unset API key."""
        key = get_api_key("nonexistent")
        
        assert key is None
    
    def test_check_api_keys(self, monkeypatch):
        """Test checking multiple API keys."""
        monkeypatch.setenv("OPENAI_API_KEY", "test")
        
        results = check_api_keys(["openai", "anthropic"], verbose=False)
        
        assert results["openai"] is True
        assert results["anthropic"] is False

