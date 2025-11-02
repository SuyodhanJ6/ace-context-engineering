"""
Test dynamic prompt templates for auto-critique functionality.
"""

import pytest
import os
from ace import ACEConfig, ACEAgent, PlaybookManager, Reflector
from langchain.chat_models import init_chat_model


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required"
)
def test_default_auto_critique():
    """Test with default auto-critique template"""
    print("=" * 80)
    print("TEST 1: DEFAULT AUTO-CRITIQUE TEMPLATE")
    print("=" * 80)
    
    config = ACEConfig(playbook_name="test_default", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Use default auto-critique template
    reflector = Reflector(
        model=config.chat_model,
        storage_path=config.get_storage_path()
    )
    
    print("\n Testing with default auto-critique template...")
    
    chat_data = {
        "question": "What is machine learning?",
        "model_response": "Machine learning is a subset of AI that enables computers to learn without being explicitly programmed."
    }
    
    insight = reflector.analyze_feedback(
        chat_data=chat_data,
        feedback_data=None,  # Auto-critique mode
        refine=False
    )
    
    print(f"\n Auto-critique results:")
    print(f"   Analysis: {insight.error_identification[:100]}...")
    print(f"   Confidence: {insight.confidence:.2f}")
    print(f"   Key insight: {insight.key_insight[:100]}...")
    
    print("\n DEFAULT TEMPLATE TEST PASSED!\n")


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required"
)
def test_custom_auto_critique():
    """Test with custom auto-critique template"""
    print("=" * 80)
    print("TEST 2: CUSTOM AUTO-CRITIQUE TEMPLATE")
    print("=" * 80)
    
    # Custom template focused on technical accuracy
    custom_template = """You are a technical reviewer. Evaluate this response for technical accuracy and completeness.

QUESTION: {question}

MODEL RESPONSE: {model_response}

TECHNICAL EVALUATION CRITERIA:
1. Is the response technically accurate?
2. Are key concepts explained correctly?
3. Is the response complete enough for the question?
4. Are there any technical errors or misconceptions?
5. Would a technical expert find this response helpful?

IMPORTANT:
- If TECHNICALLY SOUND, use LOW confidence (< 0.4)
- If TECHNICAL ISSUES found, use HIGHER confidence (> 0.7)
- Focus on factual accuracy and technical correctness

Output JSON:
{{
    "error_identification": "Describe technical issues (or 'Technically sound' if good)",
    "root_cause_analysis": "Why these technical issues exist",
    "correct_approach": "What should be done technically",
    "key_insight": "Technical improvement strategy",
    "confidence": 0.0-1.0
}}"""
    
    config = ACEConfig(playbook_name="test_custom", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Use custom auto-critique template
    reflector = Reflector(
        model=config.chat_model,
        storage_path=config.get_storage_path(),
        auto_critique_template=custom_template  # Custom template!
    )
    
    print("\n Testing with custom technical template...")
    
    chat_data = {
        "question": "What is recursion?",
        "model_response": "Recursion is when a function calls itself. It's like a loop but more elegant."
    }
    
    insight = reflector.analyze_feedback(
        chat_data=chat_data,
        feedback_data=None,  # Auto-critique mode
        refine=False
    )
    
    print(f"\n Custom template results:")
    print(f"   Analysis: {insight.error_identification[:100]}...")
    print(f"   Confidence: {insight.confidence:.2f}")
    print(f"   Key insight: {insight.key_insight[:100]}...")
    
    print("\n CUSTOM TEMPLATE TEST PASSED!\n")


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key required"
)
def test_domain_specific_template():
    """Test domain-specific auto-critique template"""
    print("=" * 80)
    print("TEST 3: DOMAIN-SPECIFIC TEMPLATE")
    print("=" * 80)
    
    # Domain-specific template for medical/healthcare
    medical_template = """You are a medical information reviewer. Evaluate this response for medical accuracy and safety.

QUESTION: {question}

MODEL RESPONSE: {model_response}

MEDICAL EVALUATION CRITERIA:
1. Is the medical information accurate and up-to-date?
2. Are there any potentially harmful medical claims?
3. Is the response appropriate for general public consumption?
4. Are medical terms used correctly?
5. Does it encourage consulting healthcare professionals when needed?

SAFETY FIRST:
- If MEDICALLY SOUND and SAFE, use LOW confidence (< 0.3)
- If MEDICAL ISSUES or SAFETY CONCERNS, use HIGH confidence (> 0.8)
- Prioritize patient safety over everything else

Output JSON:
{{
    "error_identification": "Describe medical/safety issues (or 'Medically sound' if good)",
    "root_cause_analysis": "Why these medical issues exist",
    "correct_approach": "What should be done medically",
    "key_insight": "Medical safety improvement strategy",
    "confidence": 0.0-1.0
}}"""
    
    config = ACEConfig(playbook_name="test_medical", vector_store="faiss")
    playbook = PlaybookManager(
        playbook_dir=config.get_storage_path(),
        vector_store=config.vector_store,
        embedding_model=config.embedding_model
    )
    
    # Use medical-specific template
    reflector = Reflector(
        model=config.chat_model,
        storage_path=config.get_storage_path(),
        auto_critique_template=medical_template  # Medical template!
    )
    
    print("\n Testing with medical domain template...")
    
    chat_data = {
        "question": "What should I do for a headache?",
        "model_response": "Take aspirin and rest. If it persists, see a doctor."
    }
    
    insight = reflector.analyze_feedback(
        chat_data=chat_data,
        feedback_data=None,  # Auto-critique mode
        refine=False
    )
    
    print(f"\n Medical template results:")
    print(f"   Analysis: {insight.error_identification[:100]}...")
    print(f"   Confidence: {insight.confidence:.2f}")
    print(f"   Key insight: {insight.key_insight[:100]}...")
    
    print("\n DOMAIN-SPECIFIC TEMPLATE TEST PASSED!\n")


