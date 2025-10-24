"""
Basic Usage Example for ACE Context Engineering.

This example shows how to wrap any LangChain agent with ACE for automatic
context injection from a self-improving playbook.
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model

def main():
    """Basic usage example."""
    
    # Step 1: Configure ACE
    print(" Configuring ACE...")
    config = ACEConfig(
        playbook_name="my_app",  # Name of your application
        vector_store="faiss",    # Use FAISS vector store
        chat_model="openai:gpt-4o-mini",  # Model for reflections
        embedding_model="openai:text-embedding-3-small",  # Model for embeddings
        top_k=10  # Number of relevant bullets to retrieve
    )
    
    print(f" Storage path: {config.get_storage_path()}")
    
    # Step 2: Initialize Playbook Manager
    print("\n Initializing Playbook Manager...")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Step 3: Add some initial strategies (optional)
    print("\n Adding initial strategies...")
    playbook.add_bullet(
        content="When processing payments, always verify the order exists first",
        section="Payment Processing"
    )
    playbook.add_bullet(
        content="For user queries, check authentication status before accessing sensitive data",
        section="Security"
    )
    
    # Step 4: Create your base agent (any LangChain agent/model)
    print("\n Creating base agent...")
    base_agent = init_chat_model("openai:gpt-4o-mini")
    
    # Step 5: Wrap with ACE for automatic context injection
    print("\n Wrapping agent with ACE...")
    agent = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook,
        config=config,
        auto_inject=True  # Automatically inject playbook context
    )
    
    # Step 6: Use the agent normally - ACE handles context automatically!
    print("\n Running agent with automatic context injection...")
    
    query = "How should I process a payment for order #12345?"
    
    response = agent.invoke([
        {"role": "user", "content": query}
    ])
    
    print(f"\n Agent Response:")
    print(response.content)
    
    # Step 7: Get bullets that were used (for feedback tracking)
    used_bullets = agent.get_used_bullets()
    print(f"\n Used {len(used_bullets)} bullets from playbook: {used_bullets}")
    
    # Step 8: Update bullet counters based on feedback
    print("\n Simulating positive feedback...")
    for bullet_id in used_bullets:
        playbook.update_counters(bullet_id, helpful=True)
    
    # Step 9: Check playbook stats
    stats = playbook.get_stats()
    print(f"\n Playbook Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Sections: {list(stats['sections'].keys())}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
    
    print("\n Example completed!")


if __name__ == "__main__":
    main()
