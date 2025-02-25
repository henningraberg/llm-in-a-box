from textual.widgets import Select

from integrations.ollama_manager import OllamaManager


class LLMSelector(Select):
    DEFAULT_CSS = """
        LLMSelector {
        }
    """

    def __init__(self, *args, **kwargs):
        installed_models = OllamaManager().get_installed_models()
        model_name_list = []

        for model in installed_models.models:
            model_name_list.append((model.model, model.model))

        super().__init__(model_name_list, *args, **kwargs)