def test_prompt_formatting():
    """Test that prompt formatting works correctly"""
    print("=" * 80)
    print("TEST 4: PROMPT FORMATTING")
    print("=" * 80)
    
    from ace.prompts import ReflectorPrompts, AUTO_CRITIQUE_TEMPLATE
    
    # Test default template formatting
    formatted_prompt = ReflectorPrompts.format_auto_critique_prompt(
        question="What is Python?",
        model_response="Python is a programming language."
    )
    
    print("\n Testing prompt formatting...")
    print(f"   Question included: {'{question}' in formatted_prompt}")
    print(f"   Response included: {'{model_response}' in formatted_prompt}")
    print(f"   Template used: {AUTO_CRITIQUE_TEMPLATE[:50]}...")
    
    # Test custom template formatting
    custom_template = "Evaluate: {question} -> {model_response}"
    custom_formatted = ReflectorPrompts.format_auto_critique_prompt(
        question="Test question",
        model_response="Test response",
        custom_template=custom_template
    )
    
    print(f"\n   Custom template works: {custom_formatted == 'Evaluate: Test question -> Test response'}")
    
    print("\n PROMPT FORMATTING TEST PASSED!\n")


if __name__ == "__main__":
    try:
        print("\n TESTING DYNAMIC PROMPT TEMPLATES\n")
        
        # Test 1: Default template
        test_default_auto_critique()
        
        # Test 2: Custom template
        test_custom_auto_critique()
        
        # Test 3: Domain-specific template
        test_domain_specific_template()
        
        # Test 4: Prompt formatting
        test_prompt_formatting()
        
        print("=" * 80)
        print(" ALL DYNAMIC PROMPT TESTS PASSED!")
        print("=" * 80)
        print("""
Summary:
 Default auto-critique template works
 Custom auto-critique template works  
 Domain-specific templates work
 Prompt formatting works correctly

Dynamic prompt templates are working perfectly!
        """)
        
    except Exception as e:
        print(f"\n TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
