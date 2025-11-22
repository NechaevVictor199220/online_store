import pytest
from src.online_store.models import Product, Category, CategoryIterator


class TestProductMagicMethods:
    """Тесты для магических методов класса Product."""

    def test_product_str_method(self):
        """Тест строкового представления Product."""
        product = Product("Телефон", "Смартфон", 50000.0, 10)

        expected_str = "Телефон, 50000.0 руб. Остаток: 10 шт."
        assert str(product) == expected_str

    def test_product_str_method_with_different_values(self):
        """Тест строкового представления с разными значениями."""
        product1 = Product("Товар1", "Описание", 100.0, 5)
        product2 = Product("Товар2", "Описание", 999.99, 1)

        assert str(product1) == "Товар1, 100.0 руб. Остаток: 5 шт."
        assert str(product2) == "Товар2, 999.99 руб. Остаток: 1 шт."

    def test_product_add_method(self):
        """Тест сложения двух товаров."""
        product1 = Product("Товар1", "Описание", 100.0, 5)  # 100 * 5 = 500
        product2 = Product("Товар2", "Описание", 200.0, 3)  # 200 * 3 = 600

        result = product1 + product2

        assert result == 1100.0  # 500 + 600

    def test_product_add_method_with_zero_quantity(self):
        """Тест сложения товаров с нулевым количеством."""
        product1 = Product("Товар1", "Описание", 100.0, 0)  # 100 * 0 = 0
        product2 = Product("Товар2", "Описание", 200.0, 5)  # 200 * 5 = 1000

        result = product1 + product2

        assert result == 1000.0

    def test_product_add_method_same_product(self):
        """Тест сложения товара с самим собой."""
        product = Product("Товар", "Описание", 150.0, 4)  # 150 * 4 = 600

        result = product + product

        assert result == 1200.0  # 600 + 600

    def test_product_add_method_type_error(self):
        """Тест ошибки при сложении с неправильным типом."""
        product = Product("Товар", "Описание", 100.0, 5)

        with pytest.raises(
            TypeError, match="Можно складывать только объекты класса Product"
        ):
            product + "не товар"

        with pytest.raises(TypeError):
            product + 123

    def test_product_add_method_commutative(self):
        """Тест коммутативности сложения."""
        product1 = Product("Товар1", "Описание", 100.0, 2)
        product2 = Product("Товар2", "Описание", 300.0, 1)

        result1 = product1 + product2
        result2 = product2 + product1

        assert result1 == result2 == 500.0  # (100*2) + (300*1) = 500


class TestCategoryMagicMethods:
    """Тесты для магических методов класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_str_method_empty(self):
        """Тест строкового представления пустой категории."""
        category = Category("Пустая", "Описание", [])

        expected_str = "Пустая, количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_category_str_method_single_product(self):
        """Тест строкового представления категории с одним товаром."""
        product = Product("Товар", "Описание", 100.0, 5)
        category = Category("Категория", "Описание", [product])

        expected_str = "Категория, количество продуктов: 5 шт."
        assert str(category) == expected_str

    def test_category_str_method_multiple_products(self):
        """Тест строкового представления категории с несколькими товарами."""
        products = [
            Product("Товар1", "Описание", 100.0, 3),  # 3 шт
            Product("Товар2", "Описание", 200.0, 2),  # 2 шт
            Product("Товар3", "Описание", 300.0, 1),  # 1 шт
        ]
        category = Category("Категория", "Описание", products)

        expected_str = "Категория, количество продуктов: 6 шт."  # 3+2+1=6
        assert str(category) == expected_str

    def test_category_str_method_with_zero_quantity(self):
        """Тест строкового представления с товарами с нулевым количеством."""
        products = [
            Product("Товар1", "Описание", 100.0, 0),  # 0 шт
            Product("Товар2", "Описание", 200.0, 5),  # 5 шт
            Product("Товар3", "Описание", 300.0, 0),  # 0 шт
        ]
        category = Category("Категория", "Описание", products)

        expected_str = "Категория, количество продуктов: 5 шт."  # 0+5+0=5
        assert str(category) == expected_str

    def test_products_getter_uses_product_str(self):
        """Тест, что геттер products использует __str__ Product."""
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
        ]
        category = Category("Категория", "Описание", products)

        products_str = category.products

        # Проверяем, что используется строковое представление Product
        assert "Товар1, 100.0 руб. Остаток: 3 шт." in products_str
        assert "Товар2, 200.0 руб. Остаток: 2 шт." in products_str


class TestCategoryIterator:
    """Тесты для итератора категории."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_iterator_creation(self):
        """Тест создания итератора."""
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
        ]
        category = Category("Категория", "Описание", products)

        iterator = iter(category)

        assert isinstance(iterator, CategoryIterator)

    def test_category_iterator_iteration(self):
        """Тест итерации по товарам категории."""
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
        ]
        category = Category("Категория", "Описание", products)

        # Используем цикл for
        iterated_products = []
        for product in category:
            iterated_products.append(product)

        assert len(iterated_products) == 2
        assert iterated_products[0].name == "Товар1"
        assert iterated_products[1].name == "Товар2"

    def test_category_iterator_empty(self):
        """Тест итерации по пустой категории."""
        category = Category("Пустая", "Описание", [])

        iterated_products = []
        for product in category:
            iterated_products.append(product)

        assert len(iterated_products) == 0

    def test_category_iterator_next_method(self):
        """Тест прямого использования next()."""
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
        ]
        category = Category("Категория", "Описание", products)

        iterator = iter(category)

        product1 = next(iterator)
        product2 = next(iterator)

        assert product1.name == "Товар1"
        assert product2.name == "Товар2"

        with pytest.raises(StopIteration):
            next(iterator)

    def test_category_iterator_multiple_iterations(self):
        """Тест нескольких итераций по одной категории."""
        products = [
            Product("Товар1", "Описание1", 100.0, 3),
            Product("Товар2", "Описание2", 200.0, 2),
        ]
        category = Category("Категория", "Описание", products)

        # Первая итерация
        first_iteration = [product.name for product in category]

        # Вторая итерация
        second_iteration = [product.name for product in category]

        assert first_iteration == second_iteration == ["Товар1", "Товар2"]


