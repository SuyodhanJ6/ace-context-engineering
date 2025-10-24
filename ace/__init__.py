"""
ACE Context Engineering - Agentic Context Engineering Framework

A framework for evolving contexts that enable self-improving language models
through structured playbooks, reflection, and curation.

Based on the research paper:
"Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"
Authors: Qizheng Zhang, Changran Hu, et al.

GitHub: https://github.com/SuyodhanJ6/ace-context-engineering
"""

__version__ = "0.1.0"
__author__ = "Suyodhan J"
__email__ = "suyodhanj6@gmail.com"

# Core components
from ace.reflector import Reflector, ReflectionInsight
from ace.curator import Curator, DeltaUpdate, DeltaOperation
from ace.agent import ACEAgent

# Playbook management
from ace.playbook.manager import PlaybookManager
from ace.playbook.bullet import Bullet

# Configuration
from ace.config import ACEConfig, ModelConfig

# Prompts
from ace.prompts import ReflectorPrompts

# Vector stores
from ace.vectorstores.base import VectorStoreBase
from ace.vectorstores.faiss import FAISSVectorStore

__all__ = [
    # Core components
    "Reflector",
    "ReflectionInsight",
    "Curator",
    "DeltaUpdate",
    "DeltaOperation",
    "ACEAgent",
    
    # Playbook management
    "PlaybookManager",
    "Bullet",
    
    # Configuration
    "ACEConfig",
    "ModelConfig",
    
    # Prompts
    "ReflectorPrompts",
    
    # Vector stores
    "VectorStoreBase",
    "FAISSVectorStore",
]

# Conditionally export ChromaDB if available
try:
    from ace.vectorstores.chromadb import ChromaDBVectorStore
    __all__.append("ChromaDBVectorStore")
except ImportError:
    pass
