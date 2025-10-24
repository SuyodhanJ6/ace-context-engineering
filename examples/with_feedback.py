"""
Feedback Loop Example for ACE Context Engineering.

This example shows how to use ACE's Reflector and Curator to learn
from user feedback and improve the playbook over time.
"""

from ace import (
    ACEConfig,
    ACEAgent,
    PlaybookManager,
    Reflector,
    Curator,
    ReflectionInsight
)
from langchain.chat_models import init_chat_model


def simulate_feedback(is_positive: bool, feedback_text: str, rating: int):
    """Simulate user feedback data."""
    class FeedbackData:
        def __init__(self, feedback_type, user_feedback, rating, feedback_id):
            self.feedback_type = feedback_type
            self.user_feedback = user_feedback
            self.rating = rating
            self.feedback_id = feedback_id
    
    feedback_type = "positive" if is_positive else "incorrect"
    return FeedbackData(feedback_type, feedback_text, rating, "feed-001")


def main():
    """Complete feedback loop example."""
    
    # Step 1: Setup ACE
    print(" Setting up ACE components...")
    config = ACEConfig(
        playbook_name="feedback_demo",
        vector_store="faiss",
        chat_model="openai:gpt-4o-mini"
    )
    
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    reflector = Reflector(
        model=config.chat_model,
        storage_path=config.get_storage_path()
    )
    
    curator = Curator(
        playbook_manager=playbook,
        storage_path=config.get_storage_path()
    )
    
    # Step 2: Create ACE-wrapped agent
    print("\n Creating agent...")
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(base_agent, playbook, config)
    
    # Step 3: Run agent on a task
    print("\n Running agent on task...")
    question = "What's the best way to handle user authentication?"
    
    response = agent.invoke([
        {"role": "user", "content": question}
    ])
    
    model_response = response.content
    used_bullets = agent.get_used_bullets()
    
    print(f"\n Agent Response:")
    print(model_response[:200] + "...")
    
    # Step 4: Simulate user feedback
    print("\n Simulating user feedback...")
    feedback = simulate_feedback(
        is_positive=False,
        feedback_text="The response should mention OAuth 2.0 and JWT tokens specifically",
        rating=2
    )
    
    # Step 5: Use Reflector to analyze feedback
    print("\n Running Reflector to analyze feedback...")
    chat_data = {
        "question": question,
        "model_response": model_response,
        "used_bullets": used_bullets
    }
    
    insight = reflector.analyze_feedback(chat_data, feedback)
    
    print(f"\n Reflection Results:")
    print(f"   Error: {insight.error_identification[:100]}...")
    print(f"   Root cause: {insight.root_cause_analysis[:100]}...")
    print(f"   Correct approach: {insight.correct_approach[:100]}...")
    print(f"   Key insight: {insight.key_insight[:100]}...")
    print(f"   Confidence: {insight.confidence}")
    
    # Step 6: Use Curator to update playbook
    print("\n Running Curator to update playbook...")
    delta = curator.process_insights(insight, feedback.feedback_id)
    
    print(f"\n Delta created with {delta.total_operations} operations:")
    for i, op in enumerate(delta.operations, 1):
        print(f"   {i}. {op.operation}: {op.content[:80] if op.content else op.bullet_id}...")
    
    # Step 7: Apply delta to playbook
    print("\n Applying delta to playbook...")
    success = curator.merge_delta(delta)
    
    if success:
        print(" Playbook updated successfully!")
    else:
        print(" Failed to update playbook")
    
    # Step 8: Update bullet counters based on feedback
    print("\n Updating bullet counters...")
    for bullet_id in used_bullets:
        # Negative feedback
        playbook.update_counters(bullet_id, helpful=False)
    
    # Step 9: Check updated stats
    stats = playbook.get_stats()
    print(f"\n Updated Playbook Stats:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
    print(f"   Sections: {list(stats['sections'].keys())}")
    
    # Step 10: Run agent again to see improvement
    print("\n Running agent again with updated playbook...")
    response2 = agent.invoke([
        {"role": "user", "content": question}
    ])
    
    print(f"\n Improved Response:")
    print(response2.content[:200] + "...")
    
    print("\n Complete feedback loop example completed!")
    print("   The playbook has learned from feedback and will improve over time!")


if __name__ == "__main__":
    main()

