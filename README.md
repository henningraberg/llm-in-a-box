# LLM in a Box (LIAB)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A terminal-based chat application for running Large Language Models locally. Manage conversations, switch between models, and stream responses — all from your terminal.

<p align="center">
  <img src="https://i.imgur.com/lr3cFX3.gif" alt="LIAB demo" width="800">
</p>

## Features

- **Rich terminal UI** — split-pane chat interface with sidebar, model selector, and real-time streaming
- **Full CLI** — manage chats, models, and the database entirely from the command line
- **Multi-model support** — download any model from the [Ollama library](https://ollama.com/library) and switch between them per chat
- **Persistent chat history** — conversations are stored in PostgreSQL and survive restarts
- **Auto-generated chat names** — the LLM names your conversations based on context
- **Abort in-progress responses** — cancel a generation mid-stream from the GUI
- **Dockerized services** — Ollama and PostgreSQL run in containers, managed via Docker Compose

## Tech Stack

| Component | Technology |
|---|---|
| LLM Runtime | [Ollama](https://ollama.com/) |
| Terminal UI | [Textual](https://textual.textualize.io/) |
| CLI | [Click](https://click.palletsprojects.com/) |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Database | [PostgreSQL](https://www.postgresql.org/) |
| Containerization | [Docker](https://www.docker.com/) |
| Package Manager | [Poetry](https://python-poetry.org/) |

## Project Structure

```
llm-in-a-box/
├── cli/              # CLI commands (Click)
├── gui/              # Terminal UI (Textual)
│   ├── views/        # Screen layouts
│   ├── widgets/      # UI components
│   └── static/       # Stylesheets
├── models/           # SQLAlchemy ORM models
├── database/         # DB init & cleanup
├── integrations/     # Ollama client wrapper
└── tests/            # Pytest test suite
```

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-started/) — allocate enough memory for the models you plan to run

## Getting Started

**1. Clone and enter the repository**
```bash
git clone https://github.com/henningraberg/llm-in-a-box.git
cd llm-in-a-box
```

**2. Install dependencies and start services**

Make sure Docker is running, then:
```bash
make install
```
This installs Python packages, starts the Ollama and PostgreSQL containers, and initializes the database.

**3. Download a model**

Browse available models at [ollama.com/library](https://ollama.com/library), then:
```bash
poetry run liab download-model --model <model_name>
```
For example:
```bash
poetry run liab download-model --model gemma3:1b
```

**4. Launch the GUI**
```bash
poetry run liab gui
```

## CLI Reference

```
Usage: liab [OPTIONS] COMMAND [ARGS]...
```

### Chat commands
| Command | Description |
|---|---|
| `gui` | Launch the terminal UI |
| `chat --chat-id <id>` | Interactive chat session in the terminal |
| `add-chat --name <n> --model <m>` | Create a new chat |
| `remove-chat --chat-id <id>` | Delete a chat and its messages |
| `list-chats` | List all chats |
| `list-chat-history --chat-id <id>` | Show message history for a chat |

### Model commands
| Command | Description |
|---|---|
| `download-model --model <name>` | Download a model from Ollama |
| `remove-model --model <name>` | Delete a downloaded model |
| `list-models` | List all downloaded models |
| `show-model --model <name>` | Show model details |

### Database commands
| Command | Description |
|---|---|
| `build-db` | Initialize the database schema |
| `nuke-db` | Drop all tables |

## Makefile Commands

| Command | Description |
|---|---|
| `make install` | Install packages, start services, and build the database |
| `make run-services` | Start Docker containers |
| `make stop-services` | Stop Docker containers |
| `make clean-services` | Stop containers and remove volumes |
| `make clean` | Alias for `clean-services` |
| `make rebuild-db` | Drop and recreate the database |
| `make test` | Run the test suite |
| `make lint` | Run linting and format checks (Ruff) |
| `make coverage` | Run tests with coverage report |

## SQL Query Logging

Enable SQLAlchemy query logging for debugging:
```bash
SQL_DEBUG=1 poetry run liab gui
```
Queries are written to `logs/sql.log`. To follow in real time:
```bash
tail -f logs/sql.log
```

## License

[MIT](LICENSE) — Copyright (c) 2025 Henning Råberg
