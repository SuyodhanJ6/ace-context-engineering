"""
Qdrant Usage Example for ACE Context Engineering.

This example shows how to use Qdrant as the vector store backend
instead of FAISS or ChromaDB. Qdrant supports both local Docker
deployments and Qdrant Cloud.

Important: With Qdrant, playbook metadata (JSON files) is stored
locally, but vector embeddings are stored externally in the Qdrant server.
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


def example_local_qdrant():
    """Example using local Qdrant (Docker)."""
    print("=" * 60)
    print("Qdrant Local (Docker) Example")
    print("=" * 60)
    
    # Step 1: Configure ACE with Qdrant
    print("\n📦 Step 1: Configuring ACE with Qdrant (local)...")
    config = ACEConfig(
        playbook_name="qdrant_local_app",
        vector_store="qdrant",  # Use Qdrant local
        qdrant_url="http://localhost:6333",  # Default local Docker URL
        chat_model="openai:gpt-4o-mini",
        embedding_model="openai:text-embedding-3-small",
        top_k=5
    )
    
    print(f"   ✅ Config: {config.playbook_name}")
    print(f"   ✅ Vector store: {config.vector_store}")
    print(f"   ✅ Qdrant URL: {config.qdrant_url}")
    print(f"   ✅ Storage path: {config.get_storage_path()}")
    print("\n   📝 Note: Playbook metadata → Local storage")
    print("   📝 Note: Vector embeddings → Qdrant server (external)")
    
    # Step 2: Initialize PlaybookManager with Qdrant
    print("\n📚 Step 2: Initializing PlaybookManager with Qdrant...")
    try:
        playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store="qdrant",
            embedding_model=config.embedding_model,
            qdrant_url=config.qdrant_url,
            qdrant_api_key=None  # No API key for local
        )
        print(f"   ✅ Playbook initialized with {len(playbook.bullets)} bullets")
    except ImportError:
        print("   ❌ Qdrant client is not installed!")
        print("   Install with: pip install qdrant-client")
        return
    except Exception as e:
        print(f"   ❌ Error connecting to Qdrant: {e}")
        print("   Make sure Qdrant is running:")
        print("   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
        return
    
    # Step 3: Add some initial bullets
    print("\n📝 Step 3: Adding initial bullets...")
    playbook.add_bullet(
        content="When using Qdrant, vectors are stored externally in the Qdrant server",
        section="Architecture"
    )
    playbook.add_bullet(
        content="Qdrant supports both local Docker deployments and cloud instances",
        section="Deployment"
    )
    print(f"   ✅ Added {len(playbook.bullets)} bullets")
    
    # Step 4: Create and wrap agent
    print("\n🤖 Step 4: Creating ACE-wrapped agent...")
    base_agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt="You are a helpful assistant."
    )
    
    agent = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook,
        config=config,
        auto_inject=True
    )
    print("   ✅ ACEAgent wrapper initialized")
    
    # Step 5: Use the agent
    print("\n💬 Step 5: Testing agent with query...")
    query = "How does Qdrant store vectors?"
    print(f"   Query: '{query}'")
    
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": query}
        ]
    })
    
    print("\n📝 Response:")
    print("-" * 60)
    print(response['messages'][-1].content[:300] + "...")
    
    # Step 6: Check used bullets
    used_bullets = agent.get_used_bullets()
    print(f"\n📊 Used {len(used_bullets)} bullets from playbook")
    
    print("\n" + "=" * 60)
    print("Local Qdrant example completed!")
    print("=" * 60)


def example_qdrant_cloud():
    """Example using Qdrant Cloud."""
    print("\n\n" + "=" * 60)
    print("Qdrant Cloud Example")
    print("=" * 60)
    
    # Step 1: Configure ACE with Qdrant Cloud
    print("\n📦 Step 1: Configuring ACE with Qdrant Cloud...")
    
    # Get API key from environment or config
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL", "https://your-cluster.qdrant.io")
    
    if not qdrant_api_key:
        print("   ⚠️  QDRANT_API_KEY not set in environment")
        print("   Skipping cloud example (set QDRANT_API_KEY and QDRANT_URL to test)")
        return
    
    config = ACEConfig(
        playbook_name="qdrant_cloud_app",
        vector_store="qdrant-cloud",  # Use Qdrant Cloud
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key,  # Required for cloud
        chat_model="openai:gpt-4o-mini",
        embedding_model="openai:text-embedding-3-small",
        top_k=5
    )
    
    print(f"   ✅ Config: {config.playbook_name}")
    print(f"   ✅ Vector store: {config.vector_store}")
    print(f"   ✅ Qdrant URL: {config.qdrant_url}")
    print(f"   ✅ Storage path: {config.get_storage_path()}")
    print("\n   📝 Note: Playbook metadata → Local storage")
    print("   📝 Note: Vector embeddings → Qdrant Cloud (external)")
    
    # Step 2: Initialize PlaybookManager with Qdrant Cloud
    print("\n📚 Step 2: Initializing PlaybookManager with Qdrant Cloud...")
    try:
        playbook = PlaybookManager(
            playbook_dir=config.get_storage_path(),
            vector_store="qdrant-cloud",
            embedding_model=config.embedding_model,
            qdrant_url=config.qdrant_url,
            qdrant_api_key=config.qdrant_api_key
        )
        print(f"   ✅ Playbook initialized with {len(playbook.bullets)} bullets")
    except ImportError:
        print("   ❌ Qdrant client is not installed!")
        print("   Install with: pip install qdrant-client")
        return
    except Exception as e:
        print(f"   ❌ Error connecting to Qdrant Cloud: {e}")
        return
    
    # Step 3: Add bullets
    print("\n📝 Step 3: Adding bullets...")
    playbook.add_bullet(
        content="Qdrant Cloud provides managed vector database service",
        section="Cloud"
    )
    print(f"   ✅ Added {len(playbook.bullets)} bullets")
    
    # Step 4: Create agent
    print("\n🤖 Step 4: Creating ACE-wrapped agent...")
    base_agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[],
        system_prompt="You are a helpful assistant."
    )
    
    agent = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook,
        config=config,
        auto_inject=True
    )
    
    # Step 5: Test
    print("\n💬 Step 5: Testing agent...")
    query = "What is Qdrant Cloud?"
    response = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    print("\n📝 Response:")
    print("-" * 60)
    print(response['messages'][-1].content[:300] + "...")
    
    print("\n" + "=" * 60)
    print("Qdrant Cloud example completed!")
    print("=" * 60)


def main():
    """Run both examples."""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        return
    
    # Run local Qdrant example
    example_local_qdrant()
    
    # Run cloud example (if API key is set)
    example_qdrant_cloud()


if __name__ == "__main__":
    main()