class TestIntegrationMagicMethods:
    """Интеграционные тесты магических методов."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_products_getter_integration_with_str(self):
        """Тест интеграции геттера products с __str__ Product."""
        products = [
            Product("Смартфон", "Описание", 50000.0, 10),
            Product("Ноутбук", "Описание", 80000.0, 5),
        ]
        category = Category("Электроника", "Техника", products)

        products_str = category.products

        # Проверяем форматирование через __str__ Product
        lines = products_str.split("\n")
        assert len(lines) == 2
        assert lines[0] == "Смартфон, 50000.0 руб. Остаток: 10 шт."
        assert lines[1] == "Ноутбук, 80000.0 руб. Остаток: 5 шт."

    def test_category_str_integration(self):
        """Тест интеграции __str__ Category с подсчетом количества."""
        products = [
            Product("Товар1", "Описание", 100.0, 10),
            Product("Товар2", "Описание", 200.0, 5),
            Product("Товар3", "Описание", 300.0, 3),
        ]
        category = Category("Категория", "Описание", products)

        category_str = str(category)

        # 10 + 5 + 3 = 18
        assert category_str == "Категория, количество продуктов: 18 шт."

    def test_complex_scenario_with_all_methods(self):
        """Тест сложного сценария со всеми магическими методами."""
        # Создаем товары
        phone = Product("Смартфон", "Флагман", 100000.0, 2)
        laptop = Product("Ноутбук", "Игровой", 150000.0, 1)
        tablet = Product("Планшет", "Графический", 50000.0, 3)

        # Создаем категорию
        electronics = Category("Электроника", "Техника", [phone, laptop])

        # Проверяем строковое представление категории
        assert str(electronics) == "Электроника, количество продуктов: 3 шт."  # 2+1=3

        # Проверяем сложение товаров
        total_value = phone + laptop
        assert total_value == 350000.0  # (100000*2) + (150000*1) = 350000

        # Добавляем еще товар
        electronics.add_product(tablet)

        # Проверяем обновленное строковое представление
        assert str(electronics) == "Электроника, количество продуктов: 6 шт."  # 2+1+3=6

        # Проверяем итерацию
        product_names = [product.name for product in electronics]
        assert product_names == ["Смартфон", "Ноутбук", "Планшет"]

        # Проверяем геттер products
        products_str = electronics.products
        assert "Смартфон, 100000.0 руб. Остаток: 2 шт." in products_str
        assert "Ноутбук, 150000.0 руб. Остаток: 1 шт." in products_str
        assert "Планшет, 50000.0 руб. Остаток: 3 шт." in products_str
