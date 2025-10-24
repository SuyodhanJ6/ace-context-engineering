"""
Generator - Task executor component of ACE Framework.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)


@dataclass
class GeneratorResult:
    """Result from Generator task execution."""
    solution: str
    reasoning_trace: str
    bullet_feedback: Dict[str, str]  # bullet_id -> helpful/harmful/neutral


class Generator:
    """
    Generator component - Solves tasks using the current playbook.
    
    The Generator is responsible for:
    1. Receiving task + playbook
    2. Identifying relevant strategies/bullets
    3. Generating reasoning trajectory
    4. Producing solution
    5. Marking which bullets were helpful/harmful
    """
    
    def __init__(
        self,
        model: str = "openai:gpt-4o-mini",
        temperature: float = 0.7,
        **kwargs
    ):
        """
        Initialize the Generator.
        
        Args:
            model: Model identifier (e.g., "openai:gpt-4o-mini")
            temperature: Temperature for model generation
            **kwargs: Additional model parameters
        """
        self.model = self._create_model(model, temperature, **kwargs)
        self.temperature = temperature
        
        logger.info(f"Generator initialized with model: {model}")
    
    def _create_model(self, model_name: str, temperature: float, **kwargs) -> BaseLanguageModel:
        """Create the language model instance."""
        if model_name.startswith("openai:"):
            model_id = model_name.split(":", 1)[1]
            return ChatOpenAI(
                model=model_id,
                temperature=temperature,
                **kwargs
            )
        elif model_name.startswith("anthropic:"):
            model_id = model_name.split(":", 1)[1]
            return ChatAnthropic(
                model=model_id,
                temperature=temperature,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported model: {model_name}")
    
    def solve_task(
        self,
        task: str,
        playbook,
        context: Optional[Dict[str, Any]] = None
    ) -> GeneratorResult:
        """
        Solve a task using the current playbook.
        
        Args:
            task: Task description
            playbook: PlaybookManager instance
            context: Additional context
            
        Returns:
            GeneratorResult with solution and feedback
        """
        logger.info(f"Generator solving task: {task}")
        
        # Get relevant bullets from playbook
        relevant_bullets = playbook.get_relevant_bullets(task, top_k=10)
        
        # Create prompt with playbook context
        prompt = self._create_prompt(task, relevant_bullets, context)
        
        # Generate solution
        response = self.model.invoke(prompt)
        solution = response.content
        
        # Extract reasoning trace and bullet feedback
        reasoning_trace, bullet_feedback = self._parse_response(solution)
        
        logger.info(f"Generator completed task: {len(solution)} chars")
        
        return GeneratorResult(
            solution=solution,
            reasoning_trace=reasoning_trace,
            bullet_feedback=bullet_feedback
        )
    
    def _create_prompt(
        self,
        task: str,
        bullets: List,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create the prompt for the Generator."""
        
        playbook_content = self._format_playbook(bullets)
        
        prompt = f"""You are an expert agent with access to a curated playbook.

PLAYBOOK:
{playbook_content}

TASK:
{task}

{f"ADDITIONAL CONTEXT:\n{context}" if context else ""}

Instructions:
1. Read the playbook carefully
2. Identify relevant strategies and bullets
3. Apply them to solve the task
4. Mark which bullets were helpful/harmful/neutral
5. Provide your reasoning trace

Output format:
SOLUTION: [Your solution here]

REASONING: [Your reasoning trace here]

BULLET_FEEDBACK:
- [bullet_id]: [helpful/harmful/neutral] - [reason]
- [bullet_id]: [helpful/harmful/neutral] - [reason]
"""
        return prompt
    
    def _format_playbook(self, bullets: List) -> str:
        """Format bullets for the prompt."""
        if not bullets:
            return "No relevant strategies found in playbook."
        
        formatted = []
        for bullet in bullets:
            formatted.append(f"[{bullet.id}] helpful={bullet.helpful_count} harmful={bullet.harmful_count} ::\n{bullet.content}")
        
        return "\n\n".join(formatted)
    
    def _parse_response(self, response: str) -> tuple[str, Dict[str, str]]:
        """Parse the Generator response to extract reasoning and feedback."""
        reasoning_trace = ""
        bullet_feedback = {}
        
        # Extract reasoning trace
        if "REASONING:" in response:
            reasoning_start = response.find("REASONING:") + len("REASONING:")
            reasoning_end = response.find("BULLET_FEEDBACK:", reasoning_start)
            if reasoning_end == -1:
                reasoning_end = len(response)
            reasoning_trace = response[reasoning_start:reasoning_end].strip()
        
        # Extract bullet feedback
        if "BULLET_FEEDBACK:" in response:
            feedback_start = response.find("BULLET_FEEDBACK:") + len("BULLET_FEEDBACK:")
            feedback_section = response[feedback_start:].strip()
            
            for line in feedback_section.split('\n'):
                if line.strip().startswith('-'):
                    # Parse bullet feedback line
                    parts = line.strip()[1:].strip().split(':', 1)
                    if len(parts) == 2:
                        bullet_id = parts[0].strip()
                        feedback_text = parts[1].strip()
                        
                        # Extract helpful/harmful/neutral
                        if 'helpful' in feedback_text.lower():
                            bullet_feedback[bullet_id] = 'helpful'
                        elif 'harmful' in feedback_text.lower():
                            bullet_feedback[bullet_id] = 'harmful'
                        else:
                            bullet_feedback[bullet_id] = 'neutral'
        
        return reasoning_trace, bullet_feedback
