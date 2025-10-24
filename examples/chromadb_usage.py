"""
ChromaDB Usage Example for ACE Context Engineering.

This example shows how to use ChromaDB as the vector store backend
instead of FAISS.
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model


def main():
    """ChromaDB usage example."""
    
    # Step 1: Configure ACE with ChromaDB
    print(" Configuring ACE with ChromaDB...")
    config = ACEConfig(
        playbook_name="chromadb_app",
        vector_store="chromadb",  # Use ChromaDB instead of FAISS
        chat_model="openai:gpt-4o-mini",
        embedding_model="openai:text-embedding-3-small",
        storage_path="/path/to/custom/storage"  # Optional: custom path
    )
    
    print(f" Using ChromaDB at: {config.get_storage_path()}")
    
    # Step 2: Initialize Playbook Manager with ChromaDB
    print("\n Initializing Playbook Manager with ChromaDB...")
    try:
        playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store="chromadb",  # Specify ChromaDB
            embedding_model=config.embedding_model
        )
    except ImportError:
        print(" ChromaDB not installed!")
        print("   Install with: pip install chromadb")
        print("   or: pip install ace-context-engineering[chromadb]")
        return
    
    # Step 3: Add bullets
    print("\n Adding bullets to ChromaDB...")
    playbook.add_bullet(
        content="When using ChromaDB, leverage its metadata filtering capabilities",
        section="Best Practices"
    )
    playbook.add_bullet(
        content="ChromaDB automatically persists data, no manual save needed",
        section="Best Practices"
    )
    
    # Step 4: Create and wrap agent
    print("\n Creating ACE-wrapped agent...")
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook,
        config=config
    )
    
    # Step 5: Use the agent
    print("\n Running query...")
    response = agent.invoke([
        {"role": "user", "content": "What are the benefits of using ChromaDB?"}
    ])
    
    print(f"\n Response:")
    print(response.content)
    
    # Step 6: Check stats
    stats = playbook.get_stats()
    print(f"\n ChromaDB Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Vector count: {playbook.vector_store.get_count()}")
    
    print("\n ChromaDB example completed!")


if __name__ == "__main__":
    main()

