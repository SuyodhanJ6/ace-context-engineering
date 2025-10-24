"""
Reflector Agent for ACE Framework.

Analyzes feedback and extracts actionable insights for playbook improvement.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path

from langchain.chat_models import init_chat_model
from ace.utils.paths import get_reflections_path
from ace.prompts import ReflectorPrompts


@dataclass
class ReflectionInsight:
    """Structured insight extracted from feedback analysis.
    
    Attributes:
        error_identification: What specifically went wrong
        root_cause_analysis: Why the error occurred
        correct_approach: What should have been done instead
        key_insight: Actionable strategy for the playbook
        bullet_tags: Tags for bullets used (helpful/harmful)
        confidence: Confidence score (0.0 to 1.0)
    """
    error_identification: str
    root_cause_analysis: str
    correct_approach: str
    key_insight: str
    bullet_tags: List[Dict[str, str]]
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReflectionInsight":
        """Create from dictionary."""
        return cls(**data)


class Reflector:
    """Analyzes feedback and extracts insights for playbook improvement.
    
    Uses LLM to perform deep analysis of user feedback and extract
    actionable insights that can be added to the playbook.
    
    Args:
        model: Model name (LangChain format: "provider:model")
        storage_path: Path for storing reflections
        temperature: Temperature for LLM calls
        system_prompt: Custom system prompt (optional, uses default if None)
        analysis_template: Custom analysis template (optional, uses default if None)
    
    Example:
        >>> from ace import Reflector, ACEConfig
        >>> config = ACEConfig()
        >>> reflector = Reflector(
        ...     model=config.chat_model,
        ...     storage_path=config.get_storage_path()
        ... )
        
        >>> # With custom prompts
        >>> custom_system = "You are a customer service expert..."
        >>> custom_template = "Analyze this: Q: {question}..."
        >>> reflector = Reflector(
        ...     model="openai:gpt-4o-mini",
        ...     system_prompt=custom_system,
        ...     analysis_template=custom_template
        ... )
    """
    
    def __init__(
        self,
        model: str = "openai:gpt-4o-mini",
        storage_path: Optional[str] = None,
        temperature: float = 0.3,
        system_prompt: Optional[str] = None,
        analysis_template: Optional[str] = None,
        auto_critique_template: Optional[str] = None,
        max_refinement_iterations: int = 1
    ):
        """Initialize Reflector with LLM and storage.
        
        Args:
            model: Model name (LangChain format)
            storage_path: Path for storing reflections
            temperature: Temperature for LLM calls
            system_prompt: Custom system prompt (optional)
            analysis_template: Custom analysis template (optional)
            auto_critique_template: Custom auto-critique template (optional)
            max_refinement_iterations: Number of refinement iterations (1-5, default: 1)
                                     Paper uses up to 5 iterations for better insights
        """
        # Initialize chat model using LangChain
        print(f" Initializing Reflector with model: {model}")
        self.model = init_chat_model(model, temperature=temperature)
        
        # Set up storage
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path.home() / ".ace" / "playbooks" / "default"
        
        self.reflections_dir = get_reflections_path(self.storage_path)
        
        # Set up prompts
        self.system_prompt = system_prompt or ReflectorPrompts.DEFAULT_SYSTEM_PROMPT
        self.analysis_template = analysis_template or ReflectorPrompts.DEFAULT_ANALYSIS_TEMPLATE
        self.auto_critique_template = auto_critique_template  # Can be None, will use default
        
        # Set up refinement iterations (paper uses up to 5)
        self.max_refinement_iterations = min(max(1, max_refinement_iterations), 5)
        
        if system_prompt:
            print(f"  Using custom system prompt")
        if analysis_template:
            print(f"  Using custom analysis template")
        if auto_critique_template:
            print(f"  Using custom auto-critique template")
        if max_refinement_iterations > 1:
            print(f" Multi-iteration refinement enabled ({max_refinement_iterations} iterations)")
        
        print(f" Reflector storage: {self.reflections_dir}")
    
    def analyze_feedback(
        self,
        chat_data: Dict[str, Any],
        feedback_data: Any = None,
        refine: bool = True
    ) -> ReflectionInsight:
        """Analyze user feedback and extract insights.
        
        Can also perform auto-critique when no feedback is provided.
        
        Args:
            chat_data: Chat interaction data with 'question' and 'model_response'
            feedback_data: User feedback data (optional - if None, runs auto-critique)
            refine: Whether to use multi-iteration refinement (default: True)
            
        Returns:
            ReflectionInsight with extracted insights
            
        Example:
            >>> # With user feedback
            >>> insight = reflector.analyze_feedback(chat_data, feedback_data)
            
            >>> # Auto-critique (no feedback)
            >>> insight = reflector.analyze_feedback(chat_data, feedback_data=None)
        """
        # Extract data
        question = chat_data.get("question", "")
        model_response = chat_data.get("model_response", "")
        
        # Check if this is auto-critique (no feedback provided)
        is_auto_critique = feedback_data is None or getattr(feedback_data, "feedback_type", "") == "auto_critique"
        
        if is_auto_critique:
            # AUTO-CRITIQUE mode
            print(f" Running auto-critique:")
            print(f"   Question: {question[:50]}...")
            user_feedback = ""
            feedback_type = "auto_critique"
            rating = 3
        else:
            # NORMAL feedback mode
            user_feedback = getattr(feedback_data, "user_feedback", "")
            feedback_type = getattr(feedback_data, "feedback_type", "")
            rating = getattr(feedback_data, "rating", 3)
            
            print(f" Analyzing feedback:")
            print(f"   Question: {question[:50]}...")
            print(f"   Type: {feedback_type}, Rating: {rating}/5")
        
        # Generate initial reflection
        reflection = self._generate_reflection(
            question=question,
            model_response=model_response,
            user_feedback=user_feedback,
            feedback_type=feedback_type,
            rating=rating
        )
        
        # Multi-iteration refinement (paper: up to 5 iterations)
        if refine and self.max_refinement_iterations > 1:
            print(f" Refining insight over {self.max_refinement_iterations} iterations...")
            reflection = self._refine_reflection(
                reflection=reflection,
                question=question,
                model_response=model_response,
                user_feedback=user_feedback,
                feedback_type=feedback_type,
                rating=rating
            )
        
        # Adjust confidence for auto-critique (more conservative)
        if is_auto_critique and reflection.confidence > 0.7:
            original_confidence = reflection.confidence
            reflection.confidence = reflection.confidence * 0.85
            print(f"    Adjusted confidence for auto-critique: {original_confidence:.2f} → {reflection.confidence:.2f}")
        
        # Save reflection
        if feedback_data and hasattr(feedback_data, "feedback_id"):
            self._save_reflection(feedback_data.feedback_id, reflection)
        
        return reflection
    
    def extract_insights_from_success(
        self,
        question: str,
        model_response: str,
        feedback_type: str,
        rating: int
    ) -> ReflectionInsight:
        """Extract insights from positive feedback.
        
        Args:
            question: User question
            model_response: Model response
            feedback_type: Type of feedback
            rating: Rating (1-5)
            
        Returns:
            ReflectionInsight for successful pattern
        """
        if rating >= 4:
            return ReflectionInsight(
                error_identification="No errors - successful response",
                root_cause_analysis="Response met user expectations",
                correct_approach="Continue using this approach",
                key_insight=f"When answering '{question}', use this successful pattern: {model_response[:200]}",
                bullet_tags=[],
                confidence=0.8
            )
        else:
            return ReflectionInsight(
                error_identification="Partially successful response",
                root_cause_analysis="Response had some value but could be improved",
                correct_approach="Build on what worked, improve what didn't",
                key_insight=f"Partial success pattern for '{question}': {model_response[:200]}",
                bullet_tags=[],
                confidence=0.6
            )
    
    def _generate_reflection(
        self,
        question: str,
        model_response: str,
        user_feedback: str,
        feedback_type: str,
        rating: int
    ) -> ReflectionInsight:
        """Use LLM to analyze feedback and extract insights.
        
        Args:
            question: User question
            model_response: Model response
            user_feedback: User feedback text (empty for auto-critique)
            feedback_type: Type of feedback ("auto_critique" for automatic evaluation)
            rating: Rating score
            
        Returns:
            ReflectionInsight with analysis
        """
        # Choose the appropriate prompt template
        if feedback_type == "auto_critique":
            # Use auto-critique template
            prompt = ReflectorPrompts.format_auto_critique_prompt(
                question=question,
                model_response=model_response,
                custom_template=self.auto_critique_template
            )
        else:
            # Use normal analysis template
            prompt = ReflectorPrompts.format_analysis_prompt(
                question=question,
                model_response=model_response,
                user_feedback=user_feedback,
                feedback_type=feedback_type,
                rating=rating,
                custom_template=self.analysis_template
            )

        try:
            print(" Sending reflection prompt to LLM...")
            response = self.model.invoke([
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ])
            
            # Parse JSON response
            content = response.content.strip()
            print(f" Received reflection (length: {len(content)} chars)")
            
            # Extract JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            
            # Parse JSON
            try:
                analysis = json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                analysis = {
                    "error_identification": user_feedback,
                    "root_cause_analysis": "Unable to analyze automatically",
                    "correct_approach": "Review user feedback for guidance",
                    "key_insight": f"User feedback: {user_feedback}",
                    "confidence": 0.5
                }
            
            # Create ReflectionInsight
            insight = ReflectionInsight(
                error_identification=analysis.get("error_identification", user_feedback),
                root_cause_analysis=analysis.get("root_cause_analysis", "Analysis failed"),
                correct_approach=analysis.get("correct_approach", "Manual review needed"),
                key_insight=analysis.get("key_insight", f"User feedback: {user_feedback}"),
                bullet_tags=[],
                confidence=analysis.get("confidence", 0.5)
            )
            
            print(f" Generated reflection (confidence: {insight.confidence})")
            return insight
            
        except Exception as e:
            print(f" Error in reflection generation: {e}")
            # Return fallback insight
            return ReflectionInsight(
                error_identification=user_feedback,
                root_cause_analysis="Reflection generation failed",
                correct_approach="Manual review required",
                key_insight=f"User feedback: {user_feedback}",
                bullet_tags=[],
                confidence=0.3
            )
    
    def _refine_reflection(
        self,
        reflection: ReflectionInsight,
        question: str,
        model_response: str,
        user_feedback: str,
        feedback_type: str,
        rating: int
    ) -> ReflectionInsight:
        """Refine reflection over multiple iterations (paper: up to 5).
        
        Each iteration improves the quality of extracted insights.
        
        Args:
            reflection: Initial reflection to refine
            question: User question
            model_response: Model response
            user_feedback: User feedback
            feedback_type: Type of feedback
            rating: Rating score
            
        Returns:
            Refined ReflectionInsight
        """
        current_reflection = reflection
        
        for iteration in range(2, self.max_refinement_iterations + 1):
            print(f"    Refinement iteration {iteration}/{self.max_refinement_iterations}...")
            
            # Build refinement prompt
            refinement_prompt = f"""Review and refine this analysis to extract better insights.

