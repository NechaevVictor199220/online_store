import json
import os

import pytest

from src.online_store.json_loader import (
    get_categories_summary,
    load_categories_from_json,
)
from src.online_store.models import Category, Product


class TestJsonLoader:
    """Тесты для загрузчика JSON данных."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_load_categories_from_json_valid_file(self, tmp_path):
        """Тест загрузки категорий из корректного JSON файла."""
        # Создаем временный JSON файл с правильной структурой (список категорий)
        json_data = [
            {
                "name": "Тестовая категория",
                "description": "Тестовое описание",
                "products": [
                    {
                        "name": "Тестовый товар",
                        "description": "Тестовое описание товара",
                        "price": 1000.0,
                        "quantity": 5,
                    }
                ],
            }
        ]

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # Загружаем категории
        categories = load_categories_from_json(json_file)

        # Проверяем результат
        assert len(categories) == 1
        assert categories[0].name == "Тестовая категория"
        # products теперь возвращает строку, проверяем содержание
        products_str = categories[0].products
        assert "Тестовый товар" in products_str
        assert "1000.0 руб." in products_str
        assert Category.category_count == 1
        assert Category.product_count == 1

    def test_load_categories_from_json_multiple_categories(self, tmp_path):
        """Тест загрузки нескольких категорий из JSON."""
        # ПРАВИЛЬНАЯ СТРУКТУРА: список категорий
        json_data = [
            {
                "name": "Категория 1",
                "description": "Описание 1",
                "products": [
                    {
                        "name": "Товар 1",
                        "description": "Описание товара 1",
                        "price": 100.0,
                        "quantity": 10,
                    }
                ],
            },
            {
                "name": "Категория 2",
                "description": "Описание 2",
                "products": [
                    {
                        "name": "Товар 2",
                        "description": "Описание товара 2",
                        "price": 200.0,
                        "quantity": 5,
                    },
                    {
                        "name": "Товар 3",
                        "description": "Описание товара 3",
                        "price": 300.0,
                        "quantity": 3,
                    },
                ],
            },
        ]

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        categories = load_categories_from_json(json_file)

        assert len(categories) == 2
        assert Category.category_count == 2
        assert Category.product_count == 3

        # Проверяем первую категорию через геттер (строку)
        assert categories[0].name == "Категория 1"
        products_str1 = categories[0].products
        assert "Товар 1" in products_str1
        assert "100.0 руб." in products_str1

        # Проверяем вторую категорию
        assert categories[1].name == "Категория 2"
        products_str2 = categories[1].products
        assert "Товар 2" in products_str2
        assert "Товар 3" in products_str2

    def test_load_categories_from_json_empty_products(self, tmp_path):
        """Тест загрузки категории с пустым списком товаров."""
        # ПРАВИЛЬНАЯ СТРУКТУРА: список категорий
        json_data = [
            {"name": "Пустая категория", "description": "Описание", "products": []}
        ]

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        categories = load_categories_from_json(json_file)

        assert len(categories) == 1
        assert categories[0].name == "Пустая категория"
        assert categories[0].products == ""  # Пустая строка
        assert Category.category_count == 1
        assert Category.product_count == 0

    def test_load_categories_from_json_file_not_found(self):
        """Тест обработки ошибки при отсутствии файла."""
        with pytest.raises(FileNotFoundError):
            load_categories_from_json("nonexistent_file.json")

    def test_load_categories_from_json_invalid_json(self, tmp_path):
        """Тест обработки некорректного JSON."""
        json_file = tmp_path / "invalid.json"
        with open(json_file, "w", encoding="utf-8") as f:
            f.write("invalid json content")

        with pytest.raises(json.JSONDecodeError):
            load_categories_from_json(json_file)

    def test_load_categories_from_json_missing_required_fields(self, tmp_path):
        """Тест обработки отсутствия обязательных полей."""
        # ПРАВИЛЬНАЯ СТРУКТУРА: список категорий
        json_data = [
            {
                "name": "Категория",
                # Отсутствует description - ДОЛЖНО ВЫЗВАТЬ KeyError
                "products": [],
            }
        ]

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        with pytest.raises(KeyError):
            load_categories_from_json(json_file)

    def test_get_categories_summary(self):
        """Тест функции получения сводной информации."""
        # Создаем тестовые категории
        products1 = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3),
        ]
        products2 = [Product("Товар3", "Описание3", 300.0, 2)]

        categories = [
            Category("Кат1", "Описание1", products1),
            Category("Кат2", "Описание2", products2),
        ]

        summary = get_categories_summary(categories)

        assert summary["total_categories"] == 2
        assert summary["total_products"] == 3
        assert len(summary["categories"]) == 2
        assert summary["categories"][0]["name"] == "Кат1"
        assert summary["categories"][0]["product_count"] == 2
        assert summary["categories"][1]["name"] == "Кат2"
        assert summary["categories"][1]["product_count"] == 1


@pytest.fixture
def sample_json_file(tmp_path):
    """Фикстура для создания тестового JSON файла."""
    # ПРАВИЛЬНАЯ СТРУКТУРА: список категорий
    json_data = [
        {
            "name": "Фикстурная категория",
            "description": "Описание из фикстуры",
            "products": [
                {
                    "name": "Фикстурный товар",
                    "description": "Описание товара из фикстуры",
                    "price": 999.99,
                    "quantity": 7,
                }
            ],
        }
    ]

    json_file = tmp_path / "fixture_products.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    return json_file


def test_with_json_fixture(sample_json_file):
    """Тест с использованием фикстуры JSON файла."""
    categories = load_categories_from_json(sample_json_file)

    assert len(categories) == 1
    assert categories[0].name == "Фикстурная категория"
    products_str = categories[0].products
    assert "Фикстурный товар" in products_str
    assert "999.99 руб." in products_str


class TestJsonLoaderWithOldStructure:
    """Тесты для старой структуры JSON (с ключом 'categories')."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_load_categories_from_json_old_structure_fails(self, tmp_path):
        """Тест, что старая структура JSON вызывает ошибку."""
        # СТАРАЯ СТРУКТУРА: объект с ключом 'categories'
        json_data = {
            "categories": [
                {
                    "name": "Старая категория",
                    "description": "Описание",
                    "products": [
                        {
                            "name": "Старый товар",
                            "description": "Описание товара",
                            "price": 500.0,
                            "quantity": 2,
                        }
                    ],
                }
            ]
        }

        json_file = tmp_path / "test_old_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        # Эта структура должна вызвать ошибку
        with pytest.raises((AttributeError, KeyError)):
            load_categories_from_json(json_file)
