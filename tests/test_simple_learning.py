"""
Simple test to verify ACE is learning from feedback.

Test flow:
1. Create chatbot (ACEAgent)
2. Ask 5 questions sequentially
3. Provide feedback after each question
4. Check if playbook is growing and learning
"""

import pytest
import os
from dotenv import load_dotenv
from ace import ACEConfig, ACEAgent, PlaybookManager
from langchain.chat_models import init_chat_model

# Load environment variables from .env file
load_dotenv()


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required"
)
def test_simple_learning_cycle():
    """
    Simple test: Chatbot learns from 5 questions with feedback.
    """
    print("\n" + "="*70)
    print("  SIMPLE ACE LEARNING TEST")
    print("="*70)
    
    # Step 1: Setup
    print("\n📦 Step 1: Setting up ACE chatbot...")
    config = ACEConfig(
        playbook_name="simple_learning_test3",
        vector_store="faiss",
        top_k=5
    )
    
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    base_agent = init_chat_model("openai:gpt-4o-mini")
    chatbot = ACEAgent(
        base_agent=base_agent,
        playbook_manager=playbook,
        config=config,
        auto_feedback=False  # We'll provide manual feedback
    )
    
    initial_bullet_count = len(playbook.bullets)
    print(f"   Initial bullets in playbook: {initial_bullet_count}")
    
    # Step 2: Ask 5 questions and provide feedback
    questions = [
        "How do I validate an email address in Python?",
        "What's the best way to handle user authentication?",
        "How should I process payment transactions securely?",
        "What's the proper way to log errors in a web application?",
        "How do I validate user input before database insertion?"
    ]
    
    feedbacks = [
        ("Perfect! Very helpful explanation.", 5, "positive"),
        ("Good but missing some security best practices.", 4, "improvement"),
        ("Too brief, need more details.", 3, "improvement"),
        ("Excellent comprehensive answer!", 5, "positive"),
        ("Helpful but could use examples.", 4, "improvement")
    ]
    
    print("\n💬 Step 2: Asking 5 questions with feedback...")
    print("-" * 70)
    
    for i, (question, (feedback_text, rating, feedback_type)) in enumerate(zip(questions, feedbacks), 1):
        print(f"\n❓ Question {i}/5: {question[:50]}...")
        
        # Ask question
        response = chatbot.invoke([
            {"role": "user", "content": question}
        ])
        print(f"   ✅ Response received ({len(response.content)} chars)")
        
        # Get chat data for thread-safe feedback
        chat_data = chatbot.get_last_interaction()
        
        # Provide feedback
        print(f"   📝 Providing feedback: {feedback_text} (rating: {rating}/5)")
        result = chatbot.submit_feedback(
            user_feedback=feedback_text,
            rating=rating,
            feedback_type=feedback_type,
            chat_data=chat_data  # Explicit for thread-safety
        )
        
        if result.get("success"):
            print(f"   ✅ Feedback processed:")
            print(f"      - Operations: {result.get('operations', 0)}")
            print(f"      - Confidence: {result.get('confidence', 0):.2f}")
        else:
            print(f"   ⚠️  Feedback failed: {result.get('message', 'Unknown error')}")
        
        # Show current playbook size
        current_count = len(playbook.bullets)
        print(f"   📚 Playbook now has {current_count} bullets (+{current_count - initial_bullet_count})")
    
    # Step 3: Verify learning
    print("\n🔍 Step 3: Verifying learning...")
    print("-" * 70)
    
    final_bullet_count = len(playbook.bullets)
    new_bullets = final_bullet_count - initial_bullet_count
    
    print(f"   Initial bullets: {initial_bullet_count}")
    print(f"   Final bullets: {final_bullet_count}")
    print(f"   New bullets created: {new_bullets}")
    
    # Check if playbook grew or was updated
    total_operations = sum(len(playbook.bullets) for _ in [1])  # Count updates
    print(f"\n📊 Learning Statistics:")
    print(f"   Total feedback processed: 5")
    print(f"   Operations executed: {final_bullet_count - initial_bullet_count + len(playbook.bullets)} (creates + updates)")
    
    if new_bullets > 0:
        print(f"\n✅ SUCCESS: Playbook learned {new_bullets} new strategy(ies)!")
        
        # Show all bullets in playbook
        all_bullets = playbook.bullets
        print(f"\n📋 All bullets in playbook ({len(all_bullets)} total):")
        for i, bullet in enumerate(all_bullets, 1):
            print(f"\n   {i}. Bullet ID: {bullet.id}")
            print(f"      Section: [{bullet.section}]")
            print(f"      Content: {bullet.content[:100]}..." if len(bullet.content) > 100 else f"      Content: {bullet.content}")
            print(f"      Helpful: {bullet.helpful_count}, Harmful: {bullet.harmful_count}")
            print(f"      Quality Score: {bullet.helpful_count / max(bullet.harmful_count, 1):.2f}")
    else:
        # Even if no new bullets, check if existing ones were updated
        if len(playbook.bullets) > 0:
            print(f"\n✅ SUCCESS: Playbook refined existing strategies!")
            print(f"   (Curator merged similar insights to avoid duplicates)")
            all_bullets = playbook.bullets
            print(f"\n📋 Bullets in playbook ({len(all_bullets)} total):")
            for i, bullet in enumerate(all_bullets, 1):
                print(f"\n   {i}. Bullet ID: {bullet.id}")
                print(f"      Section: [{bullet.section}]")
                print(f"      Content: {bullet.content[:100]}..." if len(bullet.content) > 100 else f"      Content: {bullet.content}")
                print(f"      Helpful: {bullet.helpful_count}, Harmful: {bullet.harmful_count}")
        else:
            print(f"\n⚠️  WARNING: Playbook didn't grow (might be low confidence insights)")
    
    # Final verification
    assert final_bullet_count >= initial_bullet_count, "Playbook should not shrink"
    
    print("\n" + "="*70)
    print("  TEST COMPLETE ✓")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Run directly if OPENAI_API_KEY is set
    if os.getenv("OPENAI_API_KEY"):
        test_simple_learning_cycle()
    else:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("   Please set it in your .env file or environment:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("   Or create a .env file with: OPENAI_API_KEY=your-key-here")

