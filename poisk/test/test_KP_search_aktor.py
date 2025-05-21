import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import allure
from allure_commons.types import Severity, AttachmentType

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.kinopoisk_page import KinopoiskPage


@pytest.fixture
def driver():
    with allure.step("Инициализация Chrome драйвера"):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        allure.attach(
            "Chrome драйвер успешно инициализирован",
            name="Driver Initialization",
            attachment_type=AttachmentType.TEXT
        )
        yield driver
        with allure.step("Закрытие браузера"):
            driver.quit()
            allure.attach(
                "Браузер успешно закрыт",
                name="Browser Quit",
                attachment_type=AttachmentType.TEXT
            )


@allure.epic("Тесты Кинопоиска")
@allure.feature("Поиск по сайту")
@allure.story("Поиск актёров")
@allure.severity(Severity.NORMAL)
@allure.tag("web", "search", "actor")
@allure.title("Поиск актёра Брюс Уиллис")
@allure.description("Тест проверяет возможность поиска информации об актёре Брюс Уиллис")
def test_search_bruce_willis(driver):
    page = KinopoiskPage(driver)

    with allure.step("1. Открываем главную страницу Кинопоиска"):
        page.open()
        allure.attach(
            driver.current_url,
            name="Current URL",
            attachment_type=AttachmentType.TEXT
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Main Page",
            attachment_type=AttachmentType.PNG
        )

    with allure.step("2. Проходим капчу вручную (если требуется)"):
        page.pass_captcha_manually(timeout=30)
        allure.attach(
            "Ожидание 30 секунд для ручного ввода капчи",
            name="Captcha Wait",
            attachment_type=AttachmentType.TEXT
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="After Captcha",
            attachment_type=AttachmentType.PNG
        )

    with allure.step("3. Выполняем поиск по запросу 'Брюс Уиллис'"):
        page.search_movie("Брюс Уиллис")
        allure.attach(
            "Выполнен поиск по запросу 'Брюс Уиллис'",
            name="Search Query",
            attachment_type=AttachmentType.TEXT
        )
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Search Results Page",
            attachment_type=AttachmentType.PNG
        )

    with allure.step("4. Проверяем наличие результатов поиска"):
        result = page.is_result_found("Брюс Уиллис")
        allure.attach(
            str(result),
            name="Search Results Found",
            attachment_type=AttachmentType.TEXT
        )
        allure.attach(
            driver.current_url,
            name="Results Page URL",
            attachment_type=AttachmentType.TEXT
        )

        if not result:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Search Failed",
                attachment_type=AttachmentType.PNG
            )

        assert result, "Результаты по запросу 'Брюс Уиллис' не найдены!"


if __name__ == "__main__":
    pytest.main(["-v", "--alluredir=allure-results", os.path.abspath(__file__)])