import pytest

from src.online_store.models import Category, LawnGrass, Product, Smartphone


class TestProductAddition:
    """Тесты для операции сложения товаров."""

    def test_add_same_product_types(self):
        """Тест сложения товаров одного типа."""
        product1 = Product("Товар", "Описание", 100.0, 5)
        product2 = Product("Товар", "Описание", 100.0, 3)

        result = product1 + product2

        assert result.name == "Товар"
        assert result.price == 100.0
        assert result.quantity == 8
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

        assert result.name == "iPhone"
        assert result.model == "15"
        assert result.quantity == 5
        assert isinstance(result, Smartphone)

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

        assert result.name == "Трава"
        assert result.country == "Россия"
        assert result.quantity == 25
        assert isinstance(result, LawnGrass)

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
            country="Россия",
            germination_period=12,
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


class TestCategoryValidation:
    """Тесты для валидации при добавлении в категорию."""

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
        assert "Смартфон (X)" in category.products

    def test_add_lawn_grass_to_category(self):
        """Тест добавления газонной травы в категорию."""
        category = Category("Сад", "Описание", [])
        lawn_grass = LawnGrass(
            name="Трава",
            description="Описание",
            price=2000.0,
            quantity=10,
            country="Россия",
            germination_period=12,
            color="Green",
        )

        category.add_product(lawn_grass)

        assert len(category._Category__products) == 1
        assert "Трава" in category.products

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
            category.add_product({"name": "товар"})

    def test_add_list_raises_error(self):
        """Тест, что добавление списка вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product(["товар"])

    def test_add_none_raises_error(self):
        """Тест, что добавление None вызывает ошибку."""
        category = Category("Категория", "Описание", [])

        with pytest.raises(
            TypeError,
            match="Можно добавлять только объекты класса Product или его наследников",
        ):
            category.add_product(None)


class TestMixedProducts:
    """Тесты для работы с разными типами товаров."""

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
            country="Россия",
            germination_period=12,
            color="Green",
        )

        category = Category("Разные товары", "Описание", [product])
        category.add_product(smartphone)
        category.add_product(lawn_grass)

        products_str = category.products
        assert "Обычный товар" in products_str
        assert "Смартфон (X)" in products_str
        assert "Трава" in products_str
        assert len(category._Category__products) == 3

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

        category = Category("Тест", "Описание", [product, smartphone])

        products_str = category.products
        assert "Товар, 100.0 руб. Остаток: 5 шт." in products_str
        assert (
            "Смартфон (Galaxy), 50000.0 руб. Остаток: 2 шт. Память: 128ГБ"
            in products_str
        )
