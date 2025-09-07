class Product:
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
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
                if existing_product.name == product_data['name']:
                    # Объединяем количества
                    existing_product.quantity += product_data['quantity']
                    # Выбираем максимальную цену
                    if product_data['price'] > existing_product.price:
                        existing_product.price = product_data['price']
                    return existing_product

        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
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
            if confirmation.lower() != 'y':
                print("Изменение цены отменено")
                return

        self.__price = new_price


class Smartphone(Product):
    """Класс для смартфонов"""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency  # производительность
        self.model = model  # модель
        self.memory = memory  # объем встроенной памяти
        self.color = color  # цвет

    def __str__(self):
        """Строковое представление смартфона"""
        return (f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт.\n"
                f"Производительность: {self.efficiency}, Память: {self.memory}GB, Цвет: {self.color}")


class LawnGrass(Product):
    """Класс для газонной травы"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country  # страна-производитель
        self.germination_period = germination_period  # срок прорастания
        self.color = color  # цвет

    def __str__(self):
        """Строковое представление газонной травы"""
        return (f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт.\n"
                f"Страна: {self.country}, Прорастание: {self.germination_period}, Цвет: {self.color}")


class Category:
    name: str
    description: str
    __products: list
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []

        # Добавляем продукты через метод для проверки
        if products:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product):
        """Добавляет продукт в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1

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


if __name__ == '__main__':
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print("=== Информация о смартфонах ===")
    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)
    print()

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)
    print()

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)
    print()

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print("=== Информация о газонной траве ===")
    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)
    print()

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)
    print()

    print("=== Тестирование сложения ===")
    smartphone_sum = smartphone1 + smartphone2
    print(f"Сумма смартфонов: {smartphone_sum} руб.")

    grass_sum = grass1 + grass2
    print(f"Сумма газонной травы: {grass_sum} руб.")

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError as e:
        print(f"Возникла ошибка TypeError при попытке сложения: {e}")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print("\n=== Продукты в категории Смартфоны ===")
    print(category_smartphones.products)

    print(f"Общее количество продуктов: {Category.product_count}")

    try:
        category_smartphones.add_product("Not a product")
    except TypeError as e:
        print(f"Возникла ошибка TypeError при добавлении не продукта: {e}")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")

    print("\n=== Строковое представление ===")
    print(smartphone1)
    print()
    print(grass1)
    print()
    print(category_smartphones)
    print(category_grass)