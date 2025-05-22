import pytest
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_api import KinopoiskAPI


@allure.epic("Kinopoisk API Tests")
@allure.feature("Movie Genres API")
@allure.tag("API", "GET", "Genres")
@allure.severity(Severity.NORMAL)
@allure.title("Получение списка жанров")
def test_get_movie_genres_list():
    api = KinopoiskAPI()

    with allure.step("Получаем список жанров"):
        response = api.get_movie_genres()
        response_data = response.json()

    with allure.step("Проверяем статус код 200"):
        assert response.status_code == 200, \
            f"Ожидался статус код 200, но получен {response.status_code}"

    with allure.step("Проверяем структуру ответа"):
        assert isinstance(response_data, list), "Ответ должен быть списком"
        assert len(response_data) > 0, "Список жанров не должен быть пустым"

        # Проверяем структуру элементов списка
        for genre in response_data:
            assert "name" in genre, "Жанр должен содержать поле 'name'"
            assert "slug" in genre, "Жанр должен содержать поле 'slug'"

    with allure.step("Проверяем наличие основных жанров"):
        required_genres = ["драма", "комедия", "боевик", "фантастика"]
        genre_names = [g["name"].lower() for g in response_data]
        missing_genres = [g for g in required_genres if g not in genre_names]

        if missing_genres:
            allure.attach(
                f"Отсутствующие жанры: {', '.join(missing_genres)}",
                name="Missing Genres Warning",
                attachment_type=allure.attachment_type.TEXT
            )


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])