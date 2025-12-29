# Specification: Core AI Agent Logic

## Context
AI Sentinel's core value proposition is the automated conversion of unstructured inbox files (emails, notes) into structured, actionable tasks. This track focuses on implementing the backend logic to parse files and use a local LLM (via PydanticAI and Ollama) to generate these structured proposals.

## Goals
1.  **Data Modeling:** Define strict Pydantic models for the system's core entities (Tasks, Projects, Team Members).
2.  **File Parsing:** Robustly extract text content from supported file formats (`.txt`, `.eml`, `.msg`).
3.  **AI Orchestration:** Implement an AI Agent that takes text input and project context to infer task details with high accuracy.

## Technical Requirements
-   **Framework:** PydanticAI for agent definition and structured output validation.
-   **LLM:** Ollama Cloud running `gpt-oss:120b`.
-   **Parsers:** `extract-msg` for Outlook files; Python standard library for text and MIME emails.

## Data Structures

### TaskProposal
-   **Title:** Concise summary of the task.
-   **Description:** Detailed instructions extracted from the source.
-   **Deadline:** `datetime` (inferred).
-   **Assigned_To:** `TeamMember` ID (inferred based on discipline).
-   **Project_ID:** `Project` ID (matched against active projects).
-   **Confidence:** Float (0.0 - 1.0) indicating AI certainty.

## Architecture
-   **FileParserStrategy:** A pattern to handle different file types uniformly.
-   **TaskAgent:** A class encapsulating the PydanticAI `Agent`, configured with a system prompt that receives the list of active projects and team members as context.