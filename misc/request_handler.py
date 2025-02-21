import requests


class RequestHandler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def get(self, url, params=None, **kwargs):
        return self._request('GET', url, params=params, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self._request('POST', url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._request('PUT', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json() if response.content else None  # Attempt to parse JSON, return None if empty
        except requests.exceptions.RequestException as e:
            print(f'Request error: {e}')
            return None
        except ValueError as e:
            print(f'JSON decode error: {e}')
            return None
