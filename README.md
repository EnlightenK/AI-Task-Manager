# AI Sentinel (Design Office Task Manager)

AI Sentinel is a privacy-first, local automation tool designed for Civil Engineering Design Firms. It eliminates manual data entry by monitoring an inbox folder for incoming emails and design instructions, using a local AI agent to analyze and route tasks to the appropriate engineering discipline.

## Features

-   **Automated Ingestion:** Watches the `inbox/` folder for `.txt`, `.msg`, and `.eml` files.
-   **AI Analysis:** Uses local LLMs (via Ollama) to extract summaries, deadlines, and assign projects/engineers.
-   **Dashboard:** A Streamlit-based UI for triaging pending tasks, managing active work, and viewing history.
-   **Privacy First:** All processing happens locally; no data is sent to the cloud.

## Prerequisites

*   **Python:** 3.12 or higher
*   **uv:** An extremely fast Python package installer and resolver. [Install uv](https://github.com/astral-sh/uv).
*   **Ollama:** For running the local LLM. [Install Ollama](https://ollama.com/).
    *   **CRITICAL:** You must have the `llama3.2` model installed. Run:
        ```bash
        ollama pull llama3.2
        ```

## Installation

This project uses `uv` for modern Python dependency management.

1.  **Clone the repository** (if applicable) or navigate to the project root.

2.  **Sync dependencies:**
    This command creates the virtual environment and installs all locked dependencies.
    ```bash
    uv sync
    ```

3.  **Activate the virtual environment (Optional):**
    `uv run` can execute commands in the environment without explicit activation, but if you prefer:
    *   **Windows:** `.venv\Scripts\activate`
    *   **macOS/Linux:** `source .venv/bin/activate`

## Development & Testing

We use `pytest` for testing. Since the project is in active development, running tests is the best way to verify the system is set up correctly.

### Run All Tests
```bash
uv run pytest
```

### Verify Core Components
To manually verify the AI Agent (requires Ollama running):
```bash
uv run python -c "from backend.services.ai_service import TaskAnalysisAgent; agent = TaskAnalysisAgent(); print(f'Agent initialized with {agent.model_name} successfully!')"
```

## Usage

### 1. Start the Backend Service
This service watches the `inbox/` folder and processes new files.
*(Note: Ensure `inbox/` directory exists)*

```bash
uv run python backend/main.py
```

### 2. Start the Frontend Dashboard
Launch the Streamlit UI to view and manage tasks.

```bash
uv run streamlit run frontend/app.py
```

### 3. Workflow
1.  **Ingest:** Drop an email (`.msg`, `.eml`) or text file (`.txt`) into the `inbox/` directory.
2.  **Triage:** Go to the **Inbox** tab in the dashboard. Review the AI's analysis, edit if necessary, and click **Approve**.
3.  **Execute:** The task moves to the **Active Tasks** tab. Work on the task, edit details if needed, and check the box when complete.
4.  **Archive:** Completed tasks are moved to the **History** tab.

## Configuration

*   **Projects:** Define active projects in `data/projects.json`.
*   **Team:** Define team members and their roles in `data/team.json`.
*   **Environment Variables:**
    *   `OLLAMA_BASE_URL`: Defaults to `http://localhost:11434/v1`. Set this if your Ollama instance is on a different port/host.

## Directory Structure

```text
/AI_Sentinel
├── backend/            # Python backend
│   ├── core/           # Core domain models and logic
│   ├── services/       # AI and Database services
│   └── utils/          # Config and file parsers
├── frontend/           # Streamlit frontend application
├── data/               # Configuration and SQLite database
├── inbox/              # Drop incoming files here
├── processed/          # Processed files are moved here
├── tests/              # Unit and integration tests
├── conductor/          # Project management and setup docs
└── pyproject.toml      # Project dependencies and config
```
