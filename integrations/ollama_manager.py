from misc.request_handler import RequestHandler


class OllamaManager:
    PORT = 11434
    URL = f'http://localhost:{PORT}/v1/'

    def __init__(self):
        self.request_handler = RequestHandler()
        pass

    def get_installed_models(self) -> list[str]:
        api_endpoint = self.URL + 'models'
        response = self.request_handler.get(url=api_endpoint)
        return response
