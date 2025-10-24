"""Pytest configuration and fixtures."""

import pytest
import os
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_storage_path():
    """Create temporary storage path for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_openai_key(monkeypatch):
    """Mock OpenAI API key for tests."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key-for-testing")


@pytest.fixture
def sample_bullet_data():
    """Sample bullet data for testing."""
    return {
        "id": "ctx-test123",
        "content": "Always validate user input before processing",
        "section": "Security",
        "helpful_count": 5,
        "harmful_count": 1,
        "tags": ["validation", "security"]
    }


@pytest.fixture
def sample_bullets():
    """Multiple sample bullets for testing."""
    return [
        {
            "content": "Validate payment amount before processing",
            "section": "Payment",
            "tags": ["validation", "payment"]
        },
        {
            "content": "Log all failed transactions",
            "section": "Logging",
            "tags": ["logging", "errors"]
        },
        {
            "content": "Encrypt sensitive data before storage",
            "section": "Security",
            "tags": ["encryption", "security"]
        }
    ]

