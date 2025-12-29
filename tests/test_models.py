import pytest
from pydantic import ValidationError
from datetime import datetime
from backend.core.models import Project, TeamMember, TaskProposal

def test_project_model_valid():
    data = {
        "id": "SB-01",
        "name": "Suspension Bridge Feasibility",
        "context": "Preliminary design phase."
    }
    project = Project(**data)
    assert project.id == "SB-01"

def test_team_member_model_valid():
    data = {
        "name": "Alice",
        "role": "Senior Structural Engineer",
        "duties": ["Finite Element Analysis"],
        "projects": ["SB-01"]
    }
    member = TeamMember(**data)
    assert member.name == "Alice"

def test_task_proposal_model_valid():
    data = {
        "title": "Analyze cable anchorage",
        "description": "Evaluate the stress on the main anchorage points.",
        "deadline": datetime(2025, 12, 31, 17, 0),
        "assigned_to": "Alice",
        "project_id": "SB-01",
        "confidence": 0.95
    }
    proposal = TaskProposal(**data)
    assert proposal.title == "Analyze cable anchorage"
    assert proposal.confidence == 0.95

def test_task_proposal_model_invalid():
    with pytest.raises(ValidationError):
        TaskProposal(title="Incomplete")