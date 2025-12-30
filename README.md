# AI Sentinel (Design Office Task Manager)

AI Sentinel is a privacy-first, local automation tool designed for Civil Engineering Design Firms. It eliminates manual data entry by monitoring an inbox folder for incoming emails and design instructions, using a local AI agent to analyze and route tasks to the appropriate engineering discipline.

## Features

-   **Automated Ingestion:** Watches the `inbox/` folder for `.txt`, `.msg`, and `.eml` files.
-   **Robust Processing:** Uses a staging pattern to prevent race conditions during file ingestion.
-   **AI Analysis:** Uses local LLMs (via Ollama Cloud or local instance) to extract summaries, deadlines, and assign projects/engineers.
-   **Dashboard:** A Streamlit-based UI for triaging pending tasks, managing active work with sortable tables, and viewing history.
-   **Settings Management:** In-app management of Projects and Team Members via the Settings tab.
-   **Privacy First:** Optimized for local or private cloud LLM deployments.

## Prerequisites

*   **Python:** 3.12 or higher
*   **uv:** An extremely fast Python package installer and resolver. [Install uv](https://github.com/astral-sh/uv).
*   **Ollama:** For running the LLM. [Install Ollama](https://ollama.com/).
    *   **Default Model:** The system is configured for `gpt-oss:120b`. Ensure you have access to this model or update the configuration.

## Installation

This project uses `uv` for modern Python dependency management.

1.  **Clone the repository** (if applicable) or navigate to the project root.

2.  **Sync dependencies:**
    This command creates the virtual environment and installs all locked dependencies.
    ```bash
    uv sync
    ```

3.  **Setup Environment Variables:**
    Copy the example environment file and fill in your details (especially if using Ollama Cloud).
    ```bash
    cp .env.example .env
    ```

## Usage

### 1. Start the Dashboard
Launch the Streamlit UI to manage the entire system.

```bash
uv run streamlit run frontend/app.py
```

### 2. Initialize the Watcher
Once the dashboard is open:
1.  Locate the **System Status** section in the sidebar.
2.  Click **"Start Watcher"**. This starts the background service that monitors the `inbox/` folder.

### 3. Workflow
1.  **Ingest:** Drop an email (`.msg`, `.eml`) or text file (`.txt`) into the `inbox/` directory.
2.  **Triage:** Go to the **Inbox** tab. Review the AI's analysis, edit if necessary, and click **Approve** (or **Reject** to delete).
3.  **Execute:** The task moves to the **Active Tasks** tab. Select a task from the table to edit details or mark it as complete.
4.  **Archive:** Completed tasks are moved to the **History** tab where they can be viewed or restored.
5.  **Configure:** Use the **Settings** tab to add new projects or update team member assignments.

## Development & Testing

We use `pytest` for testing.

### Run All Tests
```bash
uv run pytest
```

## Configuration (.env)

*   **OLLAMA_MODEL:** Defaults to `gpt-oss:120b`.
*   **OLLAMA_BASE_URL:** Defaults to `https://ollama.com/v1/`.
*   **OLLAMA_API_KEY:** Your API key for the Ollama service.

## Directory Structure

```text
/AI_Sentinel
├── backend/            # Python backend
│   ├── core/           # Orchestration and Watcher logic
│   ├── services/       # AI Agent (PydanticAI) and Database services
│   └── utils/          # Config, Parsers, and DB initialization
├── frontend/           # Streamlit frontend
│   ├── components/     # UI Views (Inbox, Active, History, Settings)
│   └── services/       # API Client and Watcher Manager
├── data/               # SQLite database and JSON config files
├── inbox/              # Drop incoming files here
├── staging/            # Temporary folder for active processing
├── processed/          # Successfully processed files
├── tests/              # Comprehensive test suite
└── pyproject.toml      # Project dependencies
```