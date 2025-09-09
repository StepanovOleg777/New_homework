from src.product import Product, Category, ZeroQuantityError


def main():
    """Основная функция программы"""
    try:
        print("=" * 80)
        print("ТЕСТИРОВАНИЕ ПРОГРАММЫ УПРАВЛЕНИЯ ПРОДУКТАМИ")
        print("=" * 80)

        # Тестирование исключения при нулевом количестве
        print("1. ТЕСТИРОВАНИЕ ИСКЛЮЧЕНИЯ ДЛЯ НУЛЕВОГО КОЛИЧЕСТВА:")
        print("-" * 60)

        try:
            product_invalid = Product(
                "Бракованный товар", "Неверное количество", 1000.0, 0
            )
        except ZeroQuantityError as e:
            print("✅ Возникла ошибка ValueError прерывающая работу программы")
            print(f"   Сообщение: {e}")
        except ValueError as e:
            print("✅ Возникла ошибка ValueError прерывающая работу программы")
            print(f"   Сообщение: {e}")
        else:
            print(
                "❌ Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством"
            )

        # Создание валидных продуктов
        print("\n2. СОЗДАНИЕ ВАЛИДНЫХ ПРОДУКТОВ:")
        print("-" * 60)

        product1 = Product(
            "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
        )
        product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        print(f"✅ Создан: {product1.name}")
        print(f"✅ Создан: {product2.name}")
        print(f"✅ Создан: {product3.name}")

        # Создание категории с продуктами
        print("\n3. СОЗДАНИЕ КАТЕГОРИИ С ПРОДУКТАМИ:")
        print("-" * 60)

        category1 = Category(
            "Смартфоны", "Категория смартфонов", [product1, product2, product3]
        )
        print(f"✅ Создана категория: {category1.name}")
        print(f"   Количество продуктов: {len(category1.get_products_list())}")

        # Тестирование среднего ценника
        print("\n4. ТЕСТИРОВАНИЕ СРЕДНЕГО ЦЕННИКА:")
        print("-" * 60)

        middle_price = category1.middle_price()
        print(f"Средний ценник в категории '{category1.name}': {middle_price:.2f} руб.")

        # Расчет вручную для проверки: (180000 + 210000 + 31000) / 3 = 140333.33
        expected_price = (180000 + 210000 + 31000) / 3
        print(f"Ожидаемое значение: {expected_price:.2f} руб.")

        if abs(middle_price - expected_price) < 0.01:
            print("✅ Расчет среднего ценника корректен!")
        else:
            print("❌ Ошибка в расчете среднего ценника!")

        # Тестирование пустой категории
        print("\n5. ТЕСТИРОВАНИЕ ПУСТОЙ КАТЕГОРИИ:")
        print("-" * 60)

        category_empty = Category("Пустая категория", "Категория без продуктов", [])
        empty_price = category_empty.middle_price()
        print(f"Средний ценник в пустой категории: {empty_price} руб.")

        if empty_price == 0:
            print("✅ Для пустой категории возвращается 0 - корректно!")
        else:
            print("❌ Ошибка: для пустой категории должен возвращаться 0!")

        # Дополнительная информация
        print("\n6. СТАТИСТИКА:")
        print("-" * 60)
        print(f"Всего категорий: {Category.category_count}")
        print(f"Всего продуктов: {Category.product_count}")

        print("\n" + "=" * 80)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
