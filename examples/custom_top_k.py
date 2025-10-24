"""
Custom top_k Configuration Example for ACE.

This example shows how to control how many bullets (strategies) are 
retrieved from the playbook for each query.
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model


def main():
    """Demonstrate custom top_k configuration."""
    
    print(" Custom top_k Configuration Example\n")
    
    # Example 1: Default top_k (10 bullets)
    print("=" * 60)
    print("Example 1: Default Configuration (top_k=10)")
    print("=" * 60)
    
    config_default = ACEConfig(
        playbook_name="default_k",
        vector_store="faiss"
        # top_k defaults to 10
    )
    
    print(f" Config created with top_k={config_default.top_k}")
    
    # Example 2: Small top_k (only 3 bullets - for focused context)
    print("\n" + "=" * 60)
    print("Example 2: Small top_k=3 (Focused Context)")
    print("=" * 60)
    
    config_small = ACEConfig(
        playbook_name="small_k",
        vector_store="faiss",
        top_k=3  # Only retrieve 3 most relevant bullets
    )
    
    playbook_small = PlaybookManager(
        playbook_dir=config_small.get_storage_path(),
        vector_store=config_small.vector_store,
        embedding_model=config_small.embedding_model
    )
    
    # Add some bullets
    print("\n Adding sample bullets...")
    for i in range(10):
        playbook_small.add_bullet(
            content=f"Strategy {i+1}: This is a sample strategy for testing",
            section="Test Strategies"
        )
    
    # Create agent with small top_k
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent_small = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook_small,
        config=config_small,  # Uses top_k=3 from config
        auto_inject=True
    )
    
    print(f" Agent created with top_k={config_small.top_k}")
    print(f"   → Will retrieve only 3 most relevant bullets per query")
    
    # Example 3: Large top_k (20 bullets - for comprehensive context)
    print("\n" + "=" * 60)
    print("Example 3: Large top_k=20 (Comprehensive Context)")
    print("=" * 60)
    
    config_large = ACEConfig(
        playbook_name="large_k",
        vector_store="faiss",
        top_k=20  # Retrieve more bullets for comprehensive context
    )
    
    playbook_large = PlaybookManager(
        playbook_dir=config_large.get_storage_path(),
        vector_store=config_large.vector_store,
        embedding_model=config_large.embedding_model
    )
    
    agent_large = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook_large,
        config=config_large,  # Uses top_k=20 from config
        auto_inject=True
    )
    
    print(f" Agent created with top_k={config_large.top_k}")
    print(f"   → Will retrieve up to 20 most relevant bullets per query")
    
    # Example 4: Override top_k per agent (not using config value)
    print("\n" + "=" * 60)
    print("Example 4: Override top_k in ACEAgent (Independent of Config)")
    print("=" * 60)
    
    config_override = ACEConfig(
        playbook_name="override_k",
        top_k=10  # Config says 10
    )
    
    playbook_override = PlaybookManager(
        playbook_dir=config_override.get_storage_path(),
        vector_store="faiss",
        embedding_model=config_override.embedding_model
    )
    
    agent_override = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook_override,
        config=config_override,
        auto_inject=True,
        top_k=5  # But agent uses 5 (overrides config)
    )
    
    print(f" Config has top_k={config_override.top_k}")
    print(f" But agent uses top_k=5 (overridden in constructor)")
    
    # Example 5: Dynamic top_k based on use case
    print("\n" + "=" * 60)
    print("Example 5: Dynamic top_k Based on Query Complexity")
    print("=" * 60)
    
    def get_optimal_top_k(query: str) -> int:
        """Determine optimal top_k based on query complexity."""
        if len(query.split()) < 5:
            return 3  # Simple query - fewer bullets
        elif len(query.split()) < 15:
            return 10  # Medium query - standard bullets
        else:
            return 20  # Complex query - more bullets
    
    # Simulate different queries
    queries = [
        "Hello",
        "How do I process a payment?",
        "I need to implement a complex multi-step authentication flow with OAuth 2.0, JWT tokens, and refresh token rotation"
    ]
    
    for query in queries:
        optimal_k = get_optimal_top_k(query)
        print(f"\n Query: '{query[:50]}...'")
        print(f"   → Optimal top_k: {optimal_k}")
    
    # Summary
    print("\n" + "=" * 60)
    print(" Summary: When to Use Different top_k Values")
    print("=" * 60)
    
    print("""
    top_k=3-5:    Simple queries, focused context, faster inference
    top_k=10:     Default, balanced context-performance tradeoff
    top_k=15-20:  Complex queries, comprehensive context needed
    top_k=30+:     May include irrelevant context, slower inference
    
     Tips:
    - Start with default (10) and adjust based on results
    - Use smaller top_k for faster responses
    - Use larger top_k when domain knowledge is critical
    - Monitor token usage (more bullets = more tokens)
    """)
    
    print("\n Custom top_k configuration example completed!")
    
    # Show configuration options
    print("\n" + "=" * 60)
    print(" All Configuration Options")
    print("=" * 60)
    print("""
    config = ACEConfig(
        playbook_name="my_app",           # Required: name for storage
        vector_store="faiss",             # "faiss" or "chromadb"
        storage_path="/custom/path",      # Optional: custom storage
        chat_model="openai:gpt-4o-mini",  # Model for reflections
        embedding_model="openai:text-embedding-3-small",  # Embeddings
        temperature=0.3,                  # LLM temperature
        top_k=10,                         #  Number of bullets to retrieve
        deduplication_threshold=0.9,      # Similarity for dedup
        max_epochs=5                      # Learning epochs
    )
    """)


if __name__ == "__main__":
    main()

