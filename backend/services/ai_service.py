import logging
import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from backend.core.models import TaskProposal
from backend.utils.config import load_projects, load_team

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class TaskAnalysisAgent:
    def __init__(self, model_name: Optional[str] = None, base_url: Optional[str] = None, api_key: Optional[str] = None):
        # Priority: constructor arg > environment variable > default value
        self.model_name = model_name or os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "https://ollama.com/v1/")
        self.api_key = api_key or os.getenv("OLLAMA_API_KEY")
        
        # Configure the Ollama model using OpenAIChatModel and OllamaProvider
        self.model = OpenAIChatModel(
            model_name=self.model_name,
            provider=OllamaProvider(
                base_url=self.base_url,
                api_key=self.api_key
            )
        )
        self.agent = Agent(
            self.model,
            output_type=TaskProposal,
            system_prompt="You are an expert Civil Engineering Project Manager AI (The Sentinel).",
            retries=3
        )
        self._setup_agent()

    def _setup_agent(self):
        @self.agent.system_prompt
        def get_dynamic_system_prompt(ctx: RunContext) -> str:
            projects = load_projects()
            team = load_team()
            
            projects_str = "\n".join([f"- {p['id']}: {p['name']} ({p['context']})" for p in projects])
            team_str = "\n".join([f"- {t['name']} ({t['role']}): {', '.join(t['duties'])}. Projects: {', '.join(t['projects'])} " for t in team])
            
            return f"""
            Your job is to analyze incoming correspondence and route it to the correct engineer.

            **Active Projects:**
            {projects_str}

            **Engineering Team:**
            {team_str}

            **Instructions:**
            Analyze the content and extract the following information.
            
            1. **title**: A 10-20 word action-oriented summary.
            2. **description**: detailed description.
            3. **deadline**: The deadline if stated, otherwise null.
            4. **project_id**: The matching Project ID from the list above.
            5. **assigned_to**: The name of the team member whose role and projects match the task.
            6. **confidence**: A score between 0.0 and 1.0.

            **CRITICAL:** 
            - Use the `final_result` tool to return your answer.
            - Do NOT call any other tools.
            - Do NOT output multiple JSON objects.
            """

    async def analyze_content(self, content: str) -> TaskProposal:
        try:
            result = await self.agent.run(content)
            return result.output
        except Exception as e:
            logger.error(f"AI Analysis failed: {e}")
            raise e

# Singleton instance
_agent_instance: Optional[TaskAnalysisAgent] = None

async def analyze_content(content: str) -> TaskProposal:
    """
    Standalone function to analyze content using a singleton TaskAnalysisAgent.
    This maintains backward compatibility with consumers expecting a function.
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TaskAnalysisAgent()
    
    return await _agent_instance.analyze_content(content)