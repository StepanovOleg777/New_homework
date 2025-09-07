from abc import ABC, abstractmethod


class ZeroQuantityError(Exception):
    """Пользовательское исключение для товаров с нулевым количеством"""

    pass


class LoggingMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        # Не вызываем super() здесь, чтобы избежать конфликта с абстрактным классом
        class_name = self.__class__.__name__
        print(f"Создан объект {class_name} с параметрами: {self.__repr__()}")

    def __repr__(self):
        """Базовое представление объекта"""
        if hasattr(self, "name"):
            return f"{self.__class__.__name__}(name={repr(self.name)})"
        return f"{self.__class__.__name__}()"


class BaseProduct(ABC):
    """Абстрактный базовый класс для продуктов"""

    @abstractmethod
    def __init__(self, name, description, price, quantity):
        pass

    @abstractmethod
    def __str__(self):
        """Абстрактный метод для строкового представления"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Абстрактный метод для сложения продуктов"""
        pass

    @property
    @abstractmethod
    def price(self):
        """Абстрактный геттер для цены"""
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        """Абстрактный сеттер для цены"""
        pass


class Product(LoggingMixin, BaseProduct):
    """Класс продукта с наследованием от миксина и абстрактного класса"""

    def __init__(self, name, description, price, quantity):
        # Проверка на нулевое количество
        if quantity == 0:
            raise ZeroQuantityError(
                "Товар с нулевым количеством не может быть добавлен"
            )

        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity
        # Вызываем миксин после инициализации атрибутов
        LoggingMixin.__init__(self)

    def __str__(self):
        """Строковое представление продукта"""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """Сложение продуктов - возвращает общую стоимость"""
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")

        # Проверка, что объекты одного типа
        if type(self) != type(other):
            raise TypeError("Нельзя складывать продукты разных типов")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self):
        """Геттер для цены"""
        return self._price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительная логика для понижения цены
        if new_price < self._price:
            confirmation = input("Цена понижается. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self._price = new_price

    def __repr__(self):
        """Представление для отладки"""
        return f"Product(name={repr(self.name)}, description={repr(self.description)}, price={self.price}, quantity={self.quantity})"


class Smartphone(Product):
    """Класс для смартфонов"""

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        # Вызываем конструктор родителя
        super(Product, self).__init__(name, description, price, quantity)

    def __str__(self):
        """Строковое представление смартфона"""
        return (
            f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт.\n"
            f"Производительность: {self.efficiency}, Память: {self.memory}GB, Цвет: {self.color}"
        )

    def __repr__(self):
        """Представление для отладки"""
        return (
            f"Smartphone(name={repr(self.name)}, description={repr(self.description)}, "
            f"price={self.price}, quantity={self.quantity}, efficiency={self.efficiency}, "
            f"model={repr(self.model)}, memory={self.memory}, color={repr(self.color)})"
        )


class LawnGrass(Product):
    """Класс для газонной травы"""

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        # Вызываем конструктор родителя
        super(Product, self).__init__(name, description, price, quantity)

    def __str__(self):
        """Строковое представление газонной травы"""
        return (
            f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"
            f"Страна: {self.country}, Прорастание: {self.germination_period}, Цвет: {self.color}"
        )

    def __repr__(self):
        """Представление для отладки"""
        return (
            f"LawnGrass(name={repr(self.name)}, description={repr(self.description)}, "
            f"price={self.price}, quantity={self.quantity}, country={repr(self.country)}, "
            f"germination_period={repr(self.germination_period)}, color={repr(self.color)})"
        )


class BaseEntity(ABC):
    """Абстрактный базовый класс для сущностей с товарами"""

    @abstractmethod
    def __init__(self):
        self.items = []

    @abstractmethod
    def add_item(self, product, quantity):
        """Абстрактный метод для добавления товара"""
        pass

    @abstractmethod
    def total_cost(self):
        """Абстрактный метод для расчета общей стоимости"""
        pass


class Category(BaseEntity):
    """Класс категории товаров"""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products=None):
        super().__init__()
        self.name = name
        self.description = description
        self.__products = []  # Приватный список продуктов

        if products:
            for product in products:
                self.add_product_with_check(product)

        Category.category_count += 1

    def add_product_with_check(self, product):
        """Добавляет продукт с проверкой на нулевое количество"""
        try:
            if product.quantity == 0:
                raise ZeroQuantityError("Нельзя добавить товар с нулевым количеством")

            self.__products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен")

        except ZeroQuantityError as e:
            print(f"Ошибка при добавлении товара: {e}")
        finally:
            print("Обработка добавления товара завершена")

    def add_product(self, product):
        """Добавляет продукт в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

    def add_item(self, product, quantity=1):
        """Реализация абстрактного метода"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        product.quantity = quantity
        self.add_product_with_check(product)

    def middle_price(self):
        """Подсчитывает средний ценник всех товаров в категории"""
        try:
            total_price = sum(product.price for product in self.__products)
            count = len(self.__products)
            if count == 0:
                return 0
            return total_price / count
        except ZeroDivisionError:
            return 0

    def total_cost(self):
        """Рассчитывает общую стоимость всех товаров в категории"""
        return sum(product.price * product.quantity for product in self.__products)

    def __str__(self):
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self):
        """Геттер для получения строкового представления продуктов"""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def get_products_list(self):
        """Метод для получения списка продуктов"""
        return self.__products


