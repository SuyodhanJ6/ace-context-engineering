"""
Simple Auto-Critique Example

Shows how ACE can automatically evaluate and improve responses
even WITHOUT explicit user feedback using auto_feedback=True.
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model


def main():
    """Simple demonstration of auto-feedback functionality."""
    
    print(" ACE Auto-Feedback Demo\n")
    
    # 1. Setup
    config = ACEConfig(playbook_name="auto_feedback_simple", vector_store="faiss")
    
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # 2. Create agent with auto_feedback=True
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(
        base_agent,
        playbook,
        config,
        auto_feedback=True  #  Automatic self-improvement!
    )
    
    # 3. Agent answers a question
    question = "What is Python?"
    print(f" Question: {question}\n")
    
    # When auto_feedback=True, the ACE pipeline runs automatically!
    response = agent.invoke([{"role": "user", "content": question}])
    
    print(f"\n Response: {response.content[:200]}...\n")
    print(" Auto-critique already ran and updated the playbook!")
    print("   No manual feedback needed!\n")
    
    # Show playbook stats
    stats = playbook.get_stats()
    print(f" Playbook Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}\n")
    
    print("=" * 60)
    print(" KEY BENEFITS:")
    print("    Auto-feedback lets ACE improve continuously")
    print("    No waiting for user feedback")
    print("    Self-improving system")
    print("    Perfect for batch processing & automation")
    print("=" * 60)


if __name__ == "__main__":
    main()

