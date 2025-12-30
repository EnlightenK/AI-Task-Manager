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
    title: str = Field(default="Untitled Task", description="A concise summary of the task")
    description: str = Field(default="", description="Detailed instructions")
    deadline: Optional[datetime] = Field(default=None, description="The deadline extracted from the content, or None")
    assigned_to: Optional[str] = Field(default=None, description="The name of the assigned team member")
    project_id: Optional[str] = Field(default=None, description="The matching Project ID")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")