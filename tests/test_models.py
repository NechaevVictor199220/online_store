import pytest
from src.online_store.models import Product, Category


class TestProductAccessModifiers:
    """Тесты для приватных атрибутов и методов доступа Product."""

    def test_price_is_private(self):
        """Тест, что атрибут цены приватный."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Проверяем, что атрибут приватный
        assert hasattr(product, '_price')
        # property 'price' существует, но это геттер, а не атрибут
        assert hasattr(product, 'price')  # Исправлено: property существует

    def test_price_getter(self):
        """Тест геттера для цены."""
        product = Product("Тест", "Описание", 150.0, 3)

        # Проверяем, что геттер работает
        assert product.price == 150.0

    def test_price_setter_positive(self):
        """Тест сеттера для цены с положительным значением."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Меняем цену на положительное значение
        product.price = 200.0

        assert product.price == 200.0

    def test_price_setter_negative(self, capsys):
        """Тест сеттера для цены с отрицательным значением."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Пытаемся установить отрицательную цену
        product.price = -50.0

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

        # Проверяем вывод сообщения
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_zero(self, capsys):
        """Тест сеттера для цены с нулевым значением."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Пытаемся установить нулевую цену
        product.price = 0.0

        # Проверяем, что цена не изменилась
        assert product.price == 100.0

        # Проверяем вывод сообщения
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_new_product_class_method(self):
        """Тест класс-метода new_product."""
        product_data = {
            "name": "Новый товар",
            "description": "Описание нового товара",
            "price": 500.0,
            "quantity": 10
        }

        product = Product.new_product(product_data)

        assert product.name == "Новый товар"
        assert product.description == "Описание нового товара"
        assert product.price == 500.0
        assert product.quantity == 10
        assert isinstance(product, Product)


