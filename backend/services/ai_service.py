import logging
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from backend.utils.config import load_projects, load_team

# Setup logging
logger = logging.getLogger(__name__)

# Ensure OLLAMA_BASE_URL is set for local usage if not present
if "OLLAMA_BASE_URL" not in os.environ:
    os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434/v1"

class TaskAnalysis(BaseModel):
    summary: str = Field(description="A 10-20 word action-oriented summary of the task.")
    deadline: str = Field(description="The deadline in YYYY-MM-DD format, or 'None' if not specified.")
    project_id: str = Field(description="The matching Project ID (e.g., 'SB-01').")
    assignee: str = Field(description="The name of the best-suited Design Engineer.")
    reasoning: str = Field(description="Explanation for why this discipline/project was chosen.")

# Initialize Agent with local Ollama model using the string identifier
# This uses the 'ollama' provider support in pydantic-ai
agent = Agent(
    'ollama:llama3',
    output_type=TaskAnalysis
)

@agent.system_prompt
def get_dynamic_system_prompt(ctx: RunContext) -> str:
    """
    Generates the system prompt dynamically based on current projects and team.
    """
    projects = load_projects()
    team = load_team()
    
    projects_str = "\n".join([f"- {p['id']}: {p['name']} ({p['context']})" for p in projects])
    team_str = "\n".join([f"- {t['name']} ({t['role']}): {', '.join(t['duties'])}. Projects: {', '.join(t['projects'])}" for t in team])
    
    return f"""
    You are an expert Civil Engineering Project Manager AI (The Sentinel).
    Your job is to analyze incoming correspondence and route it to the correct engineer.

    **Active Projects:**
    {projects_str}

    **Engineering Team:**
    {team_str}

    **Rules:**
    1. EXTRACT a 10-20 word action-oriented summary.
    2. EXTRACT the deadline in YYYY-MM-DD format. If none, use "None".
    3. ASSIGN to the most appropriate team member based on their Role, Duties, and assigned Projects.
       - CRITICAL: You MUST ONLY assign tasks to a team member if the Project ID matches one of their allowed 'projects'.
    4. IDENTIFY the Project ID based on the content context.
    5. PROVIDE reasoning for your decision.
    """

async def analyze_content(content: str) -> TaskAnalysis:
    """
    Analyzes the text content using the AI agent to extract task details.
    """
    try:
        # Run the agent
        result = await agent.run(content)
        return result.data
    except Exception as e:
        logger.error(f"AI Analysis failed: {e}")
        # Return fallback object indicating failure
        return TaskAnalysis(
            summary="Manual Review Needed - AI Analysis Failed",
            deadline="None",
            project_id="UNKNOWN",
            assignee="Unassigned",
            reasoning=f"AI Error: {str(e)}"
        )