"""
ACE Framework - Main orchestrator for the Agentic Context Engineering system.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import logging

from .core.generator import Generator
from .core.reflector import Reflector  
from .core.curator import Curator
from .playbook.manager import PlaybookManager
from .config import ModelConfig, ACEConfig

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """Result of a task execution with ACE framework."""
    solution: str
    reasoning_trace: str
    bullet_feedback: Dict[str, str]
    insights: Optional[Dict[str, Any]] = None
    playbook_updates: Optional[Dict[str, Any]] = None


class ACEFramework:
    """
    Main ACE Framework orchestrator.
    
    Coordinates Generator, Reflector, and Curator to create self-improving
    language model systems through evolving playbooks.
    """
    
    def __init__(
        self,
        generator_model: Optional[str] = None,
        reflector_model: Optional[str] = None,
        curator_model: Optional[str] = None,
        config: Optional[ACEConfig] = None,
        **kwargs
    ):
        """
        Initialize the ACE Framework.
        
        Args:
            generator_model: Model for the Generator agent
            reflector_model: Model for the Reflector agent  
            curator_model: Model for the Curator agent
            config: ACE configuration object
            **kwargs: Additional configuration parameters
        """
        self.config = config or ACEConfig()
        
        # Initialize core components
        self.generator = Generator(
            model=generator_model or self.config.generator_model,
            temperature=self.config.generator_temperature
        )
        
        self.reflector = Reflector(
            model=reflector_model or self.config.reflector_model,
            temperature=self.config.reflector_temperature
        )
        
        self.curator = Curator(
            model=curator_model or self.config.curator_model,
            temperature=self.config.curator_temperature
        )
        
        # Initialize playbook manager
        self.playbook_manager = PlaybookManager()
        
        logger.info("ACE Framework initialized successfully")
    
    def create_playbook(self, name: str, description: str = "") -> PlaybookManager:
        """
        Create a new playbook.
        
        Args:
            name: Name of the playbook
            description: Description of the playbook
            
        Returns:
            PlaybookManager instance
        """
        return self.playbook_manager.create_playbook(name, description)
    
    def execute_task(
        self,
        task: str,
        playbook: PlaybookManager,
        context: Optional[Dict[str, Any]] = None
    ) -> TaskResult:
        """
        Execute a task using the ACE framework.
        
        Args:
            task: Task description
            playbook: Playbook to use
            context: Additional context for the task
            
        Returns:
            TaskResult with solution and insights
        """
        logger.info(f"Executing task: {task}")
        
        # Step 1: Generator solves the task
        generator_result = self.generator.solve_task(
            task=task,
            playbook=playbook,
            context=context
        )
        
        # Step 2: Reflector analyzes the solution
        reflection_result = self.reflector.analyze_solution(
            task=task,
            solution=generator_result.solution,
            reasoning_trace=generator_result.reasoning_trace,
            playbook_bullets=generator_result.bullet_feedback
        )
        
        # Step 3: Curator updates the playbook
        curator_result = self.curator.update_playbook(
            insights=reflection_result.insights,
            playbook=playbook,
            bullet_feedback=generator_result.bullet_feedback
        )
        
        return TaskResult(
            solution=generator_result.solution,
            reasoning_trace=generator_result.reasoning_trace,
            bullet_feedback=generator_result.bullet_feedback,
            insights=reflection_result.insights,
            playbook_updates=curator_result.updates
        )
    
    def learn_from_tasks(
        self,
        tasks: List[str],
        playbook: PlaybookManager,
        epochs: int = 5,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Learn from multiple tasks over multiple epochs.
        
        Args:
            tasks: List of task descriptions
            playbook: Playbook to update
            epochs: Number of learning epochs
            context: Additional context
            
        Returns:
            Learning results and metrics
        """
        logger.info(f"Starting multi-epoch learning: {epochs} epochs, {len(tasks)} tasks")
        
        results = {
            "epochs": [],
            "total_bullets": [],
            "accuracy_improvements": [],
            "new_insights": []
        }
        
        for epoch in range(epochs):
            logger.info(f"Epoch {epoch + 1}/{epochs}")
            
            epoch_results = []
            for task in tasks:
                result = self.execute_task(task, playbook, context)
                epoch_results.append(result)
            
            # Calculate epoch metrics
            epoch_metrics = self._calculate_epoch_metrics(epoch_results, playbook)
            results["epochs"].append(epoch_metrics)
            results["total_bullets"].append(len(playbook.get_all_bullets()))
            
            logger.info(f"Epoch {epoch + 1} completed: {epoch_metrics}")
        
        return results
    
    def _calculate_epoch_metrics(
        self, 
        results: List[TaskResult], 
        playbook: PlaybookManager
    ) -> Dict[str, Any]:
        """Calculate metrics for an epoch."""
        return {
            "tasks_completed": len(results),
            "new_insights": sum(1 for r in results if r.insights),
            "playbook_updates": sum(1 for r in results if r.playbook_updates),
            "total_bullets": len(playbook.get_all_bullets())
        }
    
    def get_playbook_stats(self, playbook: PlaybookManager) -> Dict[str, Any]:
        """Get statistics about a playbook."""
        bullets = playbook.get_all_bullets()
        
        return {
            "total_bullets": len(bullets),
            "helpful_bullets": sum(1 for b in bullets if b.helpful_count > b.harmful_count),
            "harmful_bullets": sum(1 for b in bullets if b.harmful_count > b.helpful_count),
            "neutral_bullets": sum(1 for b in bullets if b.helpful_count == b.harmful_count),
            "sections": list(set(b.section for b in bullets))
        }
