"""
Feedback Modes Example

Demonstrates two modes of operation:
1. Manual Feedback Mode (auto_feedback=False): Wait for explicit user feedback
2. Auto Feedback Mode (auto_feedback=True): Automatic self-improvement after each response
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model


def main():
    """Demonstrate both feedback modes."""
    
    print("=" * 80)
    print("ACE FEEDBACK MODES DEMONSTRATION")
    print("=" * 80)
    
    # Setup
    config = ACEConfig(playbook_name="feedback_modes_demo", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Add initial bullet
    playbook.add_bullet(
        content="When explaining concepts, provide clear examples",
        section="Teaching"
    )
    
    base_agent = init_chat_model("openai:gpt-4o-mini")
    
    # =========================================================================
    # MODE 1: MANUAL FEEDBACK (auto_feedback=False)
    # =========================================================================
    print("\n" + "=" * 80)
    print("MODE 1: MANUAL FEEDBACK (auto_feedback=False)")
    print("Agent waits for explicit user feedback")
    print("=" * 80 + "\n")
    
    agent_manual = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=False  # Wait for manual feedback
    )
    
    # Ask question
    question1 = "What is recursion?"
    print(f" Question: {question1}\n")
    
    response1 = agent_manual.invoke([{"role": "user", "content": question1}])
    print(f" Response: {response1.content[:200]}...\n")
    
    print("⏳ Waiting for user feedback...")
    print("   (No automatic critique happens)")
    
    # User provides feedback
    print("\n User provides feedback:")
    result = agent_manual.submit_feedback(
        user_feedback="Good explanation but needs more practical examples",
        rating=3,
        feedback_type="improvement_suggestion"
    )
    
    print(f"\n Feedback Result:")
    print(f"   Success: {result['success']}")
    print(f"   Operations: {result.get('operations', 0)}")
    print(f"   Confidence: {result.get('confidence', 0):.2f}")
    
    # =========================================================================
    # MODE 2: AUTO FEEDBACK (auto_feedback=True)
    # =========================================================================
    print("\n" + "=" * 80)
    print("MODE 2: AUTO FEEDBACK (auto_feedback=True)")
    print("Agent automatically critiques and improves after each response")
    print("=" * 80 + "\n")
    
    agent_auto = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=True  # Automatic self-improvement!
    )
    
    # Ask question
    question2 = "What is a linked list?"
    print(f" Question: {question2}\n")
    
    response2 = agent_auto.invoke([{"role": "user", "content": question2}])
    print(f" Response: {response2.content[:200]}...\n")
    
    print(" Auto-critique already ran automatically!")
    print("   Playbook updated without waiting for user feedback")
    
    # User can still provide additional feedback if they want
    print("\n User can still provide additional feedback:")
    result2 = agent_auto.submit_feedback(
        user_feedback="Excellent explanation with good examples!",
        rating=5,
        feedback_type="positive"
    )
    
    print(f"\n Additional Feedback Result:")
    print(f"   Success: {result2['success']}")
    print(f"   Operations: {result2.get('operations', 0)}")
    
    # =========================================================================
    # TOGGLING MODES
    # =========================================================================
    print("\n" + "=" * 80)
    print("TOGGLING MODES DYNAMICALLY")
    print("=" * 80 + "\n")
    
    # Start with manual mode
    agent = ACEAgent(base_agent, playbook, config, auto_feedback=False)
    
    print("1⃣  Starting in MANUAL mode")
    response = agent.invoke([{"role": "user", "content": "What is Python?"}])
    print(f"   Response: {response.content[:100]}...")
    print("   ⏳ Waiting for feedback...\n")
    
    # Switch to auto mode
    print("2⃣  Switching to AUTO mode")
    agent.enable_auto_feedback()
    response = agent.invoke([{"role": "user", "content": "What is JavaScript?"}])
    print(f"   Response: {response.content[:100]}...")
    print("    Auto-critique already applied!\n")
    
    # Switch back to manual mode
    print("3⃣  Switching back to MANUAL mode")
    agent.disable_auto_feedback()
    response = agent.invoke([{"role": "user", "content": "What is Java?"}])
    print(f"   Response: {response.content[:100]}...")
    print("   ⏳ Waiting for feedback...\n")
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY: WHEN TO USE EACH MODE")
    print("=" * 80)
    print("""
 MANUAL FEEDBACK MODE (auto_feedback=False):
    When you have explicit user feedback (ratings, comments)
    For production systems with user feedback collection
    When you want precise control over what gets learned
    Best for: chatbots, customer support, interactive systems
   
 AUTO FEEDBACK MODE (auto_feedback=True):
    When user feedback is sparse or unavailable
    For batch processing or automated systems
    When you want continuous self-improvement
    Best for: data pipelines, automated tasks, development/testing
   
 BEST PRACTICE:
   Use both! Auto-feedback for continuous improvement, 
   plus manual feedback when users provide it (more accurate)
    """)
    
    # Show final stats
    stats = playbook.get_stats()
    print(f" Final Playbook Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
    print(f"   Sections: {list(stats['sections'].keys())}")
    
    print("\n Example completed!")


if __name__ == "__main__":
    main()

