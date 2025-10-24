"""
Manual Control Example for ACE Context Engineering.

This example shows how to use ACE components individually for maximum
control, without the automatic wrapper.
"""

from ace import ACEConfig, PlaybookManager, Reflector, Curator
from langchain.chat_models import init_chat_model


def main():
    """Manual control example."""
    
    # Step 1: Setup
    print(" Setting up ACE components...")
    config = ACEConfig(
        playbook_name="manual_demo",
        vector_store="faiss"
    )
    
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Step 2: Add initial bullets manually
    print("\n Adding initial strategies...")
    bullet1 = playbook.add_bullet(
        content="Always validate input before processing",
        section="Validation"
    )
    bullet2 = playbook.add_bullet(
        content="Use descriptive variable names for clarity",
        section="Code Quality"
    )
    
    print(f"   Added bullets: {bullet1}, {bullet2}")
    
    # Step 3: Create your own agent (NOT wrapped)
    print("\n Creating agent (no wrapper)...")
    agent = init_chat_model("openai:gpt-4o-mini")
    
    # Step 4: Manually retrieve relevant context
    print("\n Manually retrieving relevant context...")
    query = "How should I write clean code?"
    
    relevant_bullets = playbook.retrieve_relevant(query, top_k=5)
    
    print(f"   Found {len(relevant_bullets)} relevant bullets:")
    for bullet in relevant_bullets:
        print(f"   - [{bullet.id}] {bullet.content[:60]}...")
    
    # Step 5: Manually construct context
    context = "# Playbook Context\n\n"
    for bullet in relevant_bullets:
        context += f"{bullet.to_markdown()}\n\n"
    
    # Step 6: Manually inject context into messages
    messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": query}
    ]
    
    print("\n Calling agent with manual context...")
    response = agent.invoke(messages)
    
    print(f"\n Response:")
    print(response.content[:200] + "...")
    
    # Step 7: Manually track which bullets were used
    used_bullet_ids = [b.id for b in relevant_bullets]
    
    # Step 8: Manually update counters
    print("\n Manually updating bullet counters...")
    for bullet_id in used_bullet_ids:
        playbook.update_counters(bullet_id, helpful=True)
        print(f"    Marked {bullet_id} as helpful")
    
    # Step 9: Manually deduplicate if needed
    print("\n Checking for duplicates...")
    removed = playbook.deduplicate(similarity_threshold=0.9)
    if removed > 0:
        print(f"    Removed {removed} duplicate bullets")
    else:
        print("    No duplicates found")
    
    # Step 10: Get specific bullet
    print("\n Getting specific bullet...")
    bullet = playbook.get_bullet(bullet1)
    if bullet:
        print(f"   ID: {bullet.id}")
        print(f"   Content: {bullet.content}")
        print(f"   Section: {bullet.section}")
        print(f"   Helpful: {bullet.helpful}, Harmful: {bullet.harmful}")
    
    # Step 11: Check stats
    stats = playbook.get_stats()
    print(f"\n Final Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Sections: {stats['sections']}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
    
    print("\n Manual control example completed!")
    print("   You have full control over every aspect of ACE!")


if __name__ == "__main__":
    main()

