import pytest
import json
import os

from src.online_store.json_loader import (
    load_categories_from_json,
    get_categories_summary,
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
        # Создаем временный JSON файл с правильной структурой
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
        assert len(categories[0].products) == 1
        assert categories[0].products[0].name == "Тестовый товар"
        assert Category.category_count == 1
        assert Category.product_count == 1

    def test_load_categories_from_json_multiple_categories(self, tmp_path):
        """Тест загрузки нескольких категорий из JSON."""
        json_data = {
            "categories": [
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
        }

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        categories = load_categories_from_json(json_file)

        assert len(categories) == 2
        assert Category.category_count == 2
        assert Category.product_count == 3

        # Проверяем первую категорию
        assert categories[0].name == "Категория 1"
        assert len(categories[0].products) == 1
        assert categories[0].products[0].price == 100.0

        # Проверяем вторую категорию
        assert categories[1].name == "Категория 2"
        assert len(categories[1].products) == 2
        assert categories[1].products[1].quantity == 3

    def test_load_categories_from_json_empty_products(self, tmp_path):
        """Тест загрузки категории с пустым списком товаров."""
        json_data = {
            "categories": [
                {"name": "Пустая категория", "description": "Описание", "products": []}
            ]
        }

        json_file = tmp_path / "test_products.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        categories = load_categories_from_json(json_file)

        assert len(categories) == 1
        assert categories[0].name == "Пустая категория"
        assert categories[0].products == []
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
        json_data = {
            "categories": [
                {
                    "name": "Категория",
                    # Отсутствует description
                    "products": [],
                }
            ]
        }

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
    json_data = {
        "categories": [
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
    }

    json_file = tmp_path / "fixture_products.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    return json_file


def test_with_json_fixture(sample_json_file):
    """Тест с использованием фикстуры JSON файла."""
    categories = load_categories_from_json(sample_json_file)

    assert len(categories) == 1
    assert categories[0].name == "Фикстурная категория"
    assert categories[0].products[0].name == "Фикстурный товар"
    assert categories[0].products[0].price == 999.99
