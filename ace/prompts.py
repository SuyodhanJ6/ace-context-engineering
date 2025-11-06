"""
Default prompt templates for ACE components.

Users can override these templates to customize ACE's behavior.
"""

from typing import Dict, Any


class ReflectorPrompts:
    """Prompt templates for the Reflector component."""
    
    DEFAULT_SYSTEM_PROMPT = """You are an expert at analyzing AI model failures and extracting actionable insights for improvement."""
    
    DEFAULT_ANALYSIS_TEMPLATE = """You are a senior reviewer diagnosing the generator's trajectory.
Use the playbook, model response, and feedback to identify mistakes and actionable insights.
Even if model reasoning is not available, analyze the response itself to determine what went wrong and what the correct approach should be.
Output must be a single valid JSON object. Do NOT include analysis text or explanations outside the JSON.
Begin the response with `{{` and end with `}}`.

Question:
{question}

{model_reasoning_section}

Model response:
{model_response}

{ground_truth_section}

Feedback:
{feedback}

{feedback_type_section}
Rating: {rating}/5

Playbook excerpts consulted:
{playbook_excerpts}

Analyze and provide:

1. ERROR IDENTIFICATION: What specifically was wrong or missing in the response?
   - Analyze the model response itself if reasoning is not available
   - Compare with feedback to identify specific issues
   - Identify what mistake was made

2. ROOT CAUSE ANALYSIS: Why did the model make this mistake? What was the underlying issue?
   - Infer the root cause from the response and feedback
   - Consider if playbook bullets were misapplied or missing

3. CORRECT APPROACH: What should have been done instead?
   - Provide the correct methodology or steps
   - This is what we want to add to the playbook

4. KEY INSIGHT: What actionable strategy should be added to the playbook to prevent this in future?
   - This should be a clear, reusable strategy
   - Format as actionable guidance

IMPORTANT: The key_insight should be a CLEAR, ACTIONABLE strategy in this format:
- For SUCCESS patterns: "When answering [question type], use this approach: [specific steps]"
- For ERROR patterns: MUST include BOTH the mistake AND correct approach:
  * Format: "When [situation], avoid [mistake] and instead [correct approach]"
  * Or: "Never [mistake]. Instead, [correct approach]"
  * Or numbered format: "1. Avoid [mistake], 2. Instead do [correct approach]"
- Use numbered lists for multiple steps: "1. First step, 2. Second step, 3. Third step"
- Be specific and practical, NOT technical object data
- ALWAYS include what NOT to do (mistake) AND what TO do (correct approach) for error patterns

Return JSON:
{{
    "reasoning": "<detailed analysis reasoning explaining the overall evaluation>",
    "error_identification": "<what went wrong - analyze response and feedback>",
    "root_cause_analysis": "<why it happened - infer from response and feedback>",
    "correct_approach": "<what should be done - the correct method>",
    "key_insight": "<reusable takeaway - clear, actionable strategy for the playbook>",
    "bullet_tags": [
        {{"id": "<bullet-id>", "tag": "helpful|harmful|neutral"}}
    ],
    "confidence": 0.8
}}

IMPORTANT: 
- Include bullet_tags array if you can identify which playbook bullets were helpful/harmful
- If bullet_tags not provided, tags will be generated automatically based on feedback rating
- Be specific and actionable. The key_insight should be a concrete, human-readable strategy that can be added to a playbook
- Even without model reasoning, you can analyze the response itself to identify mistakes and correct approaches"""
    
    @classmethod
    def format_analysis_prompt(
        cls,
        question: str,
        model_response: str,
        user_feedback: str,
        feedback_type: str,
        rating: int,
        model_reasoning: str = "",
        ground_truth: str = "",
        playbook_excerpts: str = "",
        custom_template: str = None
    ) -> str:
        """Format the analysis prompt with given data.
        
        Args:
            question: User question
            model_response: Model response
            user_feedback: User feedback text
            feedback_type: Type of feedback
            rating: Rating score (1-5)
            model_reasoning: Model's reasoning/chain of thought (optional)
            ground_truth: Ground truth answer (optional)
            playbook_excerpts: Playbook bullets that were used (optional)
            custom_template: Optional custom template (uses DEFAULT_ANALYSIS_TEMPLATE if None)
            
        Returns:
            Formatted prompt string
        """
        template = custom_template or cls.DEFAULT_ANALYSIS_TEMPLATE
        
        # Format playbook excerpts if provided
        if not playbook_excerpts:
            playbook_excerpts = "No playbook bullets were used in this interaction."
        
        # Format model reasoning section (only include if available)
        if model_reasoning and model_reasoning.strip() and "Not available" not in model_reasoning:
            model_reasoning_section = f"Model reasoning:\n{model_reasoning}"
        else:
            model_reasoning_section = ""
        
        # Format ground truth section (only include if available)
        if ground_truth and ground_truth.strip() and "Not available" not in ground_truth:
            ground_truth_section = f"Ground truth (if available):\n{ground_truth}"
        else:
            ground_truth_section = ""
        
        # Format feedback type section (only include if provided and not empty)
        if feedback_type and feedback_type.strip() and feedback_type != "user_feedback":
            feedback_type_section = f"Feedback type: {feedback_type}"
        else:
            feedback_type_section = ""
        
        return template.format(
            question=question,
            model_reasoning_section=model_reasoning_section,
            model_response=model_response,
            ground_truth_section=ground_truth_section,
            feedback=user_feedback,
            feedback_type_section=feedback_type_section,
            rating=rating,
            playbook_excerpts=playbook_excerpts
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

