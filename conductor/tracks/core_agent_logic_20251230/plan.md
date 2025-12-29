# Plan: Core AI Agent Logic

## Phase 1: Domain Models
- [ ] Task: Create Pydantic models for Project and TeamMember in ackend/core/models.py.
- [ ] Task: Create Pydantic model for TaskProposal in ackend/core/models.py with validation fields.
- [ ] Task: Conductor - User Manual Verification 'Domain Models' (Protocol in workflow.md)

## Phase 2: File Parsers
- [ ] Task: Create abstract base class FileParser in ackend/utils/parsers.py.
- [ ] Task: Implement TextFileParser for simple .txt files.
- [ ] Task: Implement EmailFileParser supporting both .eml and .msg (using extract-msg).
- [ ] Task: Conductor - User Manual Verification 'File Parsers' (Protocol in workflow.md)

## Phase 3: AI Agent Implementation
- [ ] Task: Configure PydanticAI client for Ollama in ackend/services/ai_service.py.
- [ ] Task: Implement TaskAnalysisAgent class.
    -   Define the system prompt to include current time, list of projects, and team roster.
    -   Define the nalyze_content method that returns a TaskProposal.
- [ ] Task: Conductor - User Manual Verification 'AI Agent Implementation' (Protocol in workflow.md)
