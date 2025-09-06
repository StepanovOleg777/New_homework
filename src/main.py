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

    def __str__(self):
        """Строковое представление категории"""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        """Добавляет продукт в категорию"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для получения строкового представления продуктов"""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def get_products_list(self):
        """Метод для получения списка продуктов (для внутреннего использования)"""
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


if __name__ == "__main__":

    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("=== Строковое представление продуктов ===")
    print(str(product1))
    print(str(product2))
    print(str(product3))
    print()

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print("=== Строковое представление категории ===")
    print(str(category1))
    print()

    print("=== Список продуктов через геттер ===")
    print(category1.products)

    print("=== Сложение продуктов ===")
    print(f"Product1 + Product2 = {product1 + product2} руб.")
    print(f"Product1 + Product3 = {product1 + product3} руб.")
    print(f"Product2 + Product3 = {product2 + product3} руб.")
    print()

    print("=== Итерация по продуктам категории ===")
    for product in CategoryIterator(category1):
        print(f"  - {product}")

    print("\n=== Тест обработки дубликатов ===")
    existing_products = [product1, product2, product3]

    duplicate_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "Новая версия",
        "price": 185000.0,
        "quantity": 3,
    }

    new_product = Product.new_product(duplicate_data, existing_products)
    print(
        f"После объединения: {product1.name}, количество: {product1.quantity}, цена: {product1.price} руб."
    )

    print("\n=== Тест валидации цены ===")
    print(f"Текущая цена product1: {product1.price} руб.")
    product1.price = -100
    product1.price = 190000.0
    print(f"Новая цена product1: {product1.price} руб.")
