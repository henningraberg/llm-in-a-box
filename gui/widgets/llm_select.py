from textual.widgets import Select

from integrations.ollama_manager import OllamaManager


class LLMSelect(Select):
    def __init__(self, *args, **kwargs):
        installed_models = OllamaManager().get_installed_models()
        installed_models = [(model.model, model.model) for model in installed_models.models] if installed_models else []
        super().__init__(installed_models, *args, **kwargs)
