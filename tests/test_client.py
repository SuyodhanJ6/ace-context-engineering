import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import tempfile
from ace.client import ACEClient

class TestACEClient(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Mock embedding and chat model initialization
        self.mock_init_embeddings = patch('ace.playbook.manager.init_embeddings').start()
        self.mock_init_chat_model = patch('ace.reflector.init_chat_model').start()
        
        # Setup fake embedding model
        self.fake_embedder = MagicMock()
        self.fake_embedder.embed_query.return_value = [0.1] * 1536  # Standard dimension
        self.mock_init_embeddings.return_value = self.fake_embedder
        
        # Setup fake chat model
        self.fake_llm = MagicMock()
        self.mock_init_chat_model.return_value = self.fake_llm
        
        # Initialize the ACEClient pointing to the temp dir
        self.ace = ACEClient(
            playbook_name="test_client",
            vector_store="faiss",
            storage_path=self.test_dir
        )
        
        # Mock the internal pipeline to avoid background thread race conditions during cleanup
        self.ace._process_feedback_pipeline = MagicMock()
        
        # Seed the playbook with 2 dummy rules
        self.ace.playbook.add_bullet("Dummy rule 1: Always respond politely.", section="Guidelines")
        self.ace.playbook.add_bullet("Dummy rule 2: Return output in JSON format.", section="Formatting")

    def tearDown(self):
        # Stop mocks
        patch.stopall()
        # Clean up the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_get_context(self):
        # Call get_context and assert it returns markdown and an interaction_id
        context_string, interaction_id = self.ace.get_context("How should I respond?")
        
        self.assertTrue(isinstance(context_string, str))
        self.assertTrue(len(context_string) > 0)
        self.assertTrue("Dummy rule" in context_string)
        
        self.assertTrue(isinstance(interaction_id, str))
        self.assertTrue(len(interaction_id) > 0)
        
        # Ensure interaction_id is stored internally
        self.assertIn(interaction_id, self.ace._interactions)

    def test_submit_feedback(self):
        # Get context to generate an interaction ID
        _, interaction_id = self.ace.get_context("Please format as JSON")
        
        # Submit feedback (synchronous fire-and-forget uses a background thread)
        success = self.ace.submit_feedback(
            interaction_id=interaction_id,
            user_feedback="Great JSON output!",
            rating=5,
            model_response='{"status": "success"}'
        )
        self.assertTrue(success)

if __name__ == "__main__":
    unittest.main()
