import sys
import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.kinopoisk_page import KinopoiskPage


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    with allure.step("Инициализация браузера"):
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=options)
        yield driver
        with allure.step("Закрытие браузера"):
            driver.quit()


@allure.epic("Тесты Кинопоиска")
@allure.feature("Поиск фильмов")
class TestKinopoiskSearch:
    @allure.story("Поиск фильма 'Анора'")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет возможность поиска фильма 'Анора' на Кинопоиске.
    Шаги:
    1. Открыть главную страницу
    2. Пройти капчу (если требуется)
    3. Выполнить поиск фильма
    4. Проверить результаты поиска
    """)
    def test_search_anora(self, driver):
        page = KinopoiskPage(driver)

        with allure.step("Открытие главной страницы Кинопоиска"):
            page.open()
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Главная страница",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Ручное прохождение капчи (если требуется)"):
            page.pass_captcha_manually(timeout=30)

        with allure.step("Поиск фильма 'Анора'"):
            page.search_movie("Анора")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Результаты поиска",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Проверка результатов поиска"):
            result = page.is_movie_found("Анора")
            allure.attach(
                f"Фильм 'Анора' {'найден' if result else 'не найден'}",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )
            assert result, "Фильм 'Анора' не найден!"