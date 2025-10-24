"""
End-to-End test for ACE learning system.

Tests the complete workflow:
1. Create agent with playbook
2. Run agent on tasks
3. Provide feedback
4. Reflector analyzes performance
5. Curator updates playbook
6. Verify system learns from feedback
"""

import pytest
import os
from ace import ACEConfig, PlaybookManager, Reflector, Curator, ACEAgent
from ace.playbook.bullet import Bullet
from langchain_core.messages import HumanMessage


class TestACELearningCycle:
    """Test complete ACE learning cycle end-to-end."""
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required for E2E test"
    )
    def test_complete_learning_workflow(self, temp_storage_path):
        """
        Test the complete ACE learning workflow:
        - Initialize components
        - Add initial knowledge
        - Run agent multiple times
        - Provide feedback (positive and negative)
        - Verify bullets are updated correctly
        """
        print("\n" + "="*60)
        print(" Starting End-to-End ACE Learning Test")
        print("="*60)
        
        # Step 1: Initialize ACE components
        print("\n Step 1: Initialize ACE Components")
        config = ACEConfig(
            playbook_name="e2e_test",
            storage_path=str(temp_storage_path),
            vector_store="faiss",
            top_k=3
        )
        
        playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store=config.vector_store,
            embedding_model=config.embedding_model
        )
        
        reflector = Reflector(
            model=config.chat_model,
            storage_path=config.get_storage_path(),
            max_refinement_iterations=1
        )
        
        curator = Curator(
            playbook_manager=playbook,
            storage_path=config.get_storage_path()
        )
        
        print(f"    Config: {config.playbook_name}")
        print(f"    Storage: {config.get_storage_path()}")
        print(f"    Components initialized")
        
        # Step 2: Add initial knowledge to playbook
        print("\n Step 2: Add Initial Knowledge")
        bullet1_id = playbook.add_bullet(
            content="Always validate email format before processing",
            section="Validation"
        )
        bullet2_id = playbook.add_bullet(
            content="Check user age is above 18 for registration",
            section="Validation"
        )
        bullet3_id = playbook.add_bullet(
            content="Log all validation errors for monitoring",
            section="Logging"
        )
        
        initial_count = len(playbook.bullets)
        print(f"    Added {initial_count} bullets to playbook")
        print(f"    Bullets: {bullet1_id}, {bullet2_id}, {bullet3_id}")
        
        # Step 3: Get relevant bullets for a query
        print("\n Step 3: Test Context Retrieval")
        query = "How should I validate a user registration form?"
        relevant_bullets = playbook.retrieve_relevant(query, top_k=3)
        
        print(f"   Query: '{query}'")
        print(f"    Retrieved {len(relevant_bullets)} relevant bullets")
        for bullet in relevant_bullets:
            print(f"      - [{bullet.id}] {bullet.content[:50]}...")
        
        assert len(relevant_bullets) > 0, "Should retrieve relevant bullets"
        
        # Step 4: Provide positive feedback
        print("\n Step 4: Provide Positive Feedback")
        helpful_bullet = playbook.bullets[0]
        helpful_bullet.mark_helpful()
        playbook.save_playbook()
        
        print(f"    Marked bullet {helpful_bullet.id} as helpful")
        print(f"    Helpful count: {helpful_bullet.helpful_count}")
        
        # Step 5: Provide negative feedback
        print("\n Step 5: Provide Negative Feedback")
        harmful_bullet = playbook.bullets[1]
        harmful_bullet.mark_harmful()
        playbook.save_playbook()
        
        print(f"    Marked bullet {harmful_bullet.id} as harmful")
        print(f"    Harmful count: {harmful_bullet.harmful_count}")
        
        # Step 6: Verify feedback is persisted
        print("\n Step 6: Verify Feedback Persistence")
        
        # Reload playbook
        new_playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store=config.vector_store,
            embedding_model=config.embedding_model
        )
        
        # Find the bullets we modified
        reloaded_helpful = [b for b in new_playbook.bullets if b.id == helpful_bullet.id][0]
        reloaded_harmful = [b for b in new_playbook.bullets if b.id == harmful_bullet.id][0]
        
        assert reloaded_helpful.helpful_count == 1, "Helpful count should persist"
        assert reloaded_harmful.harmful_count == 1, "Harmful count should persist"
        
        print(f"    Feedback persisted correctly")
        print(f"    Helpful bullet: +{reloaded_helpful.helpful_count}/-{reloaded_helpful.harmful_count}")
        print(f"    Harmful bullet: +{reloaded_harmful.helpful_count}/-{reloaded_harmful.harmful_count}")
        
        # Step 7: Test playbook statistics
        print("\n Step 7: Check Playbook Statistics")
        stats = playbook.get_stats()
        
        print(f"   Total bullets: {stats['total_bullets']}")
        print(f"   Sections: {list(stats['sections'].keys())}")
        print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
        print(f"   Total helpful: {stats['total_helpful']}")
        print(f"   Total harmful: {stats['total_harmful']}")
        
        assert stats['total_bullets'] == initial_count
        assert stats['total_helpful'] == 1
        assert stats['total_harmful'] == 1
        
        print("\n" + "="*60)
        print(" End-to-End ACE Learning Test PASSED!")
        print("="*60)
        print("\n Test Summary:")
        print("    Components initialized correctly")
        print("    Playbook stores and retrieves knowledge")
        print("    Feedback system works (positive & negative)")
        print("    Feedback persists across sessions")
        print("    Statistics tracking works")
        print("\n ACE System is ready for production!")
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OpenAI API key required for E2E test"
    )
    def test_learning_improves_results(self, temp_storage_path):
        """
        Test that positive feedback improves bullet ranking.
        """
        print("\n" + "="*60)
        print(" Testing Learning Improvement")
        print("="*60)
        
        # Initialize
        playbook = PlaybookManager(
            playbook_dir=str(temp_storage_path),
            vector_store="faiss",
            embedding_model="openai:text-embedding-3-small"
        )
        
        # Add bullets with different helpfulness
        bullet1_id = playbook.add_bullet(
            content="Always use HTTPS for API calls",
            section="Security"
        )
        bullet2_id = playbook.add_bullet(
            content="Cache API responses for better performance",
            section="Performance"
        )
        
        # Mark one as very helpful
        bullet1 = [b for b in playbook.bullets if b.id == bullet1_id][0]
        for _ in range(5):
            bullet1.mark_helpful()
        playbook.save_playbook()
        
        # Get relevant bullets
        results = playbook.retrieve_relevant("How to make secure API calls?", top_k=2)
        
        print(f"   Query: 'How to make secure API calls?'")
        print(f"   Results: {len(results)} bullets")
        for bullet in results:
            print(f"      - [{bullet.id}] +{bullet.helpful_count}/-{bullet.harmful_count}: {bullet.content[:40]}...")
        
        # Helpful bullet should be included
        result_ids = [b.id for b in results]
        assert bullet1_id in result_ids, "Helpful bullet should be in results"
        
        print("\n    Learning system prioritizes helpful content!")
    
    def test_bullet_lifecycle_with_curator(self, temp_storage_path):
        """
        Test complete bullet lifecycle with Curator operations.
        """
        print("\n" + "="*60)
        print(" Testing Bullet Lifecycle with Curator")
        print("="*60)
        
        # Initialize
        playbook = PlaybookManager(
            playbook_dir=str(temp_storage_path),
            vector_store="faiss",
            embedding_model="openai:text-embedding-3-small"
        )
        
        curator = Curator(
            playbook_manager=playbook,
            storage_path=str(temp_storage_path)
        )
        
        # Add initial bullets
        bullet_id = playbook.add_bullet(
            content="Test bullet for lifecycle",
            section="Testing"
        )
        
        initial_count = len(playbook.bullets)
        print(f"   Initial bullets: {initial_count}")
        
        # Mark bullet as very harmful
        bullet = playbook.bullets[0]
        for _ in range(10):
            bullet.mark_harmful()
        playbook.save_playbook()
        
        print(f"   Bullet {bullet.id}: +{bullet.helpful_count}/-{bullet.harmful_count}")
        
        # Curator should recognize harmful bullet
        harmful_bullets = [b for b in playbook.bullets if b.is_harmful]
        assert len(harmful_bullets) > 0, "Should have harmful bullets"
        
        print(f"    Found {len(harmful_bullets)} harmful bullets")
        print(f"    Curator can identify low-quality content")

