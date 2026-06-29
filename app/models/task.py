"""
Modelo SQLAlchemy para Task
"""
from __future__ import annotations

from typing import Any
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

VALID_STATUSES = {"pending", "in_progress", "done", "in_review"}
VALID_PRIORITIES = {"low", "medium", "high", "blocking"}


class Task(Base):
    __tablename__ = "tasks"

    # Columnas
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    priority = Column(String(50), nullable=False)
    effort_hours = Column(Float, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    assigned_to = Column(String(255), nullable=False)
    category = Column(String(255), nullable=True)
    risk_analysis = Column(String(1000), nullable=True)
    risk_mitigation = Column(String(1000), nullable=True)
    user_story_id = Column(Integer, ForeignKey("user_stories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relación con UserStory
    user_story = relationship("UserStory", back_populates="tasks")

    def __init__(
        self,
        title: str,
        description: str,
        priority: str,
        effort_hours: float,
        status: str,
        assigned_to: str,
        category: str | None = None,
        risk_analysis: str | None = None,
        risk_mitigation: str | None = None,
        user_story_id: int | None = None,
    ) -> None:
        self.title = title
        self.description = description
        self.priority = priority
        self.effort_hours = effort_hours
        self.status = status
        self.assigned_to = assigned_to
        self.category = category
        self.risk_analysis = risk_analysis
        self.risk_mitigation = risk_mitigation
        self.user_story_id = user_story_id
        self._validate()

    def _validate(self) -> None:
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"status must be one of {sorted(VALID_STATUSES)}, got '{self.status}'"
            )
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(
                f"priority must be one of {sorted(VALID_PRIORITIES)}, got '{self.priority}'"
            )
        if self.effort_hours < 0:
            raise ValueError("effort_hours must be a non-negative number")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": self.effort_hours,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "category": self.category,
            "risk_analysis": self.risk_analysis,
            "risk_mitigation": self.risk_mitigation,
            "user_story_id": self.user_story_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            effort_hours=float(data["effort_hours"]),
            status=data.get("status", "pending"),
            assigned_to=data["assigned_to"],
            category=data.get("category"),
            risk_analysis=data.get("risk_analysis"),
            risk_mitigation=data.get("risk_mitigation"),
            user_story_id=data.get("user_story_id"),
        )
