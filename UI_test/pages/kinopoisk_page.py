from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import allure
from allure_commons.types import AttachmentType


class KinopoiskPage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.kinopoisk.ru/"
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу Кинопоиска")
    def open(self):
        """Открыть главную страницу Кинопоиска"""
        with allure.step(f"Переходим по URL: {self.base_url}"):
            self.driver.get(self.base_url)
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="main_page_loaded",
                attachment_type=AttachmentType.PNG
            )

    @allure.step("Ручное прохождение капчи")
    def pass_captcha_manually(self, timeout=30):
        """Пауза для ручного прохождения капчи"""
        with allure.step(f"Ожидание {timeout} секунд для ручного ввода капчи"):
            allure.attach(
                "Пожалуйста, пройдите капчу вручную в открывшемся браузере",
                name="captcha_manual_input",
                attachment_type=AttachmentType.TEXT
            )
            time.sleep(timeout)
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="after_captcha",
                attachment_type=AttachmentType.PNG
            )

    @allure.step("Поиск фильма: {movie_name}")
    def search_movie(self, movie_name):
        """Поиск фильма по названию"""
        with allure.step(f"Вводим название фильма: {movie_name}"):
            search_input = self.driver.find_element(By.NAME, "kp_query")
            search_input.clear()
            search_input.send_keys(movie_name)
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="search_input_filled",
                attachment_type=AttachmentType.PNG
            )

        with allure.step("Отправляем поисковый запрос"):
            search_input.send_keys(Keys.RETURN)
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "search_results"))
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="search_results_page",
                attachment_type=AttachmentType.PNG
            )

    @allure.step("Проверка найденного фильма: {movie_name}")
    def is_movie_found(self, movie_name):
        """Проверить, что фильм найден"""
        result = (
                movie_name.lower() in self.driver.page_source.lower()
                or movie_name.lower() in self.driver.current_url.lower()
        )

        allure.attach(
            str(result),
            name="movie_found_result",
            attachment_type=AttachmentType.TEXT
        )
        allure.attach(
            self.driver.current_url,
            name="current_url",
            attachment_type=AttachmentType.TEXT
        )

        return result

    @allure.step("Проверка найденного результата: {query}")
    def is_result_found(self, query):
        """Проверить, что результат найден"""
        result = (
                query.lower() in self.driver.page_source.lower()
                or query.lower() in self.driver.current_url.lower()
        )

        allure.attach(
            str(result),
            name="search_result_found",
            attachment_type=AttachmentType.TEXT
        )

        return result

    @allure.step("Принятие cookies")
    def accept_cookies(self):
        """Принять куки, если появилось окно"""
        try:
            cookie_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Принимаю')]")))

            with allure.step("Нажимаем кнопку принятия cookies"):
                cookie_btn.click()
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="cookies_accepted",
                    attachment_type=AttachmentType.PNG
                )
        except TimeoutException:
            allure.attach(
                "Окно с куками не появилось",
                name="cookies_not_found",
                attachment_type=AttachmentType.TEXT
            )

    @allure.step("Клик на кнопку 'Онлайн-кинотеатр'")
    def click_online_cinema(self):
        """Кликает на кнопку 'Онлайн-кинотеатр'"""
        try:
            online_cinema_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-tid='acc26a70']")))

            with allure.step("Нажимаем кнопку онлайн-кинотеатра"):
                online_cinema_btn.click()
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="online_cinema_clicked",
                    attachment_type=AttachmentType.PNG
                )
                return True

        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="online_cinema_error",
                attachment_type=AttachmentType.PNG
            )
            return False

    @allure.step("Проверка загрузки страницы онлайн-кинотеатра")
    def is_online_cinema_page_loaded(self):
        """Проверяет загрузку страницы онлайн-кинотеатра"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.url_contains("hd.kinopoisk.ru"))

            allure.attach(
                self.driver.current_url,
                name="online_cinema_url",
                attachment_type=AttachmentType.TEXT
            )
            return True

        except TimeoutException:
            current_url = self.driver.current_url
            allure.attach(
                current_url,
                name="failed_online_cinema_url",
                attachment_type=AttachmentType.TEXT
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="online_cinema_load_error",
                attachment_type=AttachmentType.PNG
            )
            return False

    @allure.step("Клик на кнопку 'Фильмы'")
    def click_movie_button(self):
        """Кликает на кнопку 'Фильмы' в сайдбаре"""
        try:
            button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     "#__next div.styles_sidebarColumn__kpYI5 li:nth-child(3) > a")
                )
            )

            with allure.step("Нажимаем кнопку 'Фильмы'"):
                button.click()
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="movie_button_clicked",
                    attachment_type=AttachmentType.PNG
                )
                return True

        except TimeoutException as e:
            allure.attach(
                str(e),
                name="movie_button_error",
                attachment_type=AttachmentType.TEXT
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="movie_button_not_found",
                attachment_type=AttachmentType.PNG
            )
            return False