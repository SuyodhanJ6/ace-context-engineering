"""
Curator Agent for ACE Framework.

Manages playbook updates based on Reflector insights using deterministic operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from ace.reflector import ReflectionInsight
from ace.playbook.manager import PlaybookManager
from ace.playbook.bullet import Bullet
from ace.utils.paths import get_updates_path


@dataclass
class DeltaOperation:
    """Represents a single playbook update operation.
    
    Attributes:
        operation: Type of operation ("ADD", "UPDATE", "DEDUPLICATE")
        bullet_id: ID of bullet (for UPDATE operations)
        content: Content (for ADD operations)
        section: Section name (for ADD operations)
        helpful_increment: Increment for helpful counter
        harmful_increment: Increment for harmful counter
    """
    operation: str  # "ADD", "UPDATE", "DEDUPLICATE"
    bullet_id: Optional[str] = None
    content: Optional[str] = None
    section: Optional[str] = None
    helpful_increment: int = 0
    harmful_increment: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DeltaUpdate:
    """Collection of operations to apply to playbook.
    
    Attributes:
        operations: List of operations to perform
        timestamp: Timestamp of delta creation
        source_feedback_id: ID of feedback that generated this delta
        total_operations: Total number of operations
    """
    operations: List[DeltaOperation]
    timestamp: str
    source_feedback_id: str
    total_operations: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "operations": [op.to_dict() for op in self.operations],
            "timestamp": self.timestamp,
            "source_feedback_id": self.source_feedback_id,
            "total_operations": self.total_operations
        }


class Curator:
    """Manages playbook updates based on Reflector insights.
    
    Uses deterministic operations (no LLM calls) to update the playbook
    based on insights extracted by the Reflector.
    
    Args:
        playbook_manager: PlaybookManager instance
        storage_path: Path for storing delta updates
    
    Example:
        >>> from ace import Curator, PlaybookManager, ACEConfig
        >>> config = ACEConfig()
        >>> playbook = PlaybookManager(
        ...     playbook_dir=config.get_storage_path(),
        ...     vector_store=config.vector_store
        ... )
        >>> curator = Curator(
        ...     playbook_manager=playbook,
        ...     storage_path=config.get_storage_path()
        ... )
    """
    
    def __init__(
        self,
        playbook_manager: PlaybookManager,
        storage_path: Optional[str] = None
    ):
        """Initialize Curator with playbook manager."""
        self.playbook = playbook_manager
        
        # Set up storage
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path.home() / ".ace" / "playbooks" / "default"
        
        self.updates_dir = get_updates_path(self.storage_path)
        
        print(f" Curator initialized")
        print(f" Updates directory: {self.updates_dir}")
    
    def process_insights(
        self,
        insight: ReflectionInsight,
        feedback_id: str
    ) -> DeltaUpdate:
        """Process Reflector insights and create playbook delta.
        
        Args:
            insight: Reflection insight to process
            feedback_id: Feedback identifier
            
        Returns:
            DeltaUpdate with operations
        """
        print(f" Curator processing insights:")
        print(f"   Key insight: {insight.key_insight[:100]}...")
        print(f"   Confidence: {insight.confidence}")
        
        operations = []
        
        # Only process high-confidence insights
        if insight.confidence > 0.5:
            print(f" High confidence insight (>{0.5}), processing...")
            
            # Check if similar insight already exists
            similar_bullets = self._find_similar_bullets(insight.key_insight)
            
            if similar_bullets:
                # UPDATE existing bullet
                best_match = similar_bullets[0]
                print(f" Found similar bullet: {best_match.id}")
                
                formatted_content = self._format_bullet_content(insight)
                
                operations.append(DeltaOperation(
                    operation="UPDATE",
                    bullet_id=best_match.id,
                    content=formatted_content,
                    helpful_increment=1 if insight.confidence > 0.7 else 0,
                    harmful_increment=0
                ))
            else:
                # ADD new bullet
                section = self._determine_section(insight)
                print(f" Creating new bullet in section: {section}")
                
                formatted_content = self._format_bullet_content(insight)
                
                operations.append(DeltaOperation(
                    operation="ADD",
                    content=formatted_content,
                    section=section,
                    helpful_increment=1,
                    harmful_increment=0
                ))
        else:
            print(f"  Low confidence insight ({insight.confidence}), skipping...")
        
        # Create delta update
        delta = DeltaUpdate(
            operations=operations,
            timestamp=datetime.now().isoformat(),
            source_feedback_id=feedback_id,
            total_operations=len(operations)
        )
        
        print(f" Created delta with {len(operations)} operations")
        return delta
    
    def merge_delta(self, delta: DeltaUpdate) -> bool:
        """Apply delta operations to playbook (deterministic, no LLM).
        
        Args:
            delta: DeltaUpdate to apply
            
        Returns:
            True if successful
        """
        print(f" Applying delta operations to playbook...")
        
        try:
            for i, operation in enumerate(delta.operations):
                print(f" Operation {i+1}: {operation.operation}")
                
                if operation.operation == "ADD":
                    # Add new bullet
                    bullet_id = self.playbook.add_bullet(
                        content=operation.content,
                        section=operation.section or "General"
                    )
                    print(f"    Added new bullet: {bullet_id}")
                    
                elif operation.operation == "UPDATE":
                    # Update existing bullet counters
                    if operation.bullet_id:
                        for _ in range(operation.helpful_increment):
                            self.playbook.update_counters(operation.bullet_id, helpful=True)
                        for _ in range(operation.harmful_increment):
                            self.playbook.update_counters(operation.bullet_id, helpful=False)
                        print(f"    Updated bullet: {operation.bullet_id}")
            
            # Save delta log
            self._save_delta_log(delta)
            
            return True
            
        except Exception as e:
            print(f" Error merging delta: {e}")
            return False
    
    def process_negative_feedback(
        self,
        insight: ReflectionInsight,
        feedback_id: str
    ) -> DeltaUpdate:
        """Process negative feedback to identify harmful patterns.
        
        Args:
            insight: Reflection insight
            feedback_id: Feedback identifier
            
        Returns:
            DeltaUpdate with operations
        """
        operations = []
        
        # Only process high-confidence negative feedback
        if insight.confidence > 0.6:
            # Create a "what not to do" bullet
            dont_do_content = f"AVOID: {insight.error_identification}\n\nInstead: {insight.correct_approach}"
            
            operations.append(DeltaOperation(
                operation="ADD",
                content=dont_do_content,
                section="Anti-Patterns",
                helpful_increment=1,
                harmful_increment=0
            ))
        
        return DeltaUpdate(
            operations=operations,
            timestamp=datetime.now().isoformat(),
            source_feedback_id=feedback_id,
            total_operations=len(operations)
        )
    
    def process_positive_feedback(
        self,
        insight: ReflectionInsight,
        feedback_id: str
    ) -> DeltaUpdate:
        """Process positive feedback to reinforce good patterns.
        
        Args:
            insight: Reflection insight
            feedback_id: Feedback identifier
            
        Returns:
            DeltaUpdate with operations
        """
        operations = []
        
        if insight.confidence > 0.5:
            # Create a "success pattern" bullet
            success_content = f"SUCCESS PATTERN: {insight.key_insight}"
            
            operations.append(DeltaOperation(
                operation="ADD",
                content=success_content,
                section="Success Patterns",
                helpful_increment=1,
                harmful_increment=0
            ))
        
        return DeltaUpdate(
            operations=operations,
            timestamp=datetime.now().isoformat(),
            source_feedback_id=feedback_id,
            total_operations=len(operations)
        )
    
    def deduplicate_playbook(self, similarity_threshold: float = 0.9) -> int:
        """Remove duplicate bullets from playbook.
        
        Args:
            similarity_threshold: Cosine similarity threshold
            
        Returns:
            Number of bullets removed
        """
        return self.playbook.deduplicate(similarity_threshold)
    
    def _find_similar_bullets(
        self,
        content: str,
        threshold: float = 0.8
    ) -> List[Bullet]:
        """Find bullets similar to the given content.
        
        Args:
            content: Content to match
            threshold: Similarity threshold
            
        Returns:
            List of similar bullets
        """
        # Use playbook's retrieve_relevant to find similar bullets
        relevant_bullets = self.playbook.retrieve_relevant(content, top_k=5)
        
        # Return top matches (playbook already filters by quality)
        return relevant_bullets[:3]
    
    def _format_bullet_content(self, insight: ReflectionInsight) -> str:
        """Format bullet content from insight.
        
        Args:
            insight: Reflection insight
            
        Returns:
            Formatted content string
        """
        # Clean and format content
        if insight.error_identification and "no error" not in insight.error_identification.lower():
            # Error case - create actionable "avoid" guidance
            formatted = f"When {insight.error_identification.lower()}, avoid this approach and instead: {insight.correct_approach}"
        else:
            # Success case - create actionable "use this" guidance
            formatted = f"When answering similar questions, use this approach: {insight.correct_approach}"
        
        # Apply structured formatting
        formatted = self._apply_structured_formatting(formatted)
        
        # Ensure actionable content
        if not formatted or len(formatted) < 10:
            formatted = self._create_fallback_insight(insight)
        
        return formatted
    
    def _apply_structured_formatting(self, content: str) -> str:
        """Apply structured formatting to content.
        
        Args:
            content: Content to format
            
        Returns:
            Formatted content
        """
        # Convert to numbered list if multiple points
        if '\n' in content and not content.startswith(('1.', '2.', '3.')):
            lines = content.split('\n')
            if len(lines) > 1:
                numbered_lines = []
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        numbered_lines.append(f"{i}. {line.strip()}")
                content = '\n'.join(numbered_lines)
        
        return content.strip()
    
    def _create_fallback_insight(self, insight: ReflectionInsight) -> str:
        """Create fallback insight content.
        
        Args:
            insight: Reflection insight
            
        Returns:
            Fallback content string
        """
        if insight.error_identification and "no error" not in insight.error_identification.lower():
            return f"When {insight.error_identification.lower()}, use this approach: {insight.correct_approach}"
        else:
            return f"Success pattern: {insight.correct_approach}"
    
    def _determine_section(self, insight: ReflectionInsight) -> str:
        """Determine appropriate section for the insight.
        
        Args:
            insight: Reflection insight
            
        Returns:
            Section name
        """
        content_lower = insight.key_insight.lower()
        
        if any(word in content_lower for word in ["explain", "definition", "what is", "describe"]):
            return "Explanation Strategies"
        elif any(word in content_lower for word in ["calculate", "math", "compute", "solve"]):
            return "Calculation Strategies"
        elif any(word in content_lower for word in ["search", "find", "look up", "research"]):
            return "Search Strategies"
        elif any(word in content_lower for word in ["time", "date", "schedule"]):
            return "Time Management"
        elif any(word in content_lower for word in ["user", "personal", "individual"]):
            return "User Interaction"
        elif any(word in content_lower for word in ["error", "mistake", "wrong", "incorrect"]):
            return "Error Prevention"
        elif any(word in content_lower for word in ["format", "structure", "organize", "bullet"]):
            return "Response Formatting"
        else:
            return "General Strategies"
    
    def _save_delta_log(self, delta: DeltaUpdate):
        """Save delta update log for tracking.
        
        Args:
            delta: DeltaUpdate to save
        """
        log_data = delta.to_dict()
        
        filename = f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.updates_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f" Saved delta log to {filepath}")
        except Exception as e:
            print(f"  Error saving delta log: {e}")