class Order(BaseEntity):
    """Класс заказа"""

    def __init__(self):
        super().__init__()
        self.items = []  # список кортежей (product, quantity)

    def add_item_with_check(self, product, quantity):
        """Добавляет товар в заказ с проверкой на нулевое количество"""
        try:
            if quantity == 0:
                raise ZeroQuantityError("Нельзя добавить товар с нулевым количеством")

            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только объекты Product")

            self.items.append((product, quantity))
            print(f"Товар '{product.name}' успешно добавлен в заказ")

        except (ZeroQuantityError, TypeError) as e:
            print(f"Ошибка при добавлении товара в заказ: {e}")
        finally:
            print("Обработка добавления товара в заказ завершена")

    def add_item(self, product, quantity):
        """Добавляет товар в заказ"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        if quantity <= 0:
            raise ValueError("Количество должно быть положительным")

        self.items.append((product, quantity))

    def total_cost(self):
        """Рассчитывает общую стоимость заказа"""
        return sum(product.price * quantity for product, quantity in self.items)

    def __str__(self):
        """Строковое представление заказа"""
        if not self.items:
            return "Заказ пуст"

        result = "Заказ:\n"
        for product, quantity in self.items:
            result += f"  - {product.name}: {quantity} шт. × {product.price} руб. = {product.price * quantity} руб.\n"
        result += f"Итого: {self.total_cost()} руб."
        return result


if __name__ == "__main__":
    print("=== Тестирование исключений при создании продукта ===")
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ZeroQuantityError as e:
        print(f"Возникла ошибка ZeroQuantityError: {e}")
    except ValueError as e:
        print(f"Возникла ошибка ValueError: {e}")
    else:
        print("Не возникла ошибка при попытке добавить продукт с нулевым количеством")

    print("\n=== Создание валидных продуктов ===")
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("\n=== Тестирование среднего ценника ===")
    category1 = Category(
        "Смартфоны", "Категория смартфонов", [product1, product2, product3]
    )
    print(
        f"Средний ценник в категории '{category1.name}': {category1.middle_price()} руб."
    )

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(f"Средний ценник в пустой категории: {category_empty.middle_price()} руб.")

    print("\n=== Тестирование добавления с проверкой ===")
    product_zero = Product(
        "Тестовый товар", "Тест", 100.0, 1
    )  # Сначала создаем с количеством 1
    product_zero.quantity = 0  # Затем меняем на 0 для теста
    category1.add_product_with_check(product_zero)

    print("\n=== Тестирование заказа ===")
    order = Order()
    order.add_item_with_check(product1, 2)
    order.add_item_with_check(product1, 0)  # Попытка добавить с нулевым количеством
    print(order)
