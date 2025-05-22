import pytest
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_api import KinopoiskAPI

# Тестовые данные
MOVIE_TITLE = "джентльмены удачи"


@allure.epic("Kinopoisk API Tests")
@allure.feature("Movie Search API")
@allure.tag("API", "GET", "Search")
@allure.severity(Severity.CRITICAL)
@allure.title("Поиск фильма по названию")
def test_search_movie_by_title():
    api = KinopoiskAPI()

    with allure.step(f"Ищем фильм '{MOVIE_TITLE}'"):
        response = api.search_movie(MOVIE_TITLE)
        search_data = response.json()

    with allure.step("Проверяем статус код 200"):
        assert response.status_code == 200, \
            f"Ожидался статус код 200, но получен {response.status_code}"

    with allure.step("Проверяем структуру ответа"):
        assert "docs" in search_data, "Ответ не содержит поле 'docs'"
        assert "total" in search_data, "Ответ не содержит поле 'total'"
        assert "limit" in search_data, "Ответ не содержит поле 'limit'"
        assert "page" in search_data, "Ответ не содержит поле 'page'"

    with allure.step("Проверяем результаты поиска"):
        assert search_data["total"] > 0, "Поиск не дал результатов"

        found = any(
            movie["name"] and MOVIE_TITLE.lower() in movie["name"].lower()
            for movie in search_data["docs"]
        )
        assert found, f"Фильм '{MOVIE_TITLE}' не найден в результатах поиска"


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])