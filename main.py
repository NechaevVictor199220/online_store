from src.online_store.json_loader import (
    get_categories_summary,
    load_categories_from_json,
)
from src.online_store.models import (
    Category,
    LawnGrass,
    Product,
    Smartphone,
    ZeroQuantityError,
)


def main():
    """Основная функция для демонстрации работы с новой функциональностью."""

    print("=== ДЕМОНСТРАЦИЯ ИСКЛЮЧЕНИЙ И СРЕДНЕЙ ЦЕНЫ ===")

    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    print("\n1. Создание товаров с корректным количеством:")
    try:
        product1 = Product("Товар А", "Описание", 100.0, 5)
        product2 = Product("Товар Б", "Описание", 200.0, 3)
        print("   ✓ Товары успешно созданы")
    except ZeroQuantityError as e:
        print(f"   ✗ Ошибка: {e}")

    print("\n2. Попытка создания товара с нулевым количеством:")
    try:
        Product(
            "Невалидный товар", "Описание", 50.0, 0
        )  # Убрана неиспользуемая переменная
        print("   ✓ Товар создан (не должно быть)")
    except ZeroQuantityError as e:
        print(f"   ✓ Ожидаемая ошибка: {e}")

    print("\n3. Создание категории и расчет средней цены:")
    category = Category("Тестовая категория", "Описание", [product1, product2])

    print(f"   Товары в категории: {len(category._Category__products)}")
    print(f"   Средняя цена: {category.average_price()} руб.")

    print("\n4. Добавление еще одного товара и пересчет средней цены:")
    product3 = Product("Товар В", "Описание", 300.0, 2)
    category.add_product(product3)

    print(f"   Товары в категории: {len(category._Category__products)}")
    print(f"   Новая средняя цена: {category.average_price()} руб.")

    print("\n5. Создание пустой категории:")
    empty_category = Category("Пустая категория", "Описание", [])
    print(f"   Средняя цена пустой категории: {empty_category.average_price()} руб.")

    print("\n6. Попытка добавления товара с нулевым количеством в категорию:")
    try:
        zero_product = Product("Товар с нулем", "Описание", 100.0, 5)
        zero_product.quantity = 0  # Меняем количество на 0
        category.add_product(zero_product)
        print("   ✓ Товар добавлен (не должно быть)")
    except ZeroQuantityError as e:
        print(f"   ✓ Ожидаемая ошибка: {e}")

    print("\n7. Итоговая статистика:")
    print(f"   Всего категорий: {Category.category_count}")
    print(f"   Всего товаров: {Category.product_count}")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ИЗ JSON ===")

    try:
        categories = load_categories_from_json("data/products.json")
        summary = get_categories_summary(categories)

        print(f"Успешно загружено категорий: {summary['total_categories']}")
        print(f"Общее количество товаров: {summary['total_products']}")

        print("\nСредние цены по категориям:")
        for category_name, avg_price in summary["average_prices"].items():
            print(f"   {category_name}: {avg_price:.2f} руб.")

        for category in categories:
            print(f"\nКатегория: {category.name}")
            print(f"Количество товаров: {len(category._Category__products)}")
            print(f"Средняя цена: {category.average_price():.2f} руб.")
            print("Товары:")
            print(category.products)

    except FileNotFoundError:
        print("Файл data/products.json не найден.")
    except ZeroQuantityError as e:
        print(f"Ошибка при загрузке данных: {e}")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    main()
