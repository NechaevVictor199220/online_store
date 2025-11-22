import json
from typing import List

from .models import Category, LawnGrass, Product, Smartphone


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON файла и создает объекты классов.

    Args:
        file_path: Путь к JSON файлу

    Returns:
        List[Category]: Список объектов Category

    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит некорректный JSON
        KeyError: Если в JSON отсутствуют обязательные поля
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        categories = []

        # Сбрасываем счетчики перед загрузкой
        Category.category_count = 0
        Category.product_count = 0

        # data - это уже список категорий
        for category_data in data:
            # Создаем продукты для категории
            products = []
            for product_data in category_data.get("products", []):
                # Определяем тип товара и создаем соответствующий объект
                product = create_product_from_data(product_data)
                products.append(product)

            # Создаем категорию
            category = Category(
                name=category_data["name"],
                description=category_data["description"],
                products=products,
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка декодирования JSON: {e}", e.doc, e.pos)
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательное поле в JSON: {e}")


def create_product_from_data(product_data: dict) -> Product:
    """
    Создает объект продукта на основе данных из JSON.

    Args:
        product_data: Словарь с данными товара

    Returns:
        Product: Созданный объект товара
    """
    # Определяем тип товара по наличию специфичных полей
    if "efficiency" in product_data and "model" in product_data:
        # Это смартфон
        return Smartphone(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
            efficiency=product_data["efficiency"],
            model=product_data["model"],
            memory=product_data["memory"],
            color=product_data["color"],
        )
    elif "country" in product_data and "germination_period" in product_data:
        # Это газонная трава
        return LawnGrass(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
            country=product_data["country"],
            germination_period=product_data["germination_period"],
            color=product_data["color"],
        )
    else:
        # Обычный товар
        return Product.new_product(product_data)


def get_categories_summary(categories: List[Category]) -> dict:
    """
    Возвращает сводную информацию о загруженных категориях.

    Args:
        categories: Список объектов Category

    Returns:
        dict: Словарь со статистикой
    """
    total_categories = len(categories)
    # Используем приватный атрибут для подсчета
    total_products = sum(len(category._Category__products) for category in categories)

    return {
        "total_categories": total_categories,
        "total_products": total_products,
        "categories": [
            {"name": category.name, "product_count": len(category._Category__products)}
            for category in categories
        ],
    }
