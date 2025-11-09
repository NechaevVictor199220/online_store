import pytest
from src.online_store.models import Product, Category


class TestProductInitialization:
    """Тесты для проверки корректности инициализации объектов класса Product."""

    def test_product_initialization_basic(self):
        """Тест базовой инициализации продукта."""
        product = Product(
            name="Телефон",
            description="Смартфон",
            price=50000.0,
            quantity=10
        )

        assert product.name == "Телефон"
        assert product.description == "Смартфон"
        assert product.price == 50000.0
        assert product.quantity == 10

    def test_product_initialization_with_special_characters(self):
        """Тест инициализации продукта со специальными символами в названии."""
        product = Product(
            name="iPhone 15 Pro Max",
            description="Смартфон 256GB, Space Black",
            price=150000.99,
            quantity=3
        )

        assert product.name == "iPhone 15 Pro Max"
        assert product.description == "Смартфон 256GB, Space Black"
        assert product.price == 150000.99
        assert product.quantity == 3

    def test_product_initialization_zero_quantity(self):
        """Тест инициализации продукта с нулевым количеством."""
        product = Product("Товар", "Описание", 1000.0, 0)

        assert product.quantity == 0
        assert product.name == "Товар"

    def test_product_initialization_high_price(self):
        """Тест инициализации продукта с высокой ценой."""
        product = Product("Дорогой товар", "Люкс", 999999.99, 1)

        assert product.price == 999999.99
        assert product.quantity == 1

    def test_product_attributes_types(self):
        """Тест типов атрибутов объекта Product."""
        product = Product("Тест", "Описание", 100.50, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_product_initialization_multiple_products(self):
        """Тест создания нескольких продуктов с разными данными."""
        products = [
            Product("Товар1", "Описание1", 100.0, 10),
            Product("Товар2", "Описание2", 200.0, 20),
            Product("Товар3", "Описание3", 300.0, 30)
        ]

        for i, product in enumerate(products, 1):
            assert product.name == f"Товар{i}"
            assert product.description == f"Описание{i}"
            assert product.price == i * 100.0
            assert product.quantity == i * 10


class TestCategoryInitialization:
    """Тесты для проверки корректности инициализации объектов класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_initialization_basic(self):
        """Тест базовой инициализации категории."""
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]

        category = Category(
            name="Электроника",
            description="Электронные товары",
            products=products
        )

        assert category.name == "Электроника"
        assert category.description == "Электронные товары"
        assert len(category.products) == 2
        assert isinstance(category.products[0], Product)
        assert isinstance(category.products[1], Product)

    def test_category_initialization_empty(self):
        """Тест инициализации пустой категории."""
        category = Category("Пустая", "Пустая категория", [])

        assert category.name == "Пустая"
        assert category.description == "Пустая категория"
        assert category.products == []

    def test_category_initialization_single_product(self):
        """Тест инициализации категории с одним товаром."""
        product = Product("Единственный", "Описание", 150.0, 1)
        category = Category("Категория", "Описание", [product])

        assert len(category.products) == 1
        assert category.products[0].name == "Единственный"
        assert category.products[0].quantity == 1

    def test_category_initialization_with_special_characters(self):
        """Тест инициализации категории со специальными символами."""
        products = [Product("Товар", "Описание", 100.0, 5)]
        category = Category(
            name="Электроника & Гаджеты",
            description="Категория с & символами!",
            products=products
        )

        assert category.name == "Электроника & Гаджеты"
        assert category.description == "Категория с & символами!"

    def test_category_attributes_types(self):
        """Тест типов атрибутов объекта Category."""
        products = [Product("Товар", "Описание", 100.0, 5)]
        category = Category("Категория", "Описание", products)

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, list)
        assert all(isinstance(product, Product) for product in category.products)


class TestProductCount:
    """Тесты для проверки подсчета количества продуктов."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_product_count_empty_categories(self):
        """Тест подсчета продуктов при пустых категориях."""
        Category("Кат1", "Описание1", [])
        Category("Кат2", "Описание2", [])
        Category("Кат3", "Описание3", [])

        assert Category.product_count == 0

    def test_product_count_single_category(self):
        """Тест подсчета продуктов в одной категории."""
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3),
            Product("Товар3", "Описание3", 300.0, 7)
        ]

        Category("Категория", "Описание", products)

        assert Category.product_count == 3

    def test_product_count_multiple_categories(self):
        """Тест подсчета продуктов в нескольких категориях."""
        products1 = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]

        products2 = [
            Product("Товар3", "Описание3", 300.0, 2)
        ]

        products3 = [
            Product("Товар4", "Описание4", 400.0, 1),
            Product("Товар5", "Описание5", 500.0, 4),
            Product("Товар6", "Описание6", 600.0, 2)
        ]

        Category("Кат1", "Описание1", products1)  # +2 продукта
        Category("Кат2", "Описание2", products2)  # +1 продукт
        Category("Кат3", "Описание3", products3)  # +3 продукта

        assert Category.product_count == 6

    def test_product_count_mixed_categories(self):
        """Тест подсчета продуктов в смешанных категориях (пустые и не пустые)."""
        Category("Пустая1", "Описание", [])  # 0 продуктов

        products1 = [Product("Товар1", "Описание", 100.0, 5)]  # 1 продукт
        Category("Непустая1", "Описание", products1)

        Category("Пустая2", "Описание", [])  # 0 продуктов

        products2 = [
            Product("Товар2", "Описание", 200.0, 3),
            Product("Товар3", "Описание", 300.0, 2)
        ]  # 2 продукта
        Category("Непустая2", "Описание", products2)

        assert Category.product_count == 3

    def test_product_count_access_via_instance(self):
        """Тест доступа к счетчику продуктов через экземпляр."""
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]

        category = Category("Категория", "Описание", products)

        # Проверяем, что счетчик доступен через экземпляр
        assert category.product_count == 2
        assert Category.product_count == 2


