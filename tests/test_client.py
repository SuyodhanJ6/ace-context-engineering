import unittest
import os
import shutil
import tempfile
from ace.client import ACEClient
from ace.playbook.manager import PlaybookManager

class TestACEClient(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Initialize the ACEClient pointing to the temp dir
        self.ace = ACEClient(
            playbook_name="test_client",
            vector_store="faiss",
            storage_path=self.test_dir
        )
        
        # Seed the playbook with 2 dummy rules as per implementation plan
        self.ace.playbook.add_bullet("Dummy rule 1: Always respond politely.", section="Guidelines")
        self.ace.playbook.add_bullet("Dummy rule 2: Return output in JSON format.", section="Formatting")

    def tearDown(self):
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
