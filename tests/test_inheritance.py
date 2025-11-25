import pytest

from src.online_store.models import Category, LawnGrass, Product, Smartphone


class TestInheritance:
    """Тесты для классов-наследников."""

    def test_smartphone_inheritance(self):
        """Тест, что Smartphone наследуется от Product."""
        smartphone = Smartphone(
            name="iPhone 15",
            description="Флагманский смартфон",
            price=150000.0,
            quantity=10,
            efficiency=4.5,
            model="15 Pro",
            memory=256,
            color="Black",
        )

        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, Smartphone)
        assert smartphone.name == "iPhone 15"
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_lawn_grass_inheritance(self):
        """Тест, что LawnGrass наследуется от Product."""
        lawn_grass = LawnGrass(
            name="Газонная трава Премиум",
            description="Качественная газонная трава",
            price=5000.0,
            quantity=100,
            country="Германия",
            germination_period=14,
            color="Зеленый",
        )

        assert isinstance(lawn_grass, Product)
        assert isinstance(lawn_grass, LawnGrass)
        assert lawn_grass.name == "Газонная трава Премиум"
        assert lawn_grass.country == "Германия"
        assert lawn_grass.germination_period == 14
        assert lawn_grass.color == "Зеленый"

    def test_smartphone_additional_attributes(self):
        """Тест дополнительных атрибутов Smartphone."""
        smartphone = Smartphone(
            name="Samsung Galaxy",
            description="Android смартфон",
            price=80000.0,
            quantity=5,
            efficiency=3.8,
            model="S23 Ultra",
            memory=512,
            color="Gray",
        )

        assert smartphone.efficiency == 3.8
        assert smartphone.model == "S23 Ultra"
        assert smartphone.memory == 512
        assert smartphone.color == "Gray"
        # Проверяем наследование базовых атрибутов
        assert smartphone.price == 80000.0
        assert smartphone.quantity == 5

    def test_lawn_grass_additional_attributes(self):
        """Тест дополнительных атрибутов LawnGrass."""
        lawn_grass = LawnGrass(
            name="Трава Спорт",
            description="Для спортивных площадок",
            price=3000.0,
            quantity=50,
            country="Россия",
            germination_period=10,
            color="Темно-зеленый",
        )

        assert lawn_grass.country == "Россия"
        assert lawn_grass.germination_period == 10
        assert lawn_grass.color == "Темно-зеленый"
        # Проверяем наследование базовых атрибутов
        assert lawn_grass.price == 3000.0
        assert lawn_grass.quantity == 50


class TestAdditionRestrictions:
    """Тесты для ограничений сложения."""

    def test_add_same_product_types(self):
        """Тест сложения товаров одного типа."""
        product1 = Product("Товар", "Описание", 100.0, 5)
        product2 = Product("Товар", "Описание", 100.0, 3)

        result = product1 + product2

        assert result.quantity == 8
        assert result.name == "Товар"
        assert isinstance(result, Product)

    def test_add_same_smartphone_types(self):
        """Тест сложения смартфонов одного типа."""
        smartphone1 = Smartphone(
            name="iPhone",
            description="Описание",
            price=100000.0,
            quantity=2,
            efficiency=4.0,
            model="15",
            memory=128,
            color="Black",
        )
        smartphone2 = Smartphone(
            name="iPhone",
            description="Описание",
            price=100000.0,
            quantity=3,
            efficiency=4.0,
            model="15",
            memory=128,
            color="Black",
        )

        result = smartphone1 + smartphone2

        assert result.quantity == 5
        assert isinstance(result, Smartphone)
        assert result.model == "15"

    def test_add_same_lawn_grass_types(self):
        """Тест сложения газонной травы одного типа."""
        grass1 = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Россия",
            germination_period=12,
            color="Green",
        )
        grass2 = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=15,
            country="Россия",
            germination_period=12,
            color="Green",
        )

        result = grass1 + grass2

        assert result.quantity == 25
        assert isinstance(result, LawnGrass)
        assert result.country == "Россия"

    def test_add_different_product_types_raises_error(self):
        """Тест, что сложение разных типов товаров вызывает ошибку."""
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="X",
            memory=64,
            color="White",
        )

        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            product + smartphone

    def test_add_smartphone_and_lawn_grass_raises_error(self):
        """Тест, что сложение смартфона и газонной травы вызывает ошибку."""
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="X",
            memory=64,
            color="White",
        )
        lawn_grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Германия",
            germination_period=14,
            color="Green",
        )

        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            smartphone + lawn_grass

    def test_add_product_with_smartphone_raises_error(self):
        """Тест, что сложение Product и Smartphone вызывает ошибку."""
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="X",
            memory=64,
            color="White",
        )

        with pytest.raises(TypeError, match="Нельзя складывать товары разных типов"):
            product + smartphone


class TestAddProductRestrictions:
    """Тесты для ограничений добавления товаров в категорию."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_add_product_to_category(self):
        """Тест добавления обычного товара в категорию."""
        category = Category("Категория", "Описание", [])
        product = Product("Товар", "Описание", 100.0, 5)

        category.add_product(product)

        assert len(category._Category__products) == 1
        assert Category.product_count == 1

    def test_add_smartphone_to_category(self):
        """Тест добавления смартфона в категорию."""
        category = Category("Электроника", "Описание", [])
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="X",
            memory=64,
            color="White",
        )

        category.add_product(smartphone)

        assert len(category._Category__products) == 1
        assert Category.product_count == 1

    def test_add_lawn_grass_to_category(self):
        """Тест добавления газонной травы в категорию."""
        category = Category("Сад", "Описание", [])
        lawn_grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Германия",
            germination_period=14,
            color="Green",
        )

        category.add_product(lawn_grass)

        assert len(category._Category__products) == 1
        assert Category.product_count == 1

    def test_add_non_product_raises_error(self):
        """Тест, что добавление не-товара вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product("не товар")

    def test_add_dict_raises_error(self):
        """Тест, что добавление словаря вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product({"name": "не товар"})

    def test_add_list_raises_error(self):
        """Тест, что добавление списка вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product([1, 2, 3])

    def test_add_none_raises_error(self):
        """Тест, что добавление None вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product(None)


class TestMixedProducts:
    """Тесты для смешанных сценариев с разными типами товаров."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.category_count = 0
        Category.product_count = 0

    def test_category_with_mixed_products(self):
        """Тест категории с разными типами товаров."""
        product = Product("Обычный товар", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Смартфон",
            description="Описание",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="X",
            memory=64,
            color="White",
        )
        lawn_grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Германия",
            germination_period=14,
            color="Green",
        )

        category = Category(
            "Разные товары", "Описание", [product, smartphone, lawn_grass]
        )

        assert len(category._Category__products) == 3
        assert Category.product_count == 3

        # Проверяем, что все товары сохранили свои типы
        assert isinstance(category._Category__products[0], Product)
        assert isinstance(category._Category__products[1], Smartphone)
        assert isinstance(category._Category__products[2], LawnGrass)

    def test_products_getter_with_mixed_types(self):
        """Тест геттера products с разными типами товаров."""
        product = Product("Товар", "Описание", 100.0, 5)
        smartphone = Smartphone(
            name="Смартфон",
            description="Android",
            price=50000.0,
            quantity=2,
            efficiency=3.5,
            model="Galaxy",
            memory=128,
            color="Black",
        )

        category = Category("Категория", "Описание", [product, smartphone])
        products_str = category.products

        assert "Товар" in products_str
        assert "Смартфон" in products_str
        assert "Galaxy" in products_str
