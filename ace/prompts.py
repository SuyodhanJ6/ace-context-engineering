"""
Default prompt templates for ACE components.

Users can override these templates to customize ACE's behavior.
"""

from typing import Dict, Any


class ReflectorPrompts:
    """Prompt templates for the Reflector component."""
    
    DEFAULT_SYSTEM_PROMPT = """You are an expert at analyzing AI model failures and extracting actionable insights for improvement."""
    
    DEFAULT_ANALYSIS_TEMPLATE = """Analyze why this response received feedback and extract actionable insights.

QUESTION: {question}

MODEL RESPONSE: {model_response}

USER FEEDBACK: {user_feedback}
FEEDBACK TYPE: {feedback_type}
RATING: {rating}/5

Based on the user's feedback, analyze and provide:

1. ERROR IDENTIFICATION: What specifically was wrong or missing in the response?
2. ROOT CAUSE ANALYSIS: Why did the model make this mistake? What was the underlying issue?
3. CORRECT APPROACH: What should have been done instead?
4. KEY INSIGHT: What actionable strategy should be added to the playbook to prevent this in future?

IMPORTANT: The key_insight should be a CLEAR, ACTIONABLE strategy in this format:
- For SUCCESS patterns: "When answering [question type], use this approach: [specific steps]"
- For ERROR patterns: "When [situation], avoid [mistake] and instead [correct approach]"
- Use numbered lists for multiple steps: "1. First step, 2. Second step, 3. Third step"
- Be specific and practical, NOT technical object data

Output your analysis as JSON with these exact fields:
{{
    "reasoning": "Detailed analysis reasoning explaining the overall evaluation",
    "error_identification": "Specific description of what was wrong",
    "root_cause_analysis": "Why this mistake happened",
    "correct_approach": "What should have been done",
    "key_insight": "Clear, actionable strategy for the playbook (human-readable, not technical data)",
    "bullet_tags": [
        {{"id": "ctx-00123", "tag": "helpful"}},
        {{"id": "ctx-00456", "tag": "harmful"}}
    ],
    "confidence": 0.8
}}

IMPORTANT: Include bullet_tags array if you can identify which playbook bullets were helpful/harmful.
If not provided, tags will be generated automatically based on feedback rating.

Be specific and actionable. The key_insight should be a concrete, human-readable strategy that can be added to a playbook."""
    
    @classmethod
    def format_analysis_prompt(
        cls,
        question: str,
        model_response: str,
        user_feedback: str,
        feedback_type: str,
        rating: int,
        custom_template: str = None
    ) -> str:
        """Format the analysis prompt with given data.
        
        Args:
            question: User question
            model_response: Model response
            user_feedback: User feedback text
            feedback_type: Type of feedback
            rating: Rating score (1-5)
            custom_template: Optional custom template (uses DEFAULT_ANALYSIS_TEMPLATE if None)
            
        Returns:
            Formatted prompt string
        """
        template = custom_template or cls.DEFAULT_ANALYSIS_TEMPLATE
        
        return template.format(
            question=question,
            model_response=model_response,
            user_feedback=user_feedback,
            feedback_type=feedback_type,
            rating=rating
        )
    
    @classmethod
    def format_auto_critique_prompt(
        cls,
        question: str,
        model_response: str,
        custom_template: str = None
    ) -> str:
        """Format the auto-critique prompt with given data.
        
        Args:
            question: User question
            model_response: Model response to evaluate
            custom_template: Optional custom template (uses AUTO_CRITIQUE_TEMPLATE if None)
            
        Returns:
            Formatted auto-critique prompt string
        """
        from ace.prompts import AUTO_CRITIQUE_TEMPLATE
        template = custom_template or AUTO_CRITIQUE_TEMPLATE
        
        return template.format(
            question=question,
            model_response=model_response
        )


# Example custom templates users can use

CONCISE_ANALYSIS_TEMPLATE = """Analyze this feedback briefly.

Q: {question}
A: {model_response}
Feedback: {user_feedback} (Type: {feedback_type}, Rating: {rating}/5)

Provide JSON:
{{
    "error_identification": "what went wrong",
    "root_cause_analysis": "why",
    "correct_approach": "what to do",
    "key_insight": "actionable strategy",
    "confidence": 0.8
}}"""


DETAILED_ANALYSIS_TEMPLATE = """You are a meticulous AI improvement specialist. Perform deep analysis on this interaction.

=== INTERACTION DATA ===
QUESTION: {question}

MODEL RESPONSE: {model_response}

USER FEEDBACK: {user_feedback}
FEEDBACK TYPE: {feedback_type}
RATING: {rating}/5

=== ANALYSIS REQUIREMENTS ===

1. ERROR IDENTIFICATION
   - Identify SPECIFIC issues in the response
   - Point out factual errors, tone problems, missing information, etc.
   - Be precise about what exactly was wrong

2. ROOT CAUSE ANALYSIS
   - Why did this error occur?
   - Was it lack of context, misunderstanding, poor reasoning?
   - Identify patterns that led to the mistake

3. CORRECT APPROACH
   - What should the model have done instead?
   - Provide step-by-step correct methodology
   - Include specific techniques or checks to use

4. KEY INSIGHT
   - Distill this into ONE actionable strategy
   - Make it reusable for similar situations
   - Format as clear, numbered steps if complex

=== OUTPUT FORMAT ===
Provide your analysis as JSON:
{{
    "error_identification": "Detailed description of the error",
    "root_cause_analysis": "Deep analysis of why this happened",
    "correct_approach": "Step-by-step correct methodology",
    "key_insight": "Concise, actionable strategy for the playbook",
    "confidence": 0.8
}}

Be thorough, specific, and actionable."""


DOMAIN_SPECIFIC_TEMPLATE = """As a domain expert, analyze this interaction in the context of {domain}.

QUESTION: {question}
RESPONSE: {model_response}
FEEDBACK: {user_feedback} ({feedback_type}, {rating}/5)

Analyze from a {domain} perspective:
1. What domain-specific knowledge was missing or incorrect?
2. Which {domain} best practices were violated?
3. What {domain}-specific approach should have been used?
4. What key {domain} insight can we extract?

Output JSON:
{{
    "error_identification": "domain-specific issue",
    "root_cause_analysis": "why this matters in {domain}",
    "correct_approach": "{domain} best practice",
    "key_insight": "actionable {domain} strategy",
    "confidence": 0.8
}}"""


# Auto-critique template (for evaluating responses without user feedback)
AUTO_CRITIQUE_TEMPLATE = """Evaluate this response for quality, completeness, and accuracy.

QUESTION: {question}

MODEL RESPONSE: {model_response}

EVALUATION CRITERIA:
1. Is the response accurate and factual?
2. Is it complete enough to answer the question?
3. Does it follow best practices?
4. Are there any obvious issues or missing information?
5. Could the response be improved?

IMPORTANT INSTRUCTIONS:
- If the response is GOOD (accurate, complete, well-structured), indicate LOW confidence (< 0.5)
- If there are ISSUES (errors, missing info, poor quality), provide HIGHER confidence (> 0.6)
- Be conservative to avoid false positives
- Only flag genuine problems that need correction

Output your evaluation as JSON:
{{
    "error_identification": "Describe what's wrong (or 'Response is satisfactory' if good)",
    "root_cause_analysis": "Why this issue exists (if any)",
    "correct_approach": "What should be done instead (if issues found)",
    "key_insight": "Actionable improvement strategy (only if confidence > 0.6)",
    "confidence": 0.0-1.0
}}

Be specific and actionable. Only suggest improvements for genuine issues."""

