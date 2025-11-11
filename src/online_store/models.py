class Product:
    """
    Класс для представления товара в магазине.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
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

        Raises:
            ValueError: Если цена не положительная
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_data: dict) -> 'Product':
        """
        Класс-метод для создания нового товара из словаря.

        Args:
            product_data: Словарь с данными товара

        Returns:
            Product: Созданный объект товара
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price={self._price}, quantity={self.quantity})"

    def __str__(self) -> str:
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."


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

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в приватный список товаров категории.

        Args:
            product: Объект товара для добавления
        """
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
            products_info.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(products_info)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

    def __str__(self) -> str:
        return f"{self.name}, количество продуктов: {len(self.__products)}"
