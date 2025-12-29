# Plan: Core AI Agent Logic

## Phase 1: Domain Models [checkpoint: c2e95d7]
- [x] Task: Create Pydantic models for `Project` and `TeamMember` in `backend/core/models.py`. (3f8b4ee)
- [x] Task: Create Pydantic model for `TaskProposal` in `backend/core/models.py` with validation fields. (3f8b4ee)
- [x] Task: Conductor - User Manual Verification 'Domain Models' (Protocol in workflow.md) (c2e95d7)

## Phase 2: File Parsers [checkpoint: 5a2e8a6]
- [x] Task: Create abstract base class `FileParser` in `backend/utils/parsers.py`. (3269426)
- [x] Task: Implement `TextFileParser` for simple `.txt` files. (3269426)
- [x] Task: Implement `EmailFileParser` supporting both `.eml` and `.msg` (using `extract-msg`). (3269426)
- [x] Task: Conductor - User Manual Verification 'File Parsers' (Protocol in workflow.md) (5a2e8a6)

## Phase 3: AI Agent Implementation
- [ ] Task: Configure PydanticAI client for Ollama in `backend/services/ai_service.py`.
- [ ] Task: Implement `TaskAnalysisAgent` class.
    -   Define the system prompt to include current time, list of projects, and team roster.
    -   Define the `analyze_content` method that returns a `TaskProposal`.
- [ ] Task: Conductor - User Manual Verification 'AI Agent Implementation' (Protocol in workflow.md)
