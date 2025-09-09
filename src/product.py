class ZeroQuantityError(ValueError):
    """Пользовательское исключение для товаров с нулевым количеством"""

    pass


class Product:
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        # Проверка на нулевое количество
        if quantity == 0:
            raise ZeroQuantityError(
                "Товар с нулевым количеством не может быть добавлен"
            )

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

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

    @classmethod
    def new_product(cls, product_data, existing_products=None):
        """Класс-метод для создания нового продукта с проверкой дубликатов"""
        if existing_products:
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    # Объединяем количества
                    existing_product.quantity += product_data["quantity"]
                    # Выбираем максимальную цену
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]
                    return existing_product

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительная логика для понижения цены
        if new_price < self.__price:
            confirmation = input("Цена понижается. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price

    def __repr__(self):
        """Представление для отладки"""
        return f"Product(name={repr(self.name)}, description={repr(self.description)}, price={self.price}, quantity={self.quantity})"


class Category:
    name: str
    description: str
    __products: list
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product):
        """Добавляет продукт в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты Product или его наследников"
            )

        self.__products.append(product)
        Category.product_count += 1

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


class CategoryIterator:
    """Итератор для перебора продуктов в категории"""

    def __init__(self, category):
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category.get_products_list()):
            product = self.category.get_products_list()[self.index]
            self.index += 1
            return product
        raise StopIteration
