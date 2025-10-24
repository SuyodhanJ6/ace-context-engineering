"""
Auto-Critique Example for ACE Context Engineering.

This example demonstrates:
1. Normal feedback flow: User provides feedback → Reflector analyzes
2. Auto-critique flow: No user feedback → Reflector critiques response automatically

The Reflector can evaluate responses even without explicit user feedback,
enabling continuous improvement.
"""

from ace import (
    ACEConfig,
    ACEAgent,
    PlaybookManager,
    Reflector,
    Curator,
)
from langchain.chat_models import init_chat_model


def simulate_user_feedback(feedback_text: str, rating: int, feedback_type: str):
    """Simulate user feedback data."""
    class FeedbackData:
        def __init__(self, feedback_type, user_feedback, rating, feedback_id):
            self.feedback_type = feedback_type
            self.user_feedback = user_feedback
            self.rating = rating
            self.feedback_id = feedback_id
    
    return FeedbackData(feedback_type, feedback_text, rating, "feed-001")


def main():
    """Demonstrate both feedback and auto-critique flows."""
    
    print("=" * 80)
    print("ACE Auto-Critique Example")
    print("=" * 80)
    
    # Setup ACE
    print("\n Setting up ACE components...")
    config = ACEConfig(
        playbook_name="auto_critique_demo",
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
    
    # Create ACE-wrapped agent
    print("\n Creating agent...")
    base_agent = init_chat_model("openai:gpt-4o-mini")
    agent = ACEAgent(base_agent, playbook, config)
    
    # Add some initial bullets
    print("\n Adding initial strategies to playbook...")
    playbook.add_bullet(
        content="When explaining security concepts, always mention OAuth 2.0 and JWT tokens",
        section="Security"
    )
    playbook.add_bullet(
        content="For authentication questions, provide code examples when relevant",
        section="Security"
    )
    
    print("\n" + "=" * 80)
    print("SCENARIO 1: WITH USER FEEDBACK")
    print("=" * 80)
    
    # Scenario 1: User provides feedback
    question1 = "How should I implement user authentication in my web app?"
    
    print(f"\n Question: {question1}")
    print("\n Generating response...")
    
    response1 = agent.invoke([
        {"role": "user", "content": question1}
    ])
    
    model_response1 = response1.content
    used_bullets1 = agent.get_used_bullets()
    
    print(f"\n Agent Response:")
    print(model_response1[:300] + "...")
    print(f"\n Used {len(used_bullets1)} bullets from playbook")
    
    # User provides negative feedback
    print("\n User provides feedback (negative)...")
    feedback1 = simulate_user_feedback(
        feedback_text="The response is too general. It should mention specific OAuth providers like Google, GitHub, and best practices for storing tokens securely.",
        rating=2,
        feedback_type="incorrect"
    )
    
    print(f"   Feedback: {feedback1.user_feedback}")
    print(f"   Rating: {feedback1.rating}/5")
    
    # Reflector analyzes feedback
    print("\n Reflector analyzing user feedback...")
    chat_data1 = {
        "question": question1,
        "model_response": model_response1,
        "used_bullets": used_bullets1
    }
    
    insight1 = reflector.analyze_feedback(chat_data1, feedback1)
    
    print(f"\n Reflection Results:")
    print(f"    Error: {insight1.error_identification[:150]}...")
    print(f"    Root cause: {insight1.root_cause_analysis[:150]}...")
    print(f"    Correct approach: {insight1.correct_approach[:150]}...")
    print(f"    Key insight: {insight1.key_insight[:150]}...")
    print(f"    Confidence: {insight1.confidence}")
    
    # Curator updates playbook
    print("\n Curator updating playbook...")
    delta1 = curator.process_insights(insight1, feedback1.feedback_id)
    
    if delta1.total_operations > 0:
        print(f"   Created {delta1.total_operations} operations")
        success1 = curator.merge_delta(delta1)
        if success1:
            print("    Playbook updated successfully!")
        
        # Update bullet counters (negative feedback)
        for bullet_id in used_bullets1:
            playbook.update_counters(bullet_id, helpful=False)
        print(f"    Updated counters for {len(used_bullets1)} bullets (harmful)")
    else:
        print("     No updates created (low confidence)")
    
    print("\n" + "=" * 80)
    print("SCENARIO 2: WITHOUT USER FEEDBACK (AUTO-CRITIQUE)")
    print("=" * 80)
    
    # Scenario 2: No user feedback, auto-critique
    question2 = "What are the best practices for API rate limiting?"
    
    print(f"\n Question: {question2}")
    print("\n Generating response...")
    
    response2 = agent.invoke([
        {"role": "user", "content": question2}
    ])
    
    model_response2 = response2.content
    used_bullets2 = agent.get_used_bullets()
    
    print(f"\n Agent Response:")
    print(model_response2[:300] + "...")
    print(f"\n Used {len(used_bullets2)} bullets from playbook")
    
    # NO USER FEEDBACK - Reflector does auto-critique
    print("\n No user feedback received...")
    print(" Reflector performing AUTO-CRITIQUE...")
    
    # Use the new auto_critique method!
    insight2 = reflector.auto_critique(
        question=question2,
        model_response=model_response2,
        refine=False  # Set to True for multi-iteration refinement
    )
    
    print(f"\n Auto-Critique Results:")
    print(f"    Analysis: {insight2.error_identification[:150]}...")
    print(f"    Confidence: {insight2.confidence}")
    
    # Only update if critique finds issues (confidence > 0.6)
    if insight2.confidence > 0.6:
        print(f"    Auto-critique found improvement opportunity!")
        print(f"    Key insight: {insight2.key_insight[:150]}...")
        
        # Curator updates playbook
        print("\n Curator updating playbook from auto-critique...")
        delta2 = curator.process_insights(insight2, "auto-002")
        
        if delta2.total_operations > 0:
            print(f"   Created {delta2.total_operations} operations")
            success2 = curator.merge_delta(delta2)
            if success2:
                print("    Playbook updated from auto-critique!")
        else:
            print("     No updates needed")
    else:
        print(f"    Response looks good (confidence: {insight2.confidence})")
        # Mark bullets as helpful if auto-critique passes
        for bullet_id in used_bullets2:
            playbook.update_counters(bullet_id, helpful=True)
        print(f"    Marked {len(used_bullets2)} bullets as helpful")
    
    print("\n" + "=" * 80)
    print("FINAL PLAYBOOK STATS")
    print("=" * 80)
    
    stats = playbook.get_stats()
    print(f"\n Playbook Statistics:")
    print(f"   Total bullets: {stats['total_bullets']}")
    print(f"   Helpful ratio: {stats['helpful_ratio']:.2%}")
    print(f"   Sections: {list(stats['sections'].keys())}")
    
    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
 WITH FEEDBACK: 
   - User provides explicit feedback (rating + text)
   - Reflector analyzes based on user input
   - High confidence insights from real user pain points
   
 WITHOUT FEEDBACK (AUTO-CRITIQUE):
   - Reflector evaluates response quality automatically
   - Can identify potential improvements proactively
   - Lower confidence threshold to avoid false positives
   - Marks bullets as helpful if no issues found
   
 BEST PRACTICE:
   - Always collect user feedback when possible (more accurate)
   - Use auto-critique as a fallback/supplement
   - Auto-critique helps catch obvious issues early
   - Combine both for continuous improvement!
    """)
    
    print("\n Example completed!")


if __name__ == "__main__":
    main()

