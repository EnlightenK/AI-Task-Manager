# Technology Stack

## Core Technologies
- **Language:** Python 3.9+
- **Frontend UI:** Streamlit (v1.x)
- **AI Agent Framework:** PydanticAI
- **LLM Runtime:** Ollama Cloud (specifically gpt-oss:120b)

## Infrastructure & Libraries
- **File System Watcher:** Watchdog (for inbox monitoring)
- **Email Parser:** extract-msg (for .msg file support)
- **Logging & Tracing:** Logfire
- **Package Management:** uv
- **Data Persistence:** Local JSON files (data/projects.json, data/team.json) and SQLite (data/tasks.db)
