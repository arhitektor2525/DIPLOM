import pytest
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_api import KinopoiskAPI  # Импортируем класс из вашей структуры проекта


@allure.epic("Kinopoisk API Tests")
@allure.feature("Images API")
@allure.tag("API", "GET", "Images")
@allure.severity(Severity.NORMAL)
@allure.title("Получение списка изображений")
def test_get_images_list():
    api = KinopoiskAPI()  # Создаем экземпляр класса

    with allure.step("Подготавливаем параметры запроса"):
        page = 1
        limit = 10

    with allure.step("Отправляем запрос и получаем ответ"):
        response = api.get_images_list(page=page, limit=limit)  # Вызываем метод через экземпляр
        response_data = response.json()

    with allure.step("Проверяем статус код 200"):
        assert response.status_code == 200, \
            f"Ожидался статус код 200, но получен {response.status_code}"

    with allure.step("Проверяем структуру ответа"):
        assert isinstance(response_data, dict), "Ответ должен быть словарем"
        assert "docs" in response_data, "Ответ должен содержать поле 'docs'"
        assert "total" in response_data, "Ответ должен содержать поле 'total'"
        assert "page" in response_data, "Ответ должен содержать поле 'page'"
        assert "limit" in response_data, "Ответ должен содержать поле 'limit'"

    with allure.step("Проверяем список изображений"):
        images = response_data.get("docs", [])
        assert isinstance(images, list), "Поле 'docs' должно быть списком"
        assert len(images) <= limit, \
            f"Количество изображений превышает лимит {limit}"


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])