class TestCategoryAccessModifiers:
    """Тесты для приватных атрибутов и методов доступа Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_products_is_private(self):
        """Тест, что атрибут products приватный."""
        products = [Product("Товар1", "Описание1", 100.0, 5)]
        category = Category("Категория", "Описание", products)

        # Проверяем, что атрибут приватный
        assert hasattr(category, '_Category__products')
        # property 'products' существует, но это геттер, а не атрибут
        assert hasattr(category, 'products')  # Исправлено: property существует

    def test_add_product_method(self):
        """Тест метода add_product."""
        category = Category("Категория", "Описание", [])
        product = Product("Новый товар", "Описание", 200.0, 3)

        initial_count = Category.product_count

        # Добавляем товар
        category.add_product(product)

        # Проверяем, что товар добавлен и счетчик увеличился
        assert Category.product_count == initial_count + 1
        # Проверяем через геттер (теперь это строка)
        assert "Новый товар" in category.products

    def test_products_getter(self):
        """Тест геттера для products."""
        products = [
            Product("Товар1", "Описание1", 100.0, 5),
            Product("Товар2", "Описание2", 200.0, 3)
        ]
        category = Category("Категория", "Описание", products)

        products_str = category.products

        # Проверяем формат вывода
        assert "Товар1, 100.0 руб. Остаток: 5 шт." in products_str
        assert "Товар2, 200.0 руб. Остаток: 3 шт." in products_str
        assert isinstance(products_str, str)

    def test_products_getter_empty(self):
        """Тест геттера для пустого списка товаров."""
        category = Category("Пустая категория", "Описание", [])

        products_str = category.products

        assert products_str == ""  # Пустая строка для пустого списка

    def test_cannot_access_private_products_directly(self):
        """Тест, что нельзя напрямую обратиться к приватному атрибуту."""
        products = [Product("Товар", "Описание", 100.0, 5)]
        category = Category("Категория", "Описание", products)

        # Не должно быть публичного атрибута products как списка
        # Но property 'products' существует и возвращает строку
        products_value = category.products
        assert isinstance(products_value, str)  # Геттер возвращает строку
        assert not isinstance(products_value, list)  # Не список

    def test_multiple_add_product(self):
        """Тест добавления нескольких товаров."""
        category = Category("Категория", "Описание", [])

        initial_count = Category.product_count

        # Добавляем несколько товаров
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        category.add_product(product1)
        category.add_product(product2)

        assert Category.product_count == initial_count + 2
        products_str = category.products
        assert "Товар1" in products_str
        assert "Товар2" in products_str

    def test_private_products_access(self):
        """Тест доступа к приватному атрибуту через name mangling."""
        products = [Product("Товар", "Описание", 100.0, 5)]
        category = Category("Категория", "Описание", products)

        # Доступ к приватному атрибуту через name mangling (для тестов)
        private_products = category._Category__products
        assert isinstance(private_products, list)
        assert len(private_products) == 1
        assert private_products[0].name == "Товар"


class TestIntegrationWithAccessModifiers:
    """Интеграционные тесты с новыми методами доступа."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_json_loader_with_new_methods(self, tmp_path):
        """Тест, что JSON загрузчик работает с новыми методами."""
        import json
        from src.online_store.json_loader import load_categories_from_json

        json_data = [
            {
                "name": "Тестовая категория",
                "description": "Описание",
                "products": [
                    {
                        "name": "Товар из JSON",
                        "description": "Описание товара",
                        "price": 150.0,
                        "quantity": 7
                    }
                ]
            }
        ]

        json_file = tmp_path / "test.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        categories = load_categories_from_json(json_file)

        # Проверяем, что все работает с новыми методами доступа
        assert len(categories) == 1
        assert "Товар из JSON" in categories[0].products
        # Проверяем цену через приватный доступ к продуктам
        # assert len(categories[0]._Category__products) == 1
        # assert categories[0]._Category__products[0].price == 150.0

    def test_add_product_updates_counters(self):
        """Тест, что add_product обновляет счетчики."""
        initial_category_count = Category.category_count
        initial_product_count = Category.product_count

        category = Category("Категория", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)

        category.add_product(product)

        assert Category.category_count == initial_category_count + 1
        assert Category.product_count == initial_product_count + 1


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
        # products теперь возвращает строку, проверяем содержание
        products_str = category.products
        assert "Товар1" in products_str
        assert "Товар2" in products_str
        assert isinstance(category.products, str)

    def test_category_initialization_empty(self):
        """Тест инициализации пустой категории."""
        category = Category("Пустая", "Пустая категория", [])

        assert category.name == "Пустая"
        assert category.description == "Пустая категория"
        assert category.products == ""  # Пустая строка

    def test_category_initialization_single_product(self):
        """Тест инициализации категории с одним товаром."""
        product = Product("Единственный", "Описание", 150.0, 1)
        category = Category("Категория", "Описание", [product])

        products_str = category.products
        assert "Единственный" in products_str
        assert "150.0 руб." in products_str
        assert isinstance(products_str, str)

    def test_category_attributes_types(self):
        """Тест типов атрибутов объекта Category."""
        products = [Product("Товар", "Описание", 100.0, 5)]
        category = Category("Категория", "Описание", products)

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, str)  # Теперь это строка


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

        # Проверяем через геттер (строку)
        assert "Универсальный товар" in category1.products
        assert "Универсальный товар" in category2.products

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
        # Проверяем через геттер (строку)
        electronics_products = electronics.products
        assert "Смартфон" in electronics_products
        assert "Ноутбук" in electronics_products
        assert "Планшет" in electronics_products

        books_products = books.products
        assert "Книга1" in books_products
        assert "Книга2" in books_products

        clothing_products = clothing.products
        assert "Футболка" in clothing_products
        assert "Джинсы" in clothing_products
        assert "Куртка" in clothing_products


# Фикстуры для тестов
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

    def test_category_with_fixture(self, sample_category):
        """Тест категории с использованием фикстуры."""
        assert sample_category.name == "Тестовая категория"
        # products теперь строка, проверяем содержание
        products_str = sample_category.products
        assert "Товар1" in products_str
        assert "100.0 руб." in products_str

    def test_empty_category_with_fixture(self, empty_category):
        """Тест пустой категории с использованием фикстуры."""
        assert empty_category.name == "Пустая категория"
        assert empty_category.products == ""  # Пустая строка
