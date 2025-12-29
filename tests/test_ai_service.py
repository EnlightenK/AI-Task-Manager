import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime
from backend.services.ai_service import TaskAnalysisAgent
from pydantic_ai.models.openai import OpenAIChatModel
from backend.core.models import TaskProposal

def test_task_analysis_agent_init():
    agent_service = TaskAnalysisAgent(model_name="test-model", base_url="http://test:11434/v1")
    assert agent_service.model_name == "test-model"
    assert agent_service.base_url == "http://test:11434/v1"
    assert isinstance(agent_service.agent.model, OpenAIChatModel)

def test_task_analysis_agent_env_vars():
    with patch.dict(os.environ, {
        "OLLAMA_MODEL": "env-model",
        "OLLAMA_BASE_URL": "http://env:11434/v1",
        "OLLAMA_API_KEY": "test-key"
    }):
        agent_service = TaskAnalysisAgent()
        assert agent_service.model_name == "env-model"
        assert agent_service.base_url == "http://env:11434/v1"
        assert agent_service.api_key == "test-key"

def test_task_analysis_agent_default():
    # Clear env vars to test defaults
    with patch.dict(os.environ, {}, clear=True):
        agent_service = TaskAnalysisAgent()
        assert agent_service.model_name == "gpt-oss:120b"
        assert agent_service.base_url == "http://localhost:11434/v1"

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
