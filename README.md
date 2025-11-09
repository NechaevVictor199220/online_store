# Online Store

Проект интернет-магазина с системой управления товарами и категориями.

## Реализованный функционал

### Класс Product
- **name**: Название товара
- **description**: Описание товара  
- **price**: Цена товара
- **quantity**: Количество в наличии

### Класс Category
- **name**: Название категории
- **description**: Описание категории
- **products**: Список товаров категории

### Атрибуты класса Category
- **category_count**: Счетчик количества категорий
- **product_count**: Счетчик общего количества товаров

## Установка и запуск

```bash
# Установка зависимостей
poetry install

# Запуск тестов
poetry run pytest

# Запуск тестов с покрытием
poetry run pytest --cov=src

# Проверка линтером
poetry run flake8 src tests

# Форматирование кода
poetry run black src tests