"""
Schemas Pydantic para validación y serialización de datos
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ===== PROMPT SCHEMA =====

class GeneratePromptSchema(BaseModel):
    """Schema para generar con IA"""
    prompt: str = Field(..., min_length=10, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Como usuario quiero poder realizar compras online para adquirir productos"
            }
        }


# ===== TASK SCHEMAS =====

class TaskCreateSchema(BaseModel):
    """Schema para crear una tarea"""
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=1000)
    priority: str = Field(..., pattern="^(low|medium|high|blocking)$")
    effort_hours: float = Field(..., ge=0)
    status: str = Field(default="pending", pattern="^(pending|in_progress|done|in_review)$")
    assigned_to: str = Field(..., min_length=1, max_length=255)
    category: Optional[str] = Field(None, max_length=255)
    risk_analysis: Optional[str] = Field(None, max_length=1000)
    risk_mitigation: Optional[str] = Field(None, max_length=1000)
    user_story_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Implementar login",
                "description": "Crear endpoint de autenticación",
                "priority": "high",
                "effort_hours": 3.5,
                "status": "pending",
                "assigned_to": "María",
                "category": "Backend",
                "user_story_id": 1
            }
        }


class TaskResponseSchema(BaseModel):
    """Schema para respuesta de tarea"""
    id: int
    title: str
    description: str
    priority: str
    effort_hours: float
    status: str
    assigned_to: str
    category: Optional[str] = None
    risk_analysis: Optional[str] = None
    risk_mitigation: Optional[str] = None
    user_story_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== USER STORY SCHEMAS =====

class UserStoryCreateSchema(BaseModel):
    """Schema para crear una historia de usuario"""
    project: str = Field(..., min_length=1, max_length=255)
    role: str = Field(..., min_length=1, max_length=255)
    goal: str = Field(..., min_length=1, max_length=500)
    reason: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")
    story_points: int = Field(default=5, ge=1, le=8)
    effort_hours: float = Field(default=0.0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "project": "E-commerce",
                "role": "usuario",
                "goal": "realizar compras online",
                "reason": "aumentar ventas",
                "description": "Sistema completo de carrito de compras",
                "priority": "high",
                "story_points": 8,
                "effort_hours": 40.0
            }
        }


class UserStoryResponseSchema(BaseModel):
    """Schema para respuesta de historia de usuario"""
    id: int
    project: str
    role: str
    goal: str
    reason: str
    description: Optional[str] = None
    priority: str
    story_points: int
    effort_hours: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
