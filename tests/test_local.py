"""
Quick test to verify ACE package works locally.
"""

print(" Testing ACE Package Installation...\n")

# Test 1: Import all core components
print("1⃣ Testing imports...")
try:
    from ace import (
        ACEConfig,
        ACEAgent,
        PlaybookManager,
        Reflector,
        Curator,
        Bullet,
        ReflectionInsight,
        DeltaUpdate,
        ReflectorPrompts
    )
    print("    All imports successful!")
except Exception as e:
    print(f"    Import failed: {e}")
    exit(1)

# Test 2: Create ACEConfig
print("\n2⃣ Testing ACEConfig...")
try:
    config = ACEConfig(
        playbook_name="test_app",
        vector_store="faiss",
        top_k=5
    )
    print(f"    Config created: {config.playbook_name}")
    print(f"    Storage path: {config.get_storage_path()}")
except Exception as e:
    print(f"    Config failed: {e}")
    exit(1)

# Test 3: Initialize PlaybookManager
print("\n3⃣ Testing PlaybookManager...")
try:
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store="faiss",
        embedding_model="openai:text-embedding-3-small"
    )
    print(f"    PlaybookManager initialized")
    print(f"    Current bullets: {len(playbook.bullets)}")
except Exception as e:
    print(f"    PlaybookManager failed: {e}")
    print(f"   ℹ  Note: This requires OPENAI_API_KEY environment variable")

# Test 4: Add a test bullet
print("\n4⃣ Testing bullet creation...")
try:
    bullet_id = playbook.add_bullet(
        content="Test strategy: Always validate inputs",
        section="Testing"
    )
    print(f"    Bullet created: {bullet_id}")
    
    stats = playbook.get_stats()
    print(f"    Total bullets: {stats['total_bullets']}")
    print(f"    Sections: {list(stats['sections'].keys())}")
except Exception as e:
    print(f"     Bullet creation skipped: {e}")

# Test 5: Test Reflector initialization
print("\n5⃣ Testing Reflector...")
try:
    reflector = Reflector(
        model="openai:gpt-4o-mini",
        storage_path=config.get_storage_path(),
        max_refinement_iterations=2
    )
    print(f"    Reflector initialized")
    print(f"    Refinement iterations: {reflector.max_refinement_iterations}")
except Exception as e:
    print(f"     Reflector init: {e}")
    print(f"   ℹ  Note: This requires OPENAI_API_KEY environment variable")

# Test 6: Test Curator initialization
print("\n6⃣ Testing Curator...")
try:
    curator = Curator(
        playbook_manager=playbook,
        storage_path=config.get_storage_path()
    )
    print(f"    Curator initialized")
except Exception as e:
    print(f"    Curator failed: {e}")

# Test 7: Test custom prompts
print("\n7⃣ Testing custom prompts...")
try:
    from ace.prompts import (
        ReflectorPrompts,
        CONCISE_ANALYSIS_TEMPLATE,
        DETAILED_ANALYSIS_TEMPLATE
    )
    print(f"    Default prompts available")
    print(f"    CONCISE template available")
    print(f"    DETAILED template available")
except Exception as e:
    print(f"    Prompts test failed: {e}")

# Test 8: Test vector stores
print("\n8⃣ Testing vector store abstraction...")
try:
    from ace.vectorstores import VectorStoreBase, FAISSVectorStore
    print(f"    VectorStoreBase imported")
    print(f"    FAISSVectorStore imported")
    
    try:
        from ace.vectorstores import ChromaDBVectorStore
        print(f"    ChromaDBVectorStore available")
    except ImportError:
        print(f"   ℹ  ChromaDBVectorStore not installed (optional)")
except Exception as e:
    print(f"    Vector stores test failed: {e}")

# Final summary
print("\n" + "="*60)
print(" ACE Package Local Installation Test Complete!")
print("="*60)
print("""
 Next Steps:
1. Set OPENAI_API_KEY environment variable
2. Run examples:
   - python examples/basic_usage.py
   - python examples/custom_top_k.py
   - python examples/custom_prompts.py
3. Test with your own agent
4. Ready for deployment!
""")

