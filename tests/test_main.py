import pytest
from src.main import Product, Category, Order, ZeroQuantityError


class TestProductExceptions:
    def test_product_creation_with_zero_quantity(self):
        """Тест создания продукта с нулевым количеством"""
        with pytest.raises(ZeroQuantityError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Test Product", "Test Description", 100.0, 0)

    def test_product_creation_with_positive_quantity(self):
        """Тест создания продукта с положительным количеством"""
        product = Product("Test Product", "Test Description", 100.0, 5)
        assert product.quantity == 5
        assert product.name == "Test Product"


class TestCategoryMiddlePrice:
    def test_middle_price_with_products(self):
        """Тест среднего ценника с товарами"""
        product1 = Product("P1", "D1", 100.0, 2)
        product2 = Product("P2", "D2", 200.0, 3)
        product3 = Product("P3", "D3", 300.0, 1)

        category = Category("Test Category", "Test Description", [product1, product2, product3])
        assert category.middle_price() == 200.0

    def test_middle_price_empty_category(self):
        """Тест среднего ценника пустой категории"""
        category = Category("Empty Category", "Empty Description", [])
        assert category.middle_price() == 0

    def test_middle_price_single_product(self):
        """Тест среднего ценника с одним товаром"""
        product = Product("P1", "D1", 150.0, 5)
        category = Category("Single Category", "Single Description", [product])
        assert category.middle_price() == 150.0


class TestCategoryAddProduct:
    def test_add_product_with_zero_quantity(self, capsys):
        """Тест добавления товара с нулевым количеством в категорию"""
        product = Product("Test Product", "Test Description", 100.0, 1)
        product.quantity = 0  # Меняем количество на 0

        category = Category("Test Category", "Test Description", [])
        category.add_product_with_check(product)

        captured = capsys.readouterr()
        assert "Ошибка при добавлении товара" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category.get_products_list()) == 0

    def test_add_product_with_positive_quantity(self, capsys):
        """Тест добавления товара с положительным количеством в категорию"""
        product = Product("Test Product", "Test Description", 100.0, 5)

        category = Category("Test Category", "Test Description", [])
        category.add_product_with_check(product)

        captured = capsys.readouterr()
        assert "успешно добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out
        assert len(category.get_products_list()) == 1


class TestOrderExceptions:
    def test_add_item_with_zero_quantity(self, capsys):
        """Тест добавления товара с нулевым количеством в заказ"""
        product = Product("Test Product", "Test Description", 100.0, 5)

        order = Order()
        order.add_item_with_check(product, 0)

        captured = capsys.readouterr()
        assert "Ошибка при добавлении товара в заказ" in captured.out
        assert "Обработка добавления товара в заказ завершена" in captured.out
        assert len(order.items) == 0

    def test_add_item_with_positive_quantity(self, capsys):
        """Тест добавления товара с положительным количеством в заказ"""
        product = Product("Test Product", "Test Description", 100.0, 5)

        order = Order()
        order.add_item_with_check(product, 3)

        captured = capsys.readouterr()
        assert "успешно добавлен в заказ" in captured.out
        assert "Обработка добавления товара в заказ завершена" in captured.out
        assert len(order.items) == 1
        assert order.total_cost() == 300.0
