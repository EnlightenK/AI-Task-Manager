import logging
import os
from typing import List
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from backend.core.models import TaskProposal
from backend.utils.config import load_projects, load_team

# Setup logging
logger = logging.getLogger(__name__)

class TaskAnalysisAgent:
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434/v1"):
        self.model_name = model_name
        self.base_url = base_url
        # Configure the Ollama model using OpenAIChatModel and OllamaProvider
        self.model = OpenAIChatModel(
            model_name=self.model_name,
            provider=OllamaProvider(base_url=self.base_url)
        )
        self.agent = Agent(
            self.model,
            output_type=TaskProposal,
            system_prompt="You are an expert Civil Engineering Project Manager AI (The Sentinel)."
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

            **Rules:**
            1. EXTRACT a 10-20 word action-oriented summary for the title.
            2. EXTRACT the detailed description.
            3. EXTRACT the deadline. If none, infer a reasonable one (e.g., 7 days from now) and state it.
            4. ASSIGN to the most appropriate team member based on their Role, Duties, and assigned Projects.
               - CRITICAL: You MUST ONLY assign tasks to a team member if the Project ID matches one of their allowed 'projects'.
            5. IDENTIFY the Project ID based on the content context.
            6. PROVIDE a confidence score between 0.0 and 1.0.
            """

    async def analyze_content(self, content: str) -> TaskProposal:
        try:
            result = await self.agent.run(content)
            return result.data
        except Exception as e:
            logger.error(f"AI Analysis failed: {e}")
            raise e
