import json
from typing import List, Any
from .models import Product, Category


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON файла и создает объекты классов.

    Поддерживает две структуры:
    1. Список категорий: [{"name": "...", "products": [...]}, ...]
    2. Объект с ключом 'categories': {"categories": [{...}, ...]}

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
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        categories = []

        # Сбрасываем счетчики перед загрузкой
        Category.category_count = 0
        Category.product_count = 0

        # Определяем структуру данных
        if isinstance(data, list):
            # Новая структура: список категорий
            categories_data = data
        elif isinstance(data, dict) and 'categories' in data:
            # Старая структура: объект с ключом 'categories'
            categories_data = data['categories']
        else:
            raise ValueError("Неподдерживаемая структура JSON файла")

        for category_data in categories_data:
            # Создаем продукты для категории
            products = []
            for product_data in category_data.get('products', []):
                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    quantity=product_data['quantity']
                )
                products.append(product)

            # Создаем категорию
            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                products=products
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка декодирования JSON: {e}", e.doc, e.pos)
    except KeyError as e:
        raise KeyError(f"Отсутствует обязательное поле в JSON: {e}")


def get_categories_summary(categories: List[Category]) -> dict:
    """
    Возвращает сводную информацию о загруженных категориях.

    Args:
        categories: Список объектов Category

    Returns:
        dict: Словарь со статистикой
    """
    total_categories = len(categories)
    total_products = sum(len(category.products) for category in categories)

    return {
        'total_categories': total_categories,
        'total_products': total_products,
        'categories': [
            {
                'name': category.name,
                'product_count': len(category.products)
            }
            for category in categories
        ]
    }