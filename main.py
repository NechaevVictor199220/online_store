from src.online_store.models import Product, Category
from src.online_store.json_loader import load_categories_from_json, get_categories_summary


def main():
    """Основная функция для демонстрации работы с новой функциональностью."""

    print("=== ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ ===")

    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    print("\n1. Создание товаров:")
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(f"   Товар 1: {product1}")  # Используется __str__
    print(f"   Товар 2: {product2}")
    print(f"   Товар 3: {product3}")

    print("\n2. Сложение товаров (общая стоимость на складе):")
    total_value_1_2 = product1 + product2
    total_value_2_3 = product2 + product3
    print(f"   {product1.name} + {product2.name} = {total_value_1_2} руб.")
    print(f"   {product2.name} + {product3.name} = {total_value_2_3} руб.")

    print("\n3. Создание категории:")
    category1 = Category("Смартфоны", "Современные смартфоны", [product1, product2, product3])
    print(f"   Категория: {category1}")  # Используется __str__ Category

    print("\n4. Итерация по товарам категории:")
    print("   Товары в категории:")
    for i, product in enumerate(category1, 1):
        print(f"   {i}. {product}")

    print("\n5. Добавление нового товара:")
    product4 = Product("Google Pixel 8", "128GB, Черный", 75000.0, 3)
    category1.add_product(product4)
    print(f"   Добавлен: {product4}")
    print(f"   Обновленная категория: {category1}")

    print("\n6. Вывод товаров через геттер:")
    print(category1.products)

    print(f"\n7. Статистика:")
    print(f"   Всего категорий: {Category.category_count}")
    print(f"   Всего товаров: {Category.product_count}")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ИЗ JSON ===")

    try:
        categories = load_categories_from_json("data/products.json")
        summary = get_categories_summary(categories)

        print(f"Успешно загружено категорий: {summary['total_categories']}")
        print(f"Общее количество товаров: {summary['total_products']}")

        for category in categories:
            print(f"\nКатегория: {category}")
            print("Товары:")
            for product in category:
                print(f"  - {product}")

    except FileNotFoundError:
        print("Файл data/products.json не найден.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    main()