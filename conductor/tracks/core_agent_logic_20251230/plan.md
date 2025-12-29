# Plan: Core AI Agent Logic

## Phase 1: Domain Models
- [x] Task: Create Pydantic models for `Project` and `TeamMember` in `backend/core/models.py`. (3f8b4ee)
- [x] Task: Create Pydantic model for `TaskProposal` in `backend/core/models.py` with validation fields. (3f8b4ee)
- [ ] Task: Conductor - User Manual Verification 'Domain Models' (Protocol in workflow.md)

## Phase 2: File Parsers
- [ ] Task: Create abstract base class `FileParser` in `backend/utils/parsers.py`.
- [ ] Task: Implement `TextFileParser` for simple `.txt` files.
- [ ] Task: Implement `EmailFileParser` supporting both `.eml` and `.msg` (using `extract-msg`).
- [ ] Task: Conductor - User Manual Verification 'File Parsers' (Protocol in workflow.md)

## Phase 3: AI Agent Implementation
- [ ] Task: Configure PydanticAI client for Ollama in `backend/services/ai_service.py`.
- [ ] Task: Implement `TaskAnalysisAgent` class.
    -   Define the system prompt to include current time, list of projects, and team roster.
    -   Define the `analyze_content` method that returns a `TaskProposal`.
- [ ] Task: Conductor - User Manual Verification 'AI Agent Implementation' (Protocol in workflow.md)
