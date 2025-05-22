import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_page1 import KinopoiskPage


@allure.epic("Тесты Кинопоиска")
@allure.feature("Проверка навигации по сайту")
class TestMovieButton:
    @pytest.fixture(scope="class")
    def setup(self):
        """Настройка браузера с опциями"""
        with allure.step("Инициализация браузера с настройками"):
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])

            driver = webdriver.Chrome(service=service, options=options)
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

            allure.attach(
                "Браузер Chrome инициализирован с настройками для обхода автоматизации",
                name="Browser Setup Info",
                attachment_type=allure.attachment_type.TEXT
            )

            yield driver
            driver.quit()

    @allure.story("Проверка кнопки 'Фильмы'")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("web", "ui", "navigation")
    @allure.title("Проверка перехода в раздел 'Фильмы'")
    @allure.description("Тест проверяет корректность работы кнопки 'Фильмы' на главной странице")
    def test_movie_button(self, setup):
        page = KinopoiskPage(setup)

        with allure.step("1. Открываем главную страницу Кинопоиска"):
            page.open()
            allure.attach(
                setup.get_screenshot_as_png(),
                name="Main Page Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                setup.current_url,
                name="Initial URL",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Кликаем на кнопку 'Фильмы'"):
            click_result = page.click_movie_button()
            allure.attach(
                str(click_result),
                name="Click Result",
                attachment_type=allure.attachment_type.TEXT
            )
            assert click_result, "Не удалось кликнуть на кнопку 'Фильмы'"

        with allure.step("3. Проверяем URL после перехода"):
            current_url = setup.current_url
            expected_url_part = "lists/categories/movies"
            url_check = expected_url_part in current_url

            allure.attach(
                current_url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                setup.get_screenshot_as_png(),
                name="Movies Page Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            if not url_check:
                allure.attach(
                    f"Ожидаемая часть URL: {expected_url_part}\nФактический URL: {current_url}",
                    name="URL Mismatch Details",
                    attachment_type=allure.attachment_type.TEXT
                )

            assert url_check, \
                f"Неверный URL после клика: {current_url}"


if __name__ == "__main__":
    pytest.main(["-v", "test_movie_button.py", "--alluredir=allure-results"])