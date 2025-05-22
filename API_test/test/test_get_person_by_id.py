import pytest
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_api import KinopoiskAPI  # Импортируем класс из вашей структуры проекта

# Тестовые данные
PERSON_ID = 64249  # Пример ID персоны


@allure.epic("Kinopoisk API Tests")
@allure.feature("Person API")
@allure.tag("API", "GET", "Person")
@allure.severity(Severity.CRITICAL)
@allure.title("Поиск персоны по ID")
def test_get_person_by_id():
    api = KinopoiskAPI()

    with allure.step(f"Запрашиваем данные персоны с ID {PERSON_ID}"):
        response = api.get_person_by_id(PERSON_ID)
        response_data = response.json()  # Получаем данные ответа напрямую

    with allure.step("Проверяем статус код 200"):
        assert response.status_code == 200, \
            f"Ожидался статус код 200, но получен {response.status_code}"

    with allure.step("Проверяем базовую структуру ответа"):
        assert "id" in response_data, "Ответ не содержит поле 'id'"
        assert response_data["id"] == PERSON_ID, \
            f"Ожидался ID {PERSON_ID}, но получен {response_data.get('id')}"
        assert "name" in response_data, "Ответ не содержит поле 'name'"
        assert "enName" in response_data, "Ответ не содержит поле 'enName'"

    with allure.step("Анализируем профессии персоны"):
        professions = response_data.get("profession", [])
        allure.attach(
            "\n".join([f"{p.get('value')} ({p.get('slug')})" for p in professions]),
            name="Professions List",
            attachment_type=allure.attachment_type.TEXT
        )


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results"])