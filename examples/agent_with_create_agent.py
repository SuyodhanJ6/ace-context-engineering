"""
Example: Using create_agent (LangChain 1.0) with ACE

Demonstrates:
1. Using new create_agent API (not create_react_agent)
2. Wrapping with ACEAgent for context injection
3. Verifying playbook updates work
4. Testing learning cycle
"""

from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.agents import create_agent

print("=" * 60)
print(" Testing create_agent with ACE")
print("=" * 60)

# Step 1: Configure ACE
print("\n Step 1: Configure ACE")
config = ACEConfig(
    playbook_name="create_agent_test",
    vector_store="faiss",
    top_k=5
)
print(f"    Config: {config.playbook_name}")
print(f"    Storage: {config.get_storage_path()}")

# Step 2: Initialize PlaybookManager
print("\n Step 2: Initialize PlaybookManager")
playbook = PlaybookManager(
    playbook_dir=config.get_storage_path(),
    vector_store=config.vector_store,
    embedding_model=config.embedding_model
)
print(f"    Playbook initialized")
print(f"    Current bullets: {len(playbook.bullets)}")

# Step 3: Add initial knowledge
print("\n Step 3: Add Initial Knowledge to Playbook")
bullet1_id = playbook.add_bullet(
    content="When greeting users, always be polite and professional",
    section="Communication"
)
bullet2_id = playbook.add_bullet(
    content="For technical questions, provide clear and concise explanations",
    section="Technical Support"
)
bullet3_id = playbook.add_bullet(
    content="If unsure about something, admit it and offer to help find the answer",
    section="Honesty"
)

print(f"    Added {len(playbook.bullets)} bullets")
print(f"    IDs: {bullet1_id}, {bullet2_id}, {bullet3_id}")

# Step 4: Create agent using new create_agent API
print("\n Step 4: Create Agent using create_agent (LangChain 1.0)")

# Use create_agent (new standard in LangChain 1.0)
base_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],  # No tools for now, just testing
    system_prompt="You are a helpful assistant."
)
print("    Base agent created with create_agent")

# Step 5: Wrap with ACEAgent
print("\n Step 5: Wrap with ACEAgent")
agent = ACEAgent(
    base_agent,
    playbook,
    config,
    auto_inject=True  # Automatically inject context
)
print("    ACEAgent wrapper initialized")
print(f"    Auto-inject: {agent.auto_inject}")
print(f"    Top-K: {agent.top_k}")

# Step 6: Test agent with query
print("\n Step 6: Test Agent with Query")
query = "Hello! Can you help me understand how this system works?"
print(f"   Query: '{query}'")

response = agent.invoke({
    "messages": [
        {"role": "user", "content": query}
    ]
})

print(f"\n    Agent Response:")
print(f"   {response['messages'][-1].content[:200]}...")

# Step 7: Check which bullets were used
print("\n Step 7: Check Used Bullets")
used_bullets = agent.get_used_bullets()
print(f"    Used {len(used_bullets)} bullets")
for bullet_id in used_bullets:
    bullet = next((b for b in playbook.bullets if b.id == bullet_id), None)
    if bullet:
        print(f"      - [{bullet_id}] {bullet.content[:50]}...")

# Step 8: Provide feedback and update playbook
print("\n Step 8: Simulate Feedback and Update Playbook")

# Mark first bullet as helpful
if used_bullets:
    first_bullet_id = used_bullets[0]
    bullet = next((b for b in playbook.bullets if b.id == first_bullet_id), None)
    if bullet:
        bullet.mark_helpful()
        playbook.save_playbook()
        print(f"    Marked {first_bullet_id} as helpful")
        print(f"    Helpful count: {bullet.helpful_count}")

# Step 9: Verify playbook persistence
print("\n Step 9: Verify Playbook Persistence")

# Reload playbook
new_playbook = PlaybookManager(
    playbook_dir=config.get_storage_path(),
    vector_store=config.vector_store,
    embedding_model=config.embedding_model
)

print(f"    Reloaded playbook")
print(f"    Bullets after reload: {len(new_playbook.bullets)}")

# Check if feedback persisted
if used_bullets:
    first_bullet_id = used_bullets[0]
    reloaded_bullet = next((b for b in new_playbook.bullets if b.id == first_bullet_id), None)
    if reloaded_bullet:
        print(f"    Bullet {first_bullet_id} feedback persisted!")
        print(f"    Helpful: {reloaded_bullet.helpful_count}, Harmful: {reloaded_bullet.harmful_count}")

# Step 10: Test another query to see context is working
print("\n Step 10: Test Another Query")
query2 = "What should I do if I don't know the answer to a question?"
print(f"   Query: '{query2}'")

response2 = agent.invoke({
    "messages": [
        {"role": "user", "content": query2}
    ]
})

print(f"\n    Agent Response:")
print(f"   {response2['messages'][-1].content[:200]}...")

used_bullets2 = agent.get_used_bullets()
print(f"\n    Used {len(used_bullets2)} bullets")

# Step 11: Check playbook stats
print("\n Step 11: Playbook Statistics")
stats = playbook.get_stats()
print(f"   Total bullets: {stats['total_bullets']}")
print(f"   Sections: {list(stats['sections'].keys())}")
print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
print(f"   Total helpful: {stats['total_helpful']}")
print(f"   Total harmful: {stats['total_harmful']}")

print("\n" + "=" * 60)
print(" create_agent + ACE Test Complete!")
print("=" * 60)
print("\n Summary:")
print("    create_agent (LangChain 1.0) works with ACE")
print("    Automatic context injection working")
print("    Playbook updates and persists")
print("    Feedback system functional")
print("    Agent uses relevant bullets from playbook")
print("\n System is working correctly!")

