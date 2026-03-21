# LLM in a box (LIAB)
[![Python 3.9](https://img.shields.io/badge/python-3.10+-gree.svg)](https://www.python.org/downloads/release/python-390/)

A fully functional terminal-based Large Language Model (LLM) chat application built in Python. Run and manage LLMs locally on your machine with ease. Built with [Ollama](https://ollama.com/) for model hosting, [Docker](https://www.docker.com/) for containerization, [Postgres](https://www.postgresql.org/) for data storage, [SQLAlchemy](https://www.sqlalchemy.org/) as its primary ORM, and [Textual](https://textual.textualize.io/) for a rich terminal UI.

<p align="center">
  <img src="https://i.imgur.com/lr3cFX3.gif" alt="Alt Text" width="800">
</p>


## Installation
1. Clone the repository
```bash
git clone https://github.com/henningraberg/llm-in-a-box.git
```

2. Navigate to the cloned directory
```bash
cd llm-in-a-box
```

3. Make sure you have the following installed before running the install
* [Poetry](https://python-poetry.org/docs/#installation)
* [Docker](https://docs.docker.com/get-started/) (make sure you allocated high memory limit, some models requires a lot when processing)
* [Postgresql](https://www.postgresql.org/download/)

4. Set up docker containers, python environment and packages (⚠️ make sure you have Docker running before install)
```bash
make install
```

5. Download the models you want to use (browse available models here &#8594; https://ollama.com/library)
```bash
poetry run liab download-model --model <model_name>
```
Example
```bash
poetry run liab download-model --model gemma3:1b
```

6. Run GUI application
```bash
poetry run liab gui
```

## Makefile Commands
| Command | Description |
|---|---|
| `make install` | Install dependencies, start services, and build the database |
| `make run-services` | Start Docker containers |
| `make stop-services` | Stop Docker containers |
| `make clean-services` | Stop Docker containers and remove volumes |
| `make clean` | Alias for `clean-services` |
| `make rebuild-db` | Nuke and rebuild the database |
| `make test` | Run tests |
| `make lint` | Run linting and format checks |
| `make coverage` | Run tests with coverage report |

## Usage
```
Usage: liab [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add-chat           Add a chat.
  build-db           Create the database.
  chat               List a chats message history.
  download-model     Download LLM model.
  gui                Run the LIAB GUI application.
  list-chat-history  List a chats message history.
  list-chats         List all chats.
  list-models        List all downloaded models.
  nuke-db            Clean the database.
  remove-chat        Remove a chat.
  remove-model       Remove model.
  show-model         Get model information.
```

## SQL Query Logging
You can optionally enable SQL query logging to see what queries SQLAlchemy executes. Set the `SQL_LOG` environment variable to enable it:
```bash
SQL_LOG=1 poetry run liab gui
```
Queries are written to `logs/sql.log`. To follow the log in real time, run in a separate terminal:
```bash
tail -f logs/sql.log
```