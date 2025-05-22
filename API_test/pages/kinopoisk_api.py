import requests
import allure
import json
from urllib.parse import quote
from allure_commons.types import Severity
from typing import Optional, Dict, Any


class KinopoiskAPI:
    BASE_URL = "https://api.kinopoisk.dev"
    API_KEY = "5BEMM39-R84M95R-K5JG6RJ-786NSJQ"  # Замените на реальный ключ

    def __init__(self):
        self.headers = {
            "X-API-KEY": self.API_KEY,
            "Content-Type": "application/json"
        }

    @allure.step("Отправка {method} запроса к {endpoint}")
    def _send_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Базовый метод для отправки запросов с Allure-логированием"""
        url = f"{self.BASE_URL}{endpoint}"

        with allure.step(f"Формирование {method} запроса"):
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params
            )

        self._log_request(response, params)
        self._log_response(response)
        return response

    @allure.step("Логирование деталей запроса")
    def _log_request(self, response: requests.Response, params: Optional[Dict] = None) -> None:
        """Детальное логирование запроса с Allure-аттачами"""
        request_details = {
            "URL": response.request.url,
            "Method": response.request.method,
            "Headers": dict(response.request.headers),
            "Params": params,
            "Body": getattr(response.request, 'body', None)
        }

        allure.attach(
            json.dumps(request_details, indent=2, ensure_ascii=False),
            name="Request Details",
            attachment_type=allure.attachment_type.JSON
        )

    @allure.step("Логирование деталей ответа")
    def _log_response(self, response: requests.Response) -> Dict[str, Any]:
        """Детальное логирование ответа с Allure-аттачами"""
        try:
            response_data = response.json()
        except ValueError:
            response_data = {"error": "Invalid JSON response", "text": response.text}

        response_details = {
            "Status Code": response.status_code,
            "Headers": dict(response.headers),
            "Body": response_data,
            "Elapsed Time": f"{response.elapsed.total_seconds()}s"
        }

        allure.attach(
            json.dumps(response_details, indent=2, ensure_ascii=False),
            name="Response Details",
            attachment_type=allure.attachment_type.JSON
        )

        # Добавляем скриншотный аттач (имитация)
        allure.attach(
            f"Response time: {response.elapsed.total_seconds()} seconds",
            name="Performance Info",
            attachment_type=allure.attachment_type.TEXT
        )

        return response_data

    # Методы API с Allure-аннотациями
    @allure.step("Получение списка изображений (страница {page}, лимит {limit})")
    def get_images_list(self, page: int = 1, limit: int = 10) -> requests.Response:
        return self._send_request("GET", "/v1.4/image", {"page": page, "limit": limit})

    @allure.step("Получение информации о фильме по ID {movie_id}")
    def get_movie_by_id(self, movie_id: int) -> requests.Response:
        return self._send_request("GET", f"/v1.4/movie/{movie_id}")

    @allure.step("Получение списка жанров")
    def get_movie_genres(self) -> requests.Response:
        return self._send_request("GET", "/v1/movie/possible-values-by-field", {"field": "genres.name"})

    @allure.step("Получение информации о персоне по ID {person_id}")
    def get_person_by_id(self, person_id: int) -> requests.Response:
        return self._send_request("GET", f"/v1.4/person/{person_id}")

    @allure.step("Поиск фильма по названию '{title}'")
    def search_movie(self, title: str, page: int = 1, limit: int = 10) -> requests.Response:
        return self._send_request("GET", "/v1.4/movie/search", {
            "page": page,
            "limit": limit,
            "query": title
        })

    @allure.step("Проверка доступности API")
    def health_check(self) -> bool:
        """Дополнительный метод для проверки здоровья API"""
        try:
            response = self._send_request("GET", "/v1/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            allure.attach("API недоступно", name="Health Check Failed", attachment_type=allure.attachment_type.TEXT)
            return False