class TestCategoryCount:
    """Тесты для проверки подсчета количества категорий."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_count_empty(self):
        """Тест подсчета категорий при отсутствии категорий."""
        assert Category.category_count == 0

    def test_category_count_single(self):
        """Тест подсчета одной категории."""
        Category("Категория", "Описание", [])

        assert Category.category_count == 1

    def test_category_count_multiple(self):
        """Тест подсчета нескольких категорий."""
        Category("Кат1", "Описание1", [])
        Category("Кат2", "Описание2", [])
        Category("Кат3", "Описание3", [])
        Category("Кат4", "Описание4", [])

        assert Category.category_count == 4

    def test_category_count_incremental(self):
        """Тест постепенного увеличения счетчика категорий."""
        assert Category.category_count == 0

        Category("Кат1", "Описание1", [])
        assert Category.category_count == 1

        Category("Кат2", "Описание2", [])
        assert Category.category_count == 2

        Category("Кат3", "Описание3", [])
        assert Category.category_count == 3

    def test_category_count_access_via_instance(self):
        """Тест доступа к счетчику категорий через экземпляр."""
        category1 = Category("Кат1", "Описание1", [])

        # Проверяем, что счетчик доступен через экземпляр
        assert category1.category_count == 1

        category2 = Category("Кат2", "Описание2", [])

        # Оба экземпляра должны видеть одинаковое значение
        assert category1.category_count == 2
        assert category2.category_count == 2
        assert Category.category_count == 2


class TestIntegration:
    """Интеграционные тесты для совместной работы Product и Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_product_in_multiple_categories(self):
        """Тест, когда один продукт находится в нескольких категориях."""
        product = Product("Универсальный товар", "Описание", 100.0, 5)

        # Один продукт в двух категориях
        category1 = Category("Кат1", "Описание1", [product])
        category2 = Category("Кат2", "Описание2", [product])

        # Проверяем счетчики
        assert Category.category_count == 2
        assert Category.product_count == 2  # Продукт учтен дважды!

    def test_complex_scenario(self):
        """Тест сложного сценария с множеством категорий и продуктов."""
        # Создаем продукты
        products_electronics = [
            Product("Смартфон", "Описание", 50000.0, 10),
            Product("Ноутбук", "Описание", 80000.0, 5),
            Product("Планшет", "Описание", 30000.0, 8)
        ]

        products_books = [
            Product("Книга1", "Описание", 500.0, 20),
            Product("Книга2", "Описание", 700.0, 15)
        ]

        products_clothing = [
            Product("Футболка", "Описание", 1000.0, 50),
            Product("Джинсы", "Описание", 3000.0, 30),
            Product("Куртка", "Описание", 5000.0, 10)
        ]

        # Создаем категории
        electronics = Category("Электроника", "Техника", products_electronics)
        books = Category("Книги", "Литература", products_books)
        clothing = Category("Одежда", "Модная одежда", products_clothing)

        # Проверяем итоговые счетчики
        assert Category.category_count == 3
        assert Category.product_count == 8  # 3 + 2 + 3 = 8

        # Проверяем доступность через экземпляры
        assert electronics.category_count == 3
        assert electronics.product_count == 8

        assert books.category_count == 3
        assert books.product_count == 8

        assert clothing.category_count == 3
        assert clothing.product_count == 8


# Фикстуры для pytest
@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта."""
    return Product("Тестовый товар", "Тестовое описание", 1000.0, 5)


@pytest.fixture
def sample_category():
    """Фикстура для создания тестовой категории."""
    Category.category_count = 0
    Category.product_count = 0
    products = [Product("Товар1", "Описание1", 100.0, 5)]
    return Category("Тестовая категория", "Тестовое описание", products)


@pytest.fixture
def empty_category():
    """Фикстура для создания пустой категории."""
    Category.category_count = 0
    Category.product_count = 0
    return Category("Пустая категория", "Описание", [])


class TestWithFixtures:
    """Тесты с использованием фикстур."""

    def test_product_with_fixture(self, sample_product):
        """Тест продукта с использованием фикстуры."""
        assert sample_product.name == "Тестовый товар"
        assert sample_product.price == 1000.0
        assert sample_product.quantity == 5

    def test_category_with_fixture(self, sample_category):
        """Тест категории с использованием фикстуры."""
        assert sample_category.name == "Тестовая категория"
        assert len(sample_category.products) == 1
        assert Category.category_count == 1
        assert Category.product_count == 1

    def test_empty_category_with_fixture(self, empty_category):
        """Тест пустой категории с использованием фикстуры."""
        assert empty_category.name == "Пустая категория"
        assert empty_category.products == []
        assert Category.category_count == 1
        assert Category.product_count == 0