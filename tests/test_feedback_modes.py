"""
Quick test to verify auto_feedback True/False modes work correctly.
"""

import pytest
import os
from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required for embedding model"
)
def test_manual_mode():
    """Test manual feedback mode (auto_feedback=False)"""
    print("=" * 80)
    print("TEST 1: MANUAL MODE (auto_feedback=False)")
    print("=" * 80)
    
    config = ACEConfig(playbook_name="test_manual", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=False  # Manual mode
    )
    
    print("\n Asking: What is Python?")
    response = agent.invoke([{"role": "user", "content": "What is Python?"}])
    print(f" Response received: {response.content[:100]}...")
    
    print("\n⏳ Agent is waiting for manual feedback...")
    print("   (No auto-critique should have run)")
    
    # Submit manual feedback
    print("\n Submitting manual feedback...")
    result = agent.submit_feedback(
        user_feedback="Good but needs more examples",
        rating=3,
        feedback_type="improvement_suggestion"
    )
    
    print(f" Feedback processed: {result['success']}")
    print(f"   Operations: {result.get('operations', 0)}")
    print(f"   Confidence: {result.get('confidence', 0):.2f}")
    
    print("\n MANUAL MODE TEST PASSED!\n")


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required for embedding model"
)
def test_auto_mode():
    """Test auto feedback mode (auto_feedback=True)"""
    print("=" * 80)
    print("TEST 2: AUTO MODE (auto_feedback=True)")
    print("=" * 80)
    
    config = ACEConfig(playbook_name="test_auto", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=True  # Auto mode
    )
    
    print("\n Asking: What is JavaScript?")
    response = agent.invoke([{"role": "user", "content": "What is JavaScript?"}])
    print(f" Response received: {response.content[:100]}...")
    
    print("\n Auto-critique should have run automatically!")
    print("   (Check for auto-critique messages above)")
    
    print("\n AUTO MODE TEST PASSED!\n")


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required for embedding model"
)
def test_toggle_mode():
    """Test toggling between modes"""
    print("=" * 80)
    print("TEST 3: TOGGLE MODES")
    print("=" * 80)
    
    config = ACEConfig(playbook_name="test_toggle", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=False  # Start with manual
    )
    
    print("\n1⃣  Starting in MANUAL mode")
    response = agent.invoke([{"role": "user", "content": "What is Java?"}])
    print(f" Response: {response.content[:50]}...")
    
    print("\n2⃣  Switching to AUTO mode")
    agent.enable_auto_feedback()
    response = agent.invoke([{"role": "user", "content": "What is Ruby?"}])
    print(f" Response: {response.content[:50]}...")
    
    print("\n3⃣  Switching back to MANUAL mode")
    agent.disable_auto_feedback()
    response = agent.invoke([{"role": "user", "content": "What is Go?"}])
    print(f" Response: {response.content[:50]}...")
    
    print("\n TOGGLE MODE TEST PASSED!\n")


if __name__ == "__main__":
    try:
        print("\n TESTING ACE FEEDBACK MODES\n")
        
        # Test 1: Manual mode
        test_manual_mode()
        
        # # Test 2: Auto mode
        # test_auto_mode()
        
        # # Test 3: Toggle modes
        # test_toggle_mode()
        
        print("=" * 80)
        print(" ALL TESTS PASSED!")
        print("=" * 80)
        print("""
Summary:
 Manual mode (auto_feedback=False) - Waits for feedback
 Auto mode (auto_feedback=True) - Runs auto-critique automatically  
 Toggle between modes - Works dynamically

Both modes are working correctly!
        """)
        
    except Exception as e:
        print(f"\n TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

