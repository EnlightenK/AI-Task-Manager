import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from backend.services.ai_service import TaskAnalysisAgent
from pydantic_ai.models.openai import OpenAIChatModel
from backend.core.models import TaskProposal

def test_task_analysis_agent_init():
    agent_service = TaskAnalysisAgent(model_name="gpt-oss:120b")
    assert agent_service.model_name == "gpt-oss:120b"
    assert isinstance(agent_service.agent.model, OpenAIChatModel)

def test_task_analysis_agent_default_model():
    agent_service = TaskAnalysisAgent()
    assert agent_service.model_name == "gpt-oss:120b"

@pytest.mark.asyncio
async def test_analyze_content_success():
    agent_service = TaskAnalysisAgent()
    
    # Mocking the agent.run method
    mock_result = MagicMock()
    mock_result.data = TaskProposal(
        title="Test Task",
        description="Test Description",
        deadline=datetime(2025, 12, 31),
        assigned_to="Alice",
        project_id="SB-01",
        confidence=0.9
    )
    
    agent_service.agent.run = AsyncMock(return_value=mock_result)
    
    result = await agent_service.analyze_content("Analyze this")
    assert result.title == "Test Task"
    assert result.assigned_to == "Alice"
    agent_service.agent.run.assert_called_once_with("Analyze this")

@pytest.mark.asyncio
async def test_analyze_content_failure():
    agent_service = TaskAnalysisAgent()
    agent_service.agent.run = AsyncMock(side_effect=Exception("AI Error"))
    
    with pytest.raises(Exception, match="AI Error"):
        await agent_service.analyze_content("Analyze this")
