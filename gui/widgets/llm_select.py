from textual.widgets import Select

from integrations.ollama_manager import OllamaManager


class LLMSelect(Select):
    def __init__(self, *args, **kwargs):
        downloaded_models = OllamaManager().get_downloaded_models()
        downloaded_models = (
            [(model.model, model.model) for model in downloaded_models.models] if downloaded_models else []
        )
        super().__init__(downloaded_models, *args, **kwargs)
