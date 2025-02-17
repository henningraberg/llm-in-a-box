# LLM in a box (LIAB)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

I needed an offline LLM for a long flight to help me on some projects and to get a better understanding of LLMs, so I created this project to simply manage and set up locally hosted LLMs.

# Tech used
* `Ollama` to host models
* `openai` to communicate with Ollama

# List of models to use
* https://ollama.com/library

## Installation
The installation needs internet access, so do this before you go offline. You can set it up either locally on your machine or in a docker container if you don't want the hassle.

### Docker
1. 

### Locally 
1. Create a virtual python environment (optional) - `python -m venv venv`
2. Activate the virtual environment (optional) - `source venv/bin/activate`
3. Install the requirements - `pip install -r requirements.txt`
4. Download your model of choice - `openai models download <model_name>`

(`source venv/bin/deactivate` to deactivate the virtual python environment)

