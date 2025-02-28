# LLM in a box (LIAB)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff) 
[![Python 3.9](https://img.shields.io/badge/python-3.9-gree.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-gree.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-gree.svg)](https://www.python.org/downloads/release/python-3110/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-gree.svg)](https://www.python.org/downloads/release/python-3120/)
[![Python 3.13](https://img.shields.io/badge/python-3.13-gree.svg)](https://www.python.org/downloads/release/python-3130/)

A terminal project exploring the possibilities of managing and running LLMs locally on your machine. Built on  [Ollama](https://ollama.com/), [Docker](https://www.docker.com/), [Postgres](https://www.postgresql.org/), [SQLAlchemy](https://www.sqlalchemy.org/) and [Textual](https://textual.textualize.io/).

<p align="center">
  <img src="https://s4.ezgif.com/tmp/ezgif-458da3d881d86f.gif" alt="Alt Text", width="800">
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

3. Set up docker containers, python environment and packages
```bash
make install
```

4. Download the models you want to use (brows available models here &#8594; https://ollama.com/library)
```bash
python liab.py install <model_name>
```

5. Run GUI application
```bash
python liab.py gui
```

## Usage
```
Usage: liab.py [OPTIONS] COMMAND [ARGS]...

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