import pytest

from src.online_store.models import (
    Category,
    LawnGrass,
    Product,
    Smartphone,
    ZeroQuantityError,
)


class TestZeroQuantityException:
    """Тесты для исключения при нулевом количестве товара."""

    def test_product_zero_quantity_raises_exception(self):
        """Тест, что создание Product с нулевым количеством вызывает исключение."""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product("Товар", "Описание", 100.0, 0)

    def test_smartphone_zero_quantity_raises_exception(self):
        """Тест, что создание Smartphone с нулевым количеством вызывает исключение."""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Smartphone(
                name="Смартфон",
                description="Описание",
                price=50000.0,
                quantity=0,
                efficiency=4.0,
                model="X",
                memory=128,
                color="Black",
            )

    def test_lawn_grass_zero_quantity_raises_exception(self):
        """Тест, что создание LawnGrass с нулевым количеством вызывает исключение."""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            LawnGrass(
                name="Трава",
                description="Описание",
                price=2000.0,
                quantity=0,
                country="Россия",
                germination_period=12,
                color="Green",
            )

    def test_new_product_zero_quantity_raises_exception(self):
        """Тест, что класс-метод new_product с нулевым количеством вызывает исключение."""
        product_data = {
            "name": "Товар",
            "description": "Описание",
            "price": 100.0,
            "quantity": 0,
        }

        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product.new_product(product_data)

    def test_add_product_zero_quantity_to_category_raises_exception(self):
        """Тест, что добавление товара с нулевым количеством в категорию вызывает исключение."""
        category = Category("Категория", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)

        # Меняем количество на 0
        product.quantity = 0

        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            category.add_product(product)

    def test_valid_quantity_creates_product(self):
        """Тест, что товар с положительным количеством создается успешно."""
        product = Product("Товар", "Описание", 100.0, 5)
        assert product.quantity == 5
        assert product.name == "Товар"


class TestAveragePrice:
    """Тесты для метода расчета средней цены."""

    def test_average_price_with_products(self):
        """Тест расчета средней цены при наличии товаров."""
        products = [
            Product("Товар1", "Описание", 100.0, 5),
            Product("Товар2", "Описание", 200.0, 3),
            Product("Товар3", "Описание", 300.0, 2),
        ]

        category = Category("Категория", "Описание", products)

        average_price = category.average_price()
        expected_average = (100.0 + 200.0 + 300.0) / 3

        assert average_price == expected_average
        assert average_price == 200.0

    def test_average_price_single_product(self):
        """Тест расчета средней цены для одной категории с одним товаром."""
        products = [Product("Товар", "Описание", 150.0, 1)]
        category = Category("Категория", "Описание", products)

        average_price = category.average_price()

        assert average_price == 150.0

    def test_average_price_empty_category(self):
        """Тест расчета средней цены для пустой категории."""
        category = Category("Пустая категория", "Описание", [])

        average_price = category.average_price()

        assert average_price == 0.0

    def test_average_price_with_different_product_types(self):
        """Тест расчета средней цены с разными типами товаров."""
        product = Product("Обычный товар", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=4.0,
            model="X",
            memory=128,
            color="Black",
        )
        lawn_grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Россия",
            germination_period=12,
            color="Green",
        )

        category = Category(
            "Разные товары", "Описание", [product, smartphone, lawn_grass]
        )

        average_price = category.average_price()
        expected_average = (100.0 + 50000.0 + 2000.0) / 3

        assert average_price == expected_average

    def test_average_price_after_adding_products(self):
        """Тест расчета средней цены после добавления товаров."""
        category = Category("Категория", "Описание", [])

        # Изначально пустая категория
        assert category.average_price() == 0.0

        # Добавляем товары
        product1 = Product("Товар1", "Описание", 100.0, 5)
        product2 = Product("Товар2", "Описание", 200.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        average_price = category.average_price()
        expected_average = (100.0 + 200.0) / 2

        assert average_price == expected_average


class TestIntegration:
    """Интеграционные тесты для новой функциональности."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_json_loader_with_zero_quantity_raises_exception(self, tmp_path):
        """Тест, что JSON загрузчик вызывает исключение при нулевом количестве."""
        import json

        from src.online_store.json_loader import load_categories_from_json

        json_data = [
            {
                "name": "Тестовая категория",
                "description": "Описание",
                "products": [
                    {
                        "name": "Товар с нулевым количеством",
                        "description": "Описание",
                        "price": 100.0,
                        "quantity": 0,  # Нулевое количество
                    }
                ],
            }
        ]

        json_file = tmp_path / "test_zero_quantity.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        with pytest.raises(ZeroQuantityError):
            load_categories_from_json(json_file)

    def test_category_summary_includes_average_prices(self):
        """Тест, что сводка категорий включает средние цены."""
        from src.online_store.json_loader import get_categories_summary

        products1 = [
            Product("Товар1", "Описание", 100.0, 5),
            Product("Товар2", "Описание", 200.0, 3),
        ]
        products2 = [Product("Товар3", "Описание", 300.0, 2)]

        categories = [
            Category("Кат1", "Описание1", products1),
            Category("Кат2", "Описание2", products2),
            Category("Пустая", "Описание3", []),
        ]

        summary = get_categories_summary(categories)

        # Проверяем средние цены
        assert summary["average_prices"]["Кат1"] == 150.0
        assert summary["average_prices"]["Кат2"] == 300.0
        assert summary["average_prices"]["Пустая"] == 0.0

        # Проверяем структуру категорий
        for category_info in summary["categories"]:
            if category_info["name"] == "Кат1":
                assert category_info["average_price"] == 150.0
            elif category_info["name"] == "Кат2":
                assert category_info["average_price"] == 300.0
            elif category_info["name"] == "Пустая":
                assert category_info["average_price"] == 0.0


class TestBackwardCompatibility:
    """Тесты для обратной совместимости."""

    def test_existing_tests_still_work(self):
        """Тест, что существующая функциональность продолжает работать."""
        # Создание товаров с положительным количеством работает
        product = Product("Товар", "Описание", 100.0, 5)
        assert product.name == "Товар"
        assert product.quantity == 5

        # Добавление в категорию работает
        category = Category("Категория", "Описание", [])
        category.add_product(product)
        assert len(category._Category__products) == 1

        # Сложение товаров работает
        product2 = Product("Товар", "Описание", 100.0, 3)
        result = product + product2
        assert result.quantity == 8
