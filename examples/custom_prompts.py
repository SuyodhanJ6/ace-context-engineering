"""
Custom Prompts Example for ACE.

This example shows how to customize the Reflector's prompts for
domain-specific or specialized use cases.
"""

from ace import ACEConfig, Reflector, ReflectorPrompts


def main():
    """Demonstrate custom prompts usage."""
    
    print(" Custom Prompts Example\n")
    
    # Example 1: Default prompts
    print("=" * 60)
    print("Example 1: Default Prompts (Out of the Box)")
    print("=" * 60)
    
    config = ACEConfig(playbook_name="default_prompts")
    
    reflector_default = Reflector(
        model="openai:gpt-4o-mini",
        storage_path=config.get_storage_path()
        # Uses default prompts
    )
    
    print(" Using default prompts")
    print(f"   System: {ReflectorPrompts.DEFAULT_SYSTEM_PROMPT[:80]}...")
    print(f"   Template: {ReflectorPrompts.DEFAULT_ANALYSIS_TEMPLATE[:80]}...")
    
    # Example 2: Custom system prompt
    print("\n" + "=" * 60)
    print("Example 2: Custom System Prompt")
    print("=" * 60)
    
    custom_system = """You are a customer service excellence expert specialized in analyzing 
support interactions and extracting best practices for team training."""
    
    reflector_custom_system = Reflector(
        model="openai:gpt-4o-mini",
        storage_path=config.get_storage_path(),
        system_prompt=custom_system  # Custom system prompt
    )
    
    print(" Custom system prompt:")
    print(f"   '{custom_system[:100]}...'")
    
    # Example 3: Custom analysis template (concise)
    print("\n" + "=" * 60)
    print("Example 3: Concise Analysis Template")
    print("=" * 60)
    
    concise_template = """Briefly analyze this interaction.

Question: {question}
Answer: {model_response}
Feedback: {user_feedback} (Type: {feedback_type}, Rating: {rating}/5)

Provide concise JSON analysis:
{{
    "error_identification": "what went wrong",
    "root_cause_analysis": "why it happened",
    "correct_approach": "what to do instead",
    "key_insight": "actionable strategy",
    "confidence": 0.8
}}

Be brief but actionable."""
    
    reflector_concise = Reflector(
        model="openai:gpt-4o-mini",
        storage_path=config.get_storage_path(),
        analysis_template=concise_template  # Custom template
    )
    
    print(" Using concise template for faster analysis")
    
    # Example 4: Domain-specific template
    print("\n" + "=" * 60)
    print("Example 4: Domain-Specific Template (Healthcare)")
    print("=" * 60)
    
    healthcare_system = """You are a healthcare AI specialist expert at analyzing 
medical chatbot interactions for accuracy, empathy, and compliance."""
    
    healthcare_template = """Analyze this healthcare interaction for accuracy and compliance.

PATIENT QUESTION: {question}
BOT RESPONSE: {model_response}
FEEDBACK: {user_feedback} ({feedback_type}, {rating}/5)

Healthcare-specific analysis:
1. Medical accuracy issues
2. Empathy and tone concerns
3. Compliance with healthcare communication standards
4. Patient safety considerations

Provide JSON:
{{
    "error_identification": "specific medical/communication issues",
    "root_cause_analysis": "why this is problematic in healthcare",
    "correct_approach": "compliant and accurate response",
    "key_insight": "healthcare best practice to remember",
    "confidence": 0.8
}}"""
    
    reflector_healthcare = Reflector(
        model="openai:gpt-4o-mini",
        storage_path=config.get_storage_path(),
        system_prompt=healthcare_system,
        analysis_template=healthcare_template
    )
    
    print(" Using healthcare-specific prompts")
    print("   → Focuses on medical accuracy and compliance")
    
    # Example 5: Using pre-built templates from prompts module
    print("\n" + "=" * 60)
    print("Example 5: Using Pre-built Templates")
    print("=" * 60)
    
    from ace.prompts import (
        CONCISE_ANALYSIS_TEMPLATE,
        DETAILED_ANALYSIS_TEMPLATE,
        DOMAIN_SPECIFIC_TEMPLATE
    )
    
    # Concise template
    reflector_prebuilt_concise = Reflector(
        model="openai:gpt-4o-mini",
        analysis_template=CONCISE_ANALYSIS_TEMPLATE
    )
    print(" Using pre-built CONCISE_ANALYSIS_TEMPLATE")
    
    # Detailed template
    reflector_prebuilt_detailed = Reflector(
        model="openai:gpt-4o-mini",
        analysis_template=DETAILED_ANALYSIS_TEMPLATE
    )
    print(" Using pre-built DETAILED_ANALYSIS_TEMPLATE")
    
    # Domain-specific template (requires domain parameter)
    finance_template = DOMAIN_SPECIFIC_TEMPLATE.replace("{domain}", "financial services")
    reflector_finance = Reflector(
        model="openai:gpt-4o-mini",
        analysis_template=finance_template
    )
    print(" Using pre-built DOMAIN_SPECIFIC_TEMPLATE (financial services)")
    
    # Example 6: Multilingual prompts
    print("\n" + "=" * 60)
    print("Example 6: Multilingual Prompts (Spanish)")
    print("=" * 60)
    
    spanish_system = """Eres un experto en análisis de IA y extracción de conocimientos."""
    
    spanish_template = """Analiza esta interacción y extrae conclusiones accionables.

PREGUNTA: {question}
RESPUESTA: {model_response}
FEEDBACK: {user_feedback} (Tipo: {feedback_type}, Calificación: {rating}/5)

Proporciona análisis en JSON:
{{
    "error_identification": "qué salió mal",
    "root_cause_analysis": "por qué sucedió",
    "correct_approach": "qué hacer en su lugar",
    "key_insight": "estrategia accionable",
    "confidence": 0.8
}}"""
    
    reflector_spanish = Reflector(
        model="openai:gpt-4o-mini",
        system_prompt=spanish_system,
        analysis_template=spanish_template
    )
    
    print(" Using Spanish prompts for international deployment")
    
    # Summary
    print("\n" + "=" * 60)
    print(" When to Use Custom Prompts")
    print("=" * 60)
    
    print("""
     Use Cases for Custom Prompts:
    
    1. **Domain-Specific Applications**
       - Healthcare: Medical accuracy, empathy, compliance
       - Finance: Regulatory compliance, risk assessment
       - Legal: Accuracy, citations, disclaimers
       - Education: Pedagogical approach, age-appropriateness
    
    2. **Response Style**
       - Concise: Fast analysis, token-efficient
       - Detailed: Thorough analysis, training purposes
       - Structured: Specific format requirements
    
    3. **Language/Locale**
       - Multilingual deployment
       - Cultural sensitivity
       - Local compliance requirements
    
    4. **Specific Focus Areas**
       - Safety-critical systems
       - Customer satisfaction metrics
       - Technical accuracy
       - Tone and empathy
    
     Tips:
    - Start with default prompts and customize as needed
    - Test custom prompts on representative samples
    - Keep templates focused and actionable
    - Include output format requirements
    - Balance detail with token efficiency
    """)
    
    # Code template
    print("\n" + "=" * 60)
    print(" Quick Start Template")
    print("=" * 60)
    
    print("""
# Define custom prompts
my_system_prompt = "You are a [domain] expert..."
my_template = \"\"\"Analyze this [context]:
Q: {question}
A: {model_response}
Feedback: {user_feedback}

Provide JSON with your analysis...
\"\"\"

# Use with Reflector
from ace import Reflector

reflector = Reflector(
    model="openai:gpt-4o-mini",
    system_prompt=my_system_prompt,
    analysis_template=my_template
)

# Use normally - prompts are applied automatically
insight = reflector.analyze_feedback(chat_data, feedback_data)
    """)
    
    print("\n Custom prompts example completed!")


if __name__ == "__main__":
    main()

