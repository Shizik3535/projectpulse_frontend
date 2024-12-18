import requests

from app.api.auth import AuthAPI
from app.api.references import ReferenceAPI
from app.api.tasks import TaskAPI
from app.api.projects import ProjectAPI
from app.api.management import ManagementAPI


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

        # Роутеры
        self.auth = AuthAPI(self)
        self.references = ReferenceAPI(self)
        self.tasks = TaskAPI(self)
        self.projects = ProjectAPI(self)
        self.managers = ManagementAPI(self)

    def set_token(self, token):
        self.token = token

    def clear_token(self):
        self.token = None

    def request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as http_err:
            return {"success": False, "error": f"HTTP ошибка: {http_err}"}
        except requests.exceptions.RequestException as err:
            return {"success": False, "error": f"Ошибка запроса: {err.response}"}

    def file_request(self, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            response = requests.request("GET", url, headers=headers, stream=True, **kwargs)
            response.raise_for_status()
            return {"success": True, "data": response.content}
        except requests.exceptions.HTTPError as http_err:
            return {"success": False, "error": f"HTTP ошибка: {http_err}"}
        except requests.exceptions.RequestException as err:
            return {"success": False, "error": f"Ошибка запроса: {err.response}"}


api_client = APIClient("http://127.0.0.1:8000/api/v1")
