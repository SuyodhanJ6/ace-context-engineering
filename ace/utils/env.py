"""
Environment variable management utilities.

Automatically loads .env files for API keys and configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv, find_dotenv


def load_env(env_file: Optional[str] = None, verbose: bool = False) -> bool:
    """Load environment variables from .env file.
    
    Automatically searches for .env file in:
    1. Current directory
    2. Parent directories (up to root)
    3. Custom path if provided
    
    Args:
        env_file: Optional path to specific .env file
        verbose: Print loading information
        
    Returns:
        True if .env file was found and loaded
        
    Example:
        >>> from ace.utils import load_env
        >>> load_env()  # Loads from .env file
        >>> # Or specify custom path
        >>> load_env("/path/to/custom/.env")
    """
    if env_file:
        # Load from specific file
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path, verbose=verbose)
            if verbose:
                print(f" Loaded environment from: {env_path}")
            return True
        else:
            if verbose:
                print(f"  Environment file not found: {env_path}")
            return False
    else:
        # Auto-find .env file
        env_path = find_dotenv()
        if env_path:
            load_dotenv(env_path, verbose=verbose)
            if verbose:
                print(f" Loaded environment from: {env_path}")
            return True
        else:
            if verbose:
                print("ℹ  No .env file found (using system environment variables)")
            return False


def get_api_key(service: str, env_var: Optional[str] = None) -> Optional[str]:
    """Get API key from environment variables.
    
    Args:
        service: Service name (e.g., "openai", "anthropic")
        env_var: Optional custom environment variable name
        
    Returns:
        API key if found, None otherwise
        
    Example:
        >>> from ace.utils import get_api_key
        >>> openai_key = get_api_key("openai")
        >>> # Or custom variable
        >>> key = get_api_key("custom", "MY_CUSTOM_KEY")
    """
    if env_var:
        return os.getenv(env_var)
    
    # Map service names to common environment variable names
    env_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "cohere": "COHERE_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY",
        "together": "TOGETHER_API_KEY",
        "groq": "GROQ_API_KEY",
        "mistral": "MISTRAL_API_KEY",
    }
    
    env_var_name = env_map.get(service.lower())
    if env_var_name:
        return os.getenv(env_var_name)
    
    # Try uppercase version of service name
    return os.getenv(f"{service.upper()}_API_KEY")


def check_api_keys(required: list = None, verbose: bool = True) -> dict:
    """Check which API keys are set in environment.
    
    Args:
        required: List of required services (e.g., ["openai", "anthropic"])
        verbose: Print results
        
    Returns:
        Dictionary of service -> bool (whether key is set)
        
    Example:
        >>> from ace.utils import check_api_keys
        >>> check_api_keys(["openai"])
        {'openai': True}
    """
    services = required or ["openai", "anthropic"]
    results = {}
    
    if verbose:
        print(" Checking API keys...")
    
    for service in services:
        key = get_api_key(service)
        results[service] = bool(key)
        
        if verbose:
            if key:
                print(f"    {service.upper()}: Set")
            else:
                print(f"    {service.upper()}: Not set")
    
    return results


def ensure_api_key(service: str, env_var: Optional[str] = None) -> str:
    """Ensure API key is set, raise error if not.
    
    Args:
        service: Service name (e.g., "openai")
        env_var: Optional custom environment variable name
        
    Returns:
        API key
        
    Raises:
        ValueError: If API key is not set
        
    Example:
        >>> from ace.utils import ensure_api_key
        >>> key = ensure_api_key("openai")
    """
    key = get_api_key(service, env_var)
    if not key:
        var_name = env_var or f"{service.upper()}_API_KEY"
        raise ValueError(
            f"API key not found. Please set {var_name} environment variable.\n"
            f"You can:\n"
            f"1. Create a .env file with: {var_name}=your-key-here\n"
            f"2. Set in terminal: export {var_name}=your-key-here\n"
            f"3. Load with: from ace.utils import load_env; load_env()"
        )
    return key


# Auto-load .env on import (optional, can be disabled)
_AUTO_LOAD_ENV = os.getenv("ACE_AUTO_LOAD_ENV", "true").lower() == "true"

if _AUTO_LOAD_ENV:
    # Silently try to load .env file on import
    load_env(verbose=False)

