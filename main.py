from src.online_store.models import Product, Category
from src.online_store.json_loader import load_categories_from_json, get_categories_summary


def main():
    """Основная функция для демонстрации работы с JSON загрузчиком."""

    print("=== ДЕМОНСТРАЦИЯ РУЧНОГО СОЗДАНИЯ ===")
    # Сбрасываем счетчики для чистого теста
    Category.category_count = 0
    Category.product_count = 0

    # Ручное создание (оригинальный код)
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("Товар 1:")
    print(f"  Название: {product1.name}")
    print(f"  Описание: {product1.description}")
    print(f"  Цена: {product1.price}")
    print(f"  Количество: {product1.quantity}")

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(f"\nКатегория: {category1.name}")
    print(f"Проверка названия: {category1.name == 'Смартфоны'}")
    print(f"Описание: {category1.description}")
    print(f"Количество товаров в категории: {len(category1.products)}")
    print(f"Всего категорий (счетчик класса): {Category.category_count}")
    print(f"Всего товаров (счетчик класса): {Category.product_count}")

    print("\n=== ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ИЗ JSON ===")

    try:
        # Загрузка данных из JSON файла
        categories = load_categories_from_json("data/products.json")

        # Получаем сводную информацию
        summary = get_categories_summary(categories)

        print(f"Успешно загружено категорий: {summary['total_categories']}")
        print(f"Общее количество товаров: {summary['total_products']}")
        print(f"Счетчик категорий класса: {Category.category_count}")
        print(f"Счетчик товаров класса: {Category.product_count}")

        print("\nДетальная информация по категориям:")
        for i, category in enumerate(categories, 1):
            print(f"\n{i}. Категория: {category.name}")
            print(f"   Описание: {category.description}")
            print(f"   Количество товаров: {len(category.products)}")
            print("   Товары:")
            for j, product in enumerate(category.products, 1):
                print(f"     {j}. {product.name}")
                print(f"        Цена: {product.price} руб.")
                print(f"        В наличии: {product.quantity} шт.")
                print(f"        Описание: {product.description}")

    except FileNotFoundError:
        print("Файл data/products.json не найден. Создайте файл с данными.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")
        print("Убедитесь, что структура JSON файла правильная.")


if __name__ == "__main__":
    main()