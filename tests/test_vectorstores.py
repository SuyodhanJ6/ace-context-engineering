"""Tests for vector store implementations."""

import pytest
import numpy as np
from ace.vectorstores.faiss import FAISSVectorStore


class TestFAISSVectorStore:
    """Test FAISS vector store."""
    
    def test_initialization(self, temp_storage_path):
        """Test FAISS store initialization."""
        store = FAISSVectorStore(
            storage_path=str(temp_storage_path),
            dimension=384
        )
        
        assert store.dimension == 384
        assert store.count() == 0
    
    def test_add_and_search(self, temp_storage_path):
        """Test adding and searching embeddings."""
        store = FAISSVectorStore(
            storage_path=str(temp_storage_path),
            dimension=384
        )
        
        # Create sample embeddings
        texts = ["test1", "test2", "test3"]
        embeddings = np.random.rand(3, 384)
        ids = ["id1", "id2", "id3"]
        
        # Add embeddings
        store.add_embeddings(texts, embeddings, ids)
        
        assert store.count() == 3
        
        # Search
        query_embedding = np.random.rand(384)
        scores, indices = store.search(query_embedding, top_k=2)
        
        assert len(scores) == 2
        assert len(indices) == 2
    
    def test_save_and_load(self, temp_storage_path):
        """Test saving and loading index."""
        store = FAISSVectorStore(
            storage_path=str(temp_storage_path),
            dimension=384
        )
        
        # Add data
        embeddings = np.random.rand(5, 384)
        store.add_embeddings(
            ["t1", "t2", "t3", "t4", "t5"],
            embeddings,
            ["id1", "id2", "id3", "id4", "id5"]
        )
        
        # Save
        store.save()
        
        # Create new store and load
        new_store = FAISSVectorStore(
            storage_path=str(temp_storage_path),
            dimension=384
        )
        
        assert new_store.count() == 5
    
    def test_clear(self, temp_storage_path):
        """Test clearing the index."""
        store = FAISSVectorStore(
            storage_path=str(temp_storage_path),
            dimension=384
        )
        
        # Add data
        embeddings = np.random.rand(3, 384)
        store.add_embeddings(["t1", "t2", "t3"], embeddings, ["id1", "id2", "id3"])
        
        assert store.count() == 3
        
        # Clear
        store.clear()
        
        assert store.count() == 0

