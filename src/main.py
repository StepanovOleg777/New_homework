from abc import ABC, abstractmethod


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
                self.add_product(product)

        Category.category_count += 1

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
        self.add_product(product)

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
    print("=== Создание продуктов с логированием ===")
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("\n=== Информация о продуктах ===")
    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    print("\n=== Создание категории ===")
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.get_products_list()))
    print(Category.category_count)
    print(Category.product_count)

    print("\n=== Создание дополнительного продукта и категории ===")
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.get_products_list()))
    print(category2.products)

    print("\n=== Статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего продуктов: {Category.product_count}")

    print("\n=== Дополнительное: создание заказа ===")
    order = Order()
    order.add_item(product1, 2)
    order.add_item(product2, 1)
    print(order)