ORIGINAL DATA:
Question: {question}
Response: {model_response}
Feedback: {user_feedback} ({feedback_type}, {rating}/5)

CURRENT ANALYSIS:
Error: {current_reflection.error_identification}
Root Cause: {current_reflection.root_cause_analysis}
Correct Approach: {current_reflection.correct_approach}
Key Insight: {current_reflection.key_insight}
Confidence: {current_reflection.confidence}

REFINEMENT INSTRUCTIONS:
1. Make the error identification more specific
2. Deepen the root cause analysis
3. Make the correct approach more actionable
4. Improve the key insight to be clearer and more reusable
5. Adjust confidence based on clarity

Provide refined JSON:
{{
    "error_identification": "more specific error description",
    "root_cause_analysis": "deeper root cause analysis",
    "correct_approach": "more actionable approach",
    "key_insight": "clearer, more reusable insight",
    "confidence": 0.0-1.0
}}"""
            
            try:
                response = self.model.invoke([
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": refinement_prompt}
                ])
                
                # Parse refined analysis
                content = response.content.strip()
                
                # Extract JSON
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                
                analysis = json.loads(content)
                
                # Update reflection with refined analysis
                current_reflection = ReflectionInsight(
                    error_identification=analysis.get("error_identification", current_reflection.error_identification),
                    root_cause_analysis=analysis.get("root_cause_analysis", current_reflection.root_cause_analysis),
                    correct_approach=analysis.get("correct_approach", current_reflection.correct_approach),
                    key_insight=analysis.get("key_insight", current_reflection.key_insight),
                    bullet_tags=current_reflection.bullet_tags,
                    confidence=analysis.get("confidence", current_reflection.confidence)
                )
                
                print(f"       Refined (confidence: {current_reflection.confidence})")
                
            except Exception as e:
                print(f"        Refinement iteration {iteration} failed: {e}")
                # Continue with current reflection
                break
        
        return current_reflection
    
    def _save_reflection(self, feedback_id: str, reflection: ReflectionInsight):
        """Save reflection to file.
        
        Args:
            feedback_id: Feedback identifier
            reflection: Reflection insight to save
        """
        reflection_data = {
            "feedback_id": feedback_id,
            "timestamp": datetime.now().isoformat(),
            **reflection.to_dict()
        }
        
        filename = f"reflection_{feedback_id}.json"
        filepath = self.reflections_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(reflection_data, f, indent=2)
            print(f" Saved reflection to {filepath}")
        except Exception as e:
            print(f"  Error saving reflection: {e}")

