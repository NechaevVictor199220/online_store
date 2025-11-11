from src.online_store.models import Product, Category
from src.online_store.json_loader import load_categories_from_json, get_categories_summary


def main():
    """Основная функция для демонстрации работы с новой функциональностью."""

    print("=== ДЕМОНСТРАЦИЯ НОВОЙ ФУНКЦИОНАЛЬНОСТИ ===")

    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    print("\n1. Создание товаров с приватной ценой:")
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    print(f"   Товар создан: {product1.name}")
    print(f"   Цена через геттер: {product1.price} руб.")

    print("\n2. Попытка установить отрицательную цену:")
    product1.price = -1000.0  # Должно вывести сообщение об ошибке
    print(f"   Цена после попытки установить отрицательную: {product1.price} руб.")

    print("\n3. Установка корректной цены:")
    product1.price = 190000.0
    print(f"   Новая цена: {product1.price} руб.")

    print("\n4. Создание категории с приватным списком товаров:")
    category1 = Category("Смартфоны", "Современные смартфоны", [])
    print(f"   Категория создана: {category1.name}")

    print("\n5. Добавление товаров через add_product():")
    category1.add_product(product1)
    product2 = Product("iPhone 15", "512GB, Gray space", 210000.0, 8)
    category1.add_product(product2)
    print(f"   Товары добавлены в категорию")

    print("\n6. Вывод товаров через геттер:")
    print(category1.products)

    print("\n7. Использование класс-метода new_product():")
    product_data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14
    }
    product3 = Product.new_product(product_data)
    category1.add_product(product3)
    print(f"   Товар создан класс-методом: {product3.name}")

    print("\n8. Итоговый список товаров в категории:")
    print(category1.products)

    print(f"\n9. Статистика:")
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
