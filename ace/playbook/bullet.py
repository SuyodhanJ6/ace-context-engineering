"""
Bullet - Individual knowledge unit in ACE playbooks.
"""

from dataclasses import dataclass
from typing import Optional, List
import uuid
from datetime import datetime


@dataclass
class Bullet:
    """
    Individual bullet in the ACE playbook.
    
    Each bullet represents a piece of knowledge or strategy
    with tracking for helpfulness and harmfulness.
    """
    
    id: str
    content: str
    section: str = "general"
    helpful_count: int = 0
    harmful_count: int = 0
    created_at: datetime = None
    updated_at: datetime = None
    tags: List[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.tags is None:
            self.tags = []
    
    @classmethod
    def create(
        cls,
        content: str,
        section: str = "general",
        tags: Optional[List[str]] = None
    ) -> "Bullet":
        """
        Create a new bullet.
        
        Args:
            content: The bullet content/strategy
            section: Section this bullet belongs to
            tags: Optional tags for categorization
            
        Returns:
            New Bullet instance
        """
        bullet_id = f"ctx-{str(uuid.uuid4())[:8]}"
        
        return cls(
            id=bullet_id,
            content=content,
            section=section,
            tags=tags or []
        )
    
    def mark_helpful(self) -> None:
        """Mark this bullet as helpful."""
        self.helpful_count += 1
        self.updated_at = datetime.now()
    
    def mark_harmful(self) -> None:
        """Mark this bullet as harmful."""
        self.harmful_count += 1
        self.updated_at = datetime.now()
    
    def mark_neutral(self) -> None:
        """Mark this bullet as neutral (no change to counters)."""
        self.updated_at = datetime.now()
    
    @property
    def net_score(self) -> int:
        """Calculate net helpfulness score."""
        return self.helpful_count - self.harmful_count
    
    @property
    def is_helpful(self) -> bool:
        """Check if bullet is overall helpful."""
        return self.net_score > 0
    
    @property
    def is_harmful(self) -> bool:
        """Check if bullet is overall harmful."""
        return self.net_score < 0
    
    @property
    def is_neutral(self) -> bool:
        """Check if bullet is neutral."""
        return self.net_score == 0
    
    def to_markdown(self) -> str:
        """
        Convert bullet to markdown format.
        
        Returns:
            Markdown formatted string representation
        """
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        score_str = f" (+{self.helpful_count}/-{self.harmful_count})"
        
        return f"- **[{self.id}]** {self.content}{tags_str}{score_str}"
    
    def to_dict(self) -> dict:
        """Convert bullet to dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "section": self.section,
            "helpful_count": self.helpful_count,
            "harmful_count": self.harmful_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Bullet":
        """Create bullet from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            section=data["section"],
            helpful_count=data["helpful_count"],
            harmful_count=data["harmful_count"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            tags=data.get("tags", [])
        )
    
    def __str__(self) -> str:
        """String representation of bullet."""
        return f"[{self.id}] helpful={self.helpful_count} harmful={self.harmful_count} :: {self.content[:100]}..."
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"Bullet(id='{self.id}', section='{self.section}', net_score={self.net_score})"
