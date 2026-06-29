from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str
    effort_hours: Optional[float] = None
    status: str
    assigned_to: str

    category: Optional[str] = None
    risk_analysis: Optional[str] = None
    risk_mitigation: Optional[str] = None
