from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Project(BaseModel):
    id: str
    name: str
    context: str

class TeamMember(BaseModel):
    name: str
    role: str
    duties: List[str]
    projects: List[str]

class TaskProposal(BaseModel):
    title: str
    description: str
    deadline: datetime
    assigned_to: str
    project_id: str
    confidence: float = Field(ge=0.0, le=1.0)