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

    def __str__(self) -> str:
        """
        Строковое представление товара.

        Returns:
            str: Строка в формате "Название, цена руб. Остаток: количество шт."
        """
        return f"{self.name}, {self._price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: 'Product') -> float:
        """
        Сложение товаров - возвращает общую стоимость всех товаров на складе.

        Args:
            other: Другой объект Product

        Returns:
            float: Сумма (цена * количество) для обоих товаров

        Raises:
            TypeError: Если other не является объектом Product
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self._price * self.quantity) + (other._price * other.quantity)

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

    def __str__(self) -> str:
        """
        Строковое представление категории.

        Returns:
            str: Строка в формате "Название категории, количество продуктов: X шт."
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

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
            products_info.append(str(product))  # Используем __str__ Product
        return "\n".join(products_info)

    def __repr__(self) -> str:
        return f"Category(name='{self.name}', products_count={len(self.__products)})"

    def __iter__(self):
        """
        Возвращает итератор для перебора товаров категории.

        Returns:
            CategoryIterator: Итератор товаров категории
        """
        return CategoryIterator(self.__products)


class CategoryIterator:
    """
    Итератор для перебора товаров категории.
    """

    def __init__(self, products: list):
        """
        Инициализация итератора.

        Args:
            products: Список товаров для итерации
        """
        self.products = products
        self.index = 0

    def __iter__(self):
        """Возвращает сам итератор."""
        return self

    def __next__(self) -> Product:
        """
        Возвращает следующий товар в итерации.

        Returns:
            Product: Следующий товар

        Raises:
            StopIteration: Когда товары закончились
        """
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
