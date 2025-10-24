"""Tests for Bullet class."""

import pytest
from datetime import datetime
from ace.playbook.bullet import Bullet


class TestBullet:
    """Test Bullet class functionality."""
    
    def test_create_bullet(self):
        """Test creating a new bullet."""
        bullet = Bullet.create(
            content="Test strategy",
            section="Testing",
            tags=["test"]
        )
        
        assert bullet.id.startswith("ctx-")
        assert bullet.content == "Test strategy"
        assert bullet.section == "Testing"
        assert bullet.tags == ["test"]
        assert bullet.helpful_count == 0
        assert bullet.harmful_count == 0
    
    def test_mark_helpful(self):
        """Test marking bullet as helpful."""
        bullet = Bullet.create(content="Test")
        bullet.mark_helpful()
        
        assert bullet.helpful_count == 1
        assert bullet.is_helpful
    
    def test_mark_harmful(self):
        """Test marking bullet as harmful."""
        bullet = Bullet.create(content="Test")
        bullet.mark_harmful()
        
        assert bullet.harmful_count == 1
        assert bullet.is_harmful
    
    def test_net_score(self):
        """Test net score calculation."""
        bullet = Bullet.create(content="Test")
        bullet.mark_helpful()
        bullet.mark_helpful()
        bullet.mark_harmful()
        
        assert bullet.net_score == 1
        assert bullet.is_helpful
    
    def test_to_dict_from_dict(self):
        """Test serialization and deserialization."""
        original = Bullet.create(
            content="Test strategy",
            section="Testing",
            tags=["test"]
        )
        original.mark_helpful()
        
        # Serialize
        data = original.to_dict()
        
        # Deserialize
        restored = Bullet.from_dict(data)
        
        assert restored.id == original.id
        assert restored.content == original.content
        assert restored.section == original.section
        assert restored.helpful_count == original.helpful_count
        assert restored.tags == original.tags
    
    def test_to_markdown(self):
        """Test markdown conversion."""
        bullet = Bullet.create(
            content="Test strategy",
            section="Testing",
            tags=["test"]
        )
        bullet.mark_helpful()
        
        markdown = bullet.to_markdown()
        
        assert bullet.id in markdown
        assert "Test strategy" in markdown
        assert "+1" in markdown  # helpful count

