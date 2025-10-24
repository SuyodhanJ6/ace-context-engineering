"""Path management utilities for ACE framework."""

import os
from pathlib import Path
from typing import Optional


def get_default_storage_path(playbook_name: str = "default") -> Path:
    """Get default storage path for ACE data.
    
    Creates a path in the current working directory (like .venv):
    ./.ace/playbooks/{playbook_name}/
    
    Args:
        playbook_name: Name of the playbook
        
    Returns:
        Path object for storage directory
    """
    return Path.cwd() / ".ace" / "playbooks" / playbook_name


def ensure_path_exists(path: Path) -> Path:
    """Ensure path exists, creating directories if needed.
    
    Args:
        path: Path to create
        
    Returns:
        The same path object
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_playbook_path(storage_path: Path) -> Path:
    """Get path for playbook markdown file.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to playbook.md file
    """
    return storage_path / "playbook.md"


def get_metadata_path(storage_path: Path) -> Path:
    """Get path for playbook metadata file.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to metadata.json file
    """
    return storage_path / "metadata.json"


def get_reflections_path(storage_path: Path) -> Path:
    """Get path for reflections directory.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to reflections directory
    """
    reflections_path = storage_path / "reflections"
    ensure_path_exists(reflections_path)
    return reflections_path


def get_updates_path(storage_path: Path) -> Path:
    """Get path for updates/deltas directory.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to updates directory
    """
    updates_path = storage_path / "updates"
    ensure_path_exists(updates_path)
    return updates_path


def get_feedback_path(storage_path: Path) -> Path:
    """Get path for feedback storage directory.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to feedback directory
    """
    feedback_path = storage_path / "feedback"
    ensure_path_exists(feedback_path)
    return feedback_path


def get_chat_storage_path(storage_path: Path) -> Path:
    """Get path for chat storage directory.
    
    Args:
        storage_path: Base storage path
        
    Returns:
        Path to chat_storage directory
    """
    chat_path = storage_path / "chat_storage"
    ensure_path_exists(chat_path)
    return chat_path

