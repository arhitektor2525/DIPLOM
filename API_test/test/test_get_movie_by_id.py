import pytest
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_api import KinopoiskAPI

# Константы для тестов
MOVIE_ID = 41519  # ID тестового фильма


@allure.epic("Kinopoisk API Tests")
@allure.feature("Movie API")
@allure.tag("API", "GET", "Movie")
@allure.severity(Severity.CRITICAL)
@allure.title("Поиск фильма по ID")
def test_get_movie_by_id():
    api = KinopoiskAPI()

    with allure.step(f"Отправляем запрос для фильма с ID {MOVIE_ID}"):
        response = api.get_movie_by_id(MOVIE_ID)

    with allure.step("Проверяем статус код 200"):
        assert response.status_code == 200, \
            f"Ожидался статус код 200, но получен {response.status_code}"

    with allure.step("Проверяем структуру ответа"):
        movie_data = response.json()
        assert "id" in movie_data, "Ответ не содержит поле 'id'"
        assert movie_data["id"] == MOVIE_ID, \
            f"Ожидался ID фильма {MOVIE_ID}, но получен {movie_data.get('id')}"
        assert "name" in movie_data, "Ответ не содержит поле 'name'"
        assert "year" in movie_data, "Ответ не содержит поле 'year'"


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])