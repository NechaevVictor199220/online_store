from src.online_store.models import Category, LawnGrass, Product, Smartphone


def main():
    """Основная функция для демонстрации работы с новой функциональностью."""

    print("=== ДЕМОНСТРАЦИЯ СЛОЖЕНИЯ ТОВАРОВ И ВАЛИДАЦИИ ===")

    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    print("\n1. Создание товаров для сложения:")
    product1 = Product("Товар А", "Описание", 100.0, 5)
    product2 = Product("Товар А", "Описание", 100.0, 3)

    print(f"   Товар 1: {product1}")
    print(f"   Товар 2: {product2}")

    print("\n2. Сложение товаров одного типа:")
    try:
        result = product1 + product2
        print(f"   Результат сложения: {result}")
    except TypeError as e:
        print(f"   Ошибка: {e}")

    print("\n3. Создание смартфонов для сложения:")
    smartphone1 = Smartphone(
        name="iPhone",
        description="Флагманский смартфон",
        price=150000.0,
        quantity=2,
        efficiency=4.5,
        model="15 Pro",
        memory=256,
        color="Black",
    )
    smartphone2 = Smartphone(
        name="iPhone",
        description="Флагманский смартфон",
        price=150000.0,
        quantity=3,
        efficiency=4.5,
        model="15 Pro",
        memory=256,
        color="Black",
    )

    print(f"   Смартфон 1: {smartphone1}")
    print(f"   Смартфон 2: {smartphone2}")

    print("\n4. Сложение смартфонов одного типа:")
    try:
        smartphone_result = smartphone1 + smartphone2
        print(f"   Результат сложения: {smartphone_result}")
    except TypeError as e:
        print(f"   Ошибка: {e}")

    print("\n5. Попытка сложения разных типов товаров:")
    try:
        invalid_result = product1 + smartphone1
        print(f"   Результат: {invalid_result}")
    except TypeError as e:
        print(f"   Ожидаемая ошибка: {e}")

    print("\n6. Валидация при добавлении в категорию:")
    category = Category("Тестовая категория", "Описание", [])

    print("   Добавление корректного товара:")
    category.add_product(product1)
    print("   ✓ Товар успешно добавлен")

    print("   Попытка добавления некорректного объекта:")
    try:
        category.add_product("не товар")
    except TypeError as e:
        print(f"   ✓ Ожидаемая ошибка: {e}")

    print("\n7. Итоговое состояние категории:")
    print(category.products)

    print("\n8. Статистика:")
    print(f"   Всего категорий: {Category.category_count}")
    print(f"   Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()
