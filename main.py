from src.online_store.json_loader import (
    get_categories_summary,
    load_categories_from_json,
)
from src.online_store.models import Category, LawnGrass, Product, Smartphone


def main():
    """Основная функция для демонстрации работы с новой функциональностью."""

    print("=== ДЕМОНСТРАЦИЯ НАСЛЕДОВАНИЯ И ОГРАНИЧЕНИЙ ===")

    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    print("\n1. Создание разных типов товаров:")

    # Обычный товар
    product = Product("Обычный товар", "Просто товар", 500.0, 10)
    print(f"   Обычный товар: {product}")

    # Смартфон
    smartphone = Smartphone(
        name="iPhone 15 Pro",
        description="Флагманский смартфон",
        price=150000.0,
        quantity=5,
        efficiency=4.8,
        model="15 Pro Max",
        memory=512,
        color="Titanium",
    )
    print(f"   Смартфон: {smartphone}")

    # Газонная трава
    lawn_grass = LawnGrass(
        name="Газонная трава Премиум",
        description="Высококачественная газонная трава",
        price=7500.0,
        quantity=100,
        country="Германия",
        germination_period=12,
        color="Изумрудный",
    )
    print(f"   Газонная трава: {lawn_grass}")

    print("\n2. Проверка наследования:")
    print(f"   Smartphone является Product: {isinstance(smartphone, Product)}")
    print(f"   LawnGrass является Product: {isinstance(lawn_grass, Product)}")

    print("\n3. Сложение товаров одного типа:")
    try:
        smartphone2 = Smartphone(
            name="iPhone 15 Pro",
            description="Флагманский смартфон",
            price=150000.0,
            quantity=3,
            efficiency=4.8,
            model="15 Pro Max",
            memory=512,
            color="Titanium",
        )
        total_smartphones = smartphone + smartphone2
        print(f"   Сложение смартфонов: {total_smartphones.quantity} шт.")
    except TypeError as e:
        print(f"   Ошибка: {e}")

    print("\n4. Попытка сложения разных типов товаров:")
    try:
        invalid_sum = smartphone + lawn_grass
        print(f"   Результат: {invalid_sum}")
    except TypeError as e:
        print(f"   Ошибка (ожидаемо): {e}")

    print("\n5. Добавление товаров в категорию:")
    electronics_category = Category("Электроника", "Техника и гаджеты", [])

    # Добавляем смартфон
    electronics_category.add_product(smartphone)
    print("   Смартфон добавлен в категорию")

    # Попытка добавить не-товар
    try:
        electronics_category.add_product("не товар")
        print("   Не-товар добавлен (не должно быть)")
    except TypeError as e:
        print(f"   Ошибка при добавлении не-товара (ожидаемо): {e}")

    print("\n6. Товары в категории:")
    print(electronics_category.products)

    print("\n7. Статистика:")
    print(f"   Всего категорий: {Category.category_count}")
    print(f"   Всего товаров: {Category.product_count}")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ИЗ JSON ===")

    try:
        categories = load_categories_from_json("data/products.json")
        summary = get_categories_summary(categories)

        print(f"Успешно загружено категорий: {summary['total_categories']}")
        print(f"Общее количество товаров: {summary['total_products']}")

        for category in categories:
            print(f"\nКатегория: {category.name}")
            print("Товары:")
            print(category.products)

    except FileNotFoundError:
        print("Файл data/products.json не найден.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    main()
