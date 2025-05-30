# Тестирование Кинопоиска: API и UI

Проект содержит автоматизированные тесты для API и пользовательского интерфейса (UI) Кинопоиска.

## Структура проекта
DIPLOM
1) API_test
  -pages/kinopoisk_api
  -test_get_images_list.py
  -test_get_movie_by_id.py
  -test_get_movie_genres_list.py
  -test_get_person_by_id.py
  -test_search_movie_by_title.py
2) UI_test
  -pages/kinopoisk_api
  -test_KP_search_aktor.py
  -test_KP_search_film.py
  -test_KP_search_serial.py
  -test_movie_button.py
  -test_online_cinema.py
3) .gitignore
4) requirements.txt # Зависимости
5) README.md # Документация


## Запуск тестов

**Предварительно:**
- Установите браузер Chrome
- запускать тесты через интерфейс / через терминал

### Запуск через терминал
### 1. UI-тесты

   -cd C:\Users\arhit\OneDrive\Desktop\Diplom_work\DIPLOM\UI_test - перейти в директорию UI_test
   -pytest - для запуска тестов

### 2. API-тесты

   -cd C:\Users\arhit\OneDrive\Desktop\Diplom_work\DIPLOM\API_test - перейти в директорию API_test
   -pytest - для запуска тестов

### 3. Все тесты
   -cd C:\Users\arhit\OneDrive\Desktop\Diplom_work\DIPLOM перейти в директорию DIPLOM 
   -python -m pytest --alluredir allure-result - для запуска тестов

  В директории с тестами появится папка allure-result. Там сохранятся отчеты о тестах.

## Введите команду ниже — сгенерируется отчет о тестах:
    allure serve allure-result
Отчет откроется на локальном сервере в окне вашего браузера.
Overview — раздел с общей информацией: сколько всего тестов запустили, процент успешных тестов, доля успешных и неуспешных тестов.

## Ссылка на финальный проект:
  https://ivandrago1991.yonote.ru/share/633b06f4-fbb6-4a98-8edd-bbc2117447e3





