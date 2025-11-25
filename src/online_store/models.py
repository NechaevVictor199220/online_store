class Product:
    """
    Базовый класс для представления товара в магазине.
    """

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """
        Инициализация объекта Product.

        Args:
            name: Название товара
            description: Описание товара
            price: Цена товара
            quantity: Количество товара в наличии
        """
        self.name = name
        self.description = description
        self._price = price  # Приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены товара."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Сеттер для цены товара с проверкой на положительное значение.

        Args:
            new_price: Новая цена товара
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """
        Класс-метод для создания нового товара из словаря.

        Args:
            product_data: Словарь с данными товара

        Returns:
            Product: Созданный объект товара
        """
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __add__(self, other):
        """
        Сложение товаров одного типа.

        Args:
            other: Другой товар для сложения

        Returns:
            Product: Новый товар с суммой количеств

        Raises:
            TypeError: Если товары разных типов
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

        total_quantity = self.quantity + other.quantity

        # Для базового класса Product
        if isinstance(self, Product) and not isinstance(self, (Smartphone, LawnGrass)):
            return Product(
                name=self.name,
                description=self.description,
                price=self.price,
                quantity=total_quantity,
            )

        # Для классов-наследников нужно переопределить этот метод
        raise NotImplementedError(
            f"Метод __add__ не реализован для класса {type(self).__name__}"
        )

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self._price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."


class Smartphone(Product):
    """
    Класс для представления смартфона.
    Наследуется от класса Product.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """
        Инициализация объекта Smartphone.

        Args:
            name: Название смартфона
            description: Описание смартфона
            price: Цена смартфона
            quantity: Количество в наличии
            efficiency: Производительность
            model: Модель смартфона
            memory: Объем встроенной памяти (ГБ)
            color: Цвет смартфона
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other):
        """
        Сложение смартфонов одного типа.

        Args:
            other: Другой смартфон для сложения

        Returns:
            Smartphone: Новый смартфон с суммой количеств

        Raises:
            TypeError: Если смартфоны разных типов
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

        total_quantity = self.quantity + other.quantity

        return Smartphone(
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=total_quantity,
            efficiency=self.efficiency,
            model=self.model,
            memory=self.memory,
            color=self.color,
        )

    def __repr__(self) -> str:
        return (
            f"Smartphone(name='{self.name}', model='{self.model}', "
            f"price={self._price}, quantity={self.quantity})"
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.model}), {self._price} руб. "
            f"Остаток: {self.quantity} шт. Память: {self.memory}ГБ"
        )


class LawnGrass(Product):
    """
    Класс для представления газонной травы.
    Наследуется от класса Product.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ) -> None:
        """
        Инициализация объекта LawnGrass.

        Args:
            name: Название травы
            description: Описание травы
            price: Цена травы
            quantity: Количество в наличии
            country: Страна-производитель
            germination_period: Срок прорастания (дни)
            color: Цвет травы
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other):
        """
        Сложение газонной травы одного типа.

        Args:
            other: Другая газонная трава для сложения

        Returns:
            LawnGrass: Новая газонная трава с суммой количеств

        Raises:
            TypeError: Если газонная трава разных типов
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")

        total_quantity = self.quantity + other.quantity

        return LawnGrass(
            name=self.name,
            description=self.description,
            price=self.price,
            quantity=total_quantity,
            country=self.country,
            germination_period=self.germination_period,
            color=self.color,
        )

    def __repr__(self) -> str:
        return (
            f"LawnGrass(name='{self.name}', country='{self.country}', "
            f"price={self._price}, quantity={self.quantity})"
        )

    def __str__(self) -> str:
        return (
            f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт. "
            f"Страна: {self.country}"
        )


class Category:
    """
    Класс для представления категории товаров.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        """
        Инициализация объекта Category.

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров категории
        """
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут списка товаров

        # Обновляем атрибуты класса
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product) -> None:
        """
        Добавляет товар в приватный список товаров категории.

        Args:
            product: Объект товара для добавления

        Raises:
            TypeError: Если переданный объект не является товаром
        """
        # Проверяем, что объект является товаром или наследником Product
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1  # Увеличиваем счетчик товаров

    @property
    def products(self) -> str:
        """
        Геттер для получения строкового представления товаров категории.

        Returns:
            str: Строка с информацией о всех товарах категории
        """
        products_info = []
        for product in self.__products:
            products_info.append(str(product))
        return "\n".join(products_info)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {len(self.__products)}"
