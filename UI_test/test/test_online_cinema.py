import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import allure
from allure_commons.types import Severity
from DIPLOM.API_test.pages.kinopoisk_page1 import KinopoiskPage


@allure.epic("Тесты Кинопоиска")
@allure.feature("Проверка онлайн-кинотеатра")
class TestOnlineCinema:
    @pytest.fixture(scope="class")
    def driver(self):
        """Фикстура для инициализации браузера"""
        with allure.step("Инициализация браузера Chrome"):
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=service, options=options)
            yield driver
            driver.quit()

    @allure.story("Проверка кнопки 'Онлайн-кинотеатр'")
    @allure.severity(Severity.CRITICAL)
    @allure.tag("web", "ui", "kinopoisk")
    @allure.title("Проверка перехода в онлайн-кинотеатр")
    @allure.description("Тест проверяет возможность перехода в раздел онлайн-кинотеатра с главной страницы")
    def test_online_cinema_button(self, driver):
        kp_page = KinopoiskPage(driver)

        with allure.step("1. Открываем главную страницу Кинопоиска"):
            kp_page.open()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_main_page",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("2. Принимаем куки, если они есть"):
            try:
                kp_page.accept_cookies()
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot_after_cookies",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    f"Не удалось принять куки: {str(e)}",
                    name="cookies_warning",
                    attachment_type=allure.attachment_type.TEXT
                )

        with allure.step("3. Кликаем на кнопку 'Онлайн-кинотеатр'"):
            click_result = kp_page.click_online_cinema()
            allure.attach(
                str(click_result),
                name="click_result",
                attachment_type=allure.attachment_type.TEXT
            )
            assert click_result, "Не удалось кликнуть на кнопку"

        with allure.step("4. Проверяем переход на страницу онлайн-кинотеатра"):
            is_loaded = kp_page.is_online_cinema_page_loaded()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_online_cinema_page",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                driver.current_url,
                name="current_url",
                attachment_type=allure.attachment_type.TEXT
            )

            error_message = (
                f"Не удалось подтвердить переход. Текущий URL: {driver.current_url}\n"
                "Проверьте:\n"
                "1. Не появилась ли капча\n"
                "2. Актуальность селекторов\n"
                "3. Скриншоты ошибок в папке"
            )

            assert is_loaded, error_message


if __name__ == "__main__":
    pytest.main(["-v", "test_online_cinema.py", "--alluredir=allure-results"])