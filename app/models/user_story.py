"""
Modelo SQLAlchemy para UserStory
"""
from __future__ import annotations

from typing import Any
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

VALID_PRIORITIES = {"low", "medium", "high", "critical"}


class UserStory(Base):
    __tablename__ = "user_stories"

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    goal = Column(String(500), nullable=False)
    reason = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=True)
    priority = Column(String(50), nullable=False, default="medium")
    story_points = Column(Integer, nullable=False, default=5)
    effort_hours = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relación con Task (se activará cuando Task esté actualizado)
    tasks = relationship("Task", back_populates="user_story", cascade="all, delete-orphan")

    def __init__(
        self,
        project: str,
        role: str,
        goal: str,
        reason: str,
        description: str | None = None,
        priority: str = "medium",
        story_points: int = 5,
        effort_hours: float = 0.0,
    ) -> None:
        self.project = project
        self.role = role
        self.goal = goal
        self.reason = reason
        self.description = description
        self.priority = priority
        self.story_points = story_points
        self.effort_hours = effort_hours
        self._validate()

    def _validate(self) -> None:
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"priority must be one of {sorted(VALID_PRIORITIES)}, got '{self.priority}'"
            )
        if self.story_points < 1 or self.story_points > 8:
            raise ValueError("story_points must be between 1 and 8")
        if self.effort_hours < 0:
            raise ValueError("effort_hours must be a non-negative number")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "project": self.project,
            "role": self.role,
            "goal": self.goal,
            "reason": self.reason,
            "description": self.description,
            "priority": self.priority,
            "story_points": self.story_points,
            "effort_hours": self.effort_hours,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserStory":
        return cls(
            project=data["project"],
            role=data["role"],
            goal=data["goal"],
            reason=data["reason"],
            description=data.get("description"),
            priority=data.get("priority", "medium"),
            story_points=int(data.get("story_points", 5)),
            effort_hours=float(data.get("effort_hours", 0.0)),
        )
