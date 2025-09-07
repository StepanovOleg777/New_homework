import pytest
from io import StringIO
import sys
from src.main import (
    BaseProduct,
    Product,
    Smartphone,
    LawnGrass,
    Category,
    Order,
    LoggingMixin,
    BaseEntity,
)


class TestAbstractBase:
    def test_base_product_is_abstract(self):
        """Тест что BaseProduct является абстрактным классом"""
        with pytest.raises(TypeError):
            BaseProduct("Test", "Test", 100.0, 5)

    def test_product_inherits_from_base(self):
        """Тест что Product наследуется от BaseProduct"""
        assert issubclass(Product, BaseProduct)

    def test_abstract_methods_implementation(self):
        """Тест что Product реализует все абстрактные методы"""
        product = Product("Test", "Test", 100.0, 5)
        assert hasattr(product, "__str__")
        assert hasattr(product, "__add__")
        assert hasattr(product, "price")


class TestLoggingMixin:
    def test_logging_on_creation(self, capsys):
        """Тест логирования при создании объекта"""
        product = Product("Test Product", "Test Description", 100.0, 5)
        captured = capsys.readouterr()
        assert "Создан объект Product" in captured.out
        assert "name='Test Product'" in captured.out

    def test_repr_method(self):
        """Тест метода __repr__"""
        product = Product("Test", "Desc", 100.0, 5)
        repr_str = repr(product)
        assert "Product" in repr_str
        assert "name='Test'" in repr_str


class TestInheritanceChain:
    def test_mro_chain(self):
        """Тест порядка разрешения методов"""
        mro = Product.__mro__
        assert LoggingMixin in mro
        assert BaseProduct in mro
        assert object in mro

    def test_smartphone_inheritance(self):
        """Тест цепочки наследования Smartphone"""
        assert issubclass(Smartphone, Product)
        assert issubclass(Smartphone, BaseProduct)
        assert issubclass(Smartphone, LoggingMixin)

    def test_lawn_grass_inheritance(self):
        """Тест цепочки наследования LawnGrass"""
        assert issubclass(LawnGrass, Product)
        assert issubclass(LawnGrass, BaseProduct)
        assert issubclass(LawnGrass, LoggingMixin)


class TestAdditionalFeatures:
    def test_order_creation(self):
        """Тест создания заказа"""
        product = Product("Test", "Desc", 100.0, 5)
        order = Order()
        order.add_item(product, 2)
        assert len(order.items) == 1
        assert order.total_cost() == 200.0

    def test_order_string_representation(self):
        """Тест строкового представления заказа"""
        product = Product("Test", "Desc", 100.0, 5)
        order = Order()
        order.add_item(product, 3)
        order_str = str(order)
        assert "Заказ:" in order_str
        assert "300.0 руб." in order_str

    def test_category_inheritance(self):
        """Тест что Category наследуется от BaseEntity"""
        assert issubclass(Category, BaseEntity)

    def test_category_total_cost(self):
        """Тест расчета общей стоимости в категории"""
        product1 = Product("P1", "D1", 100.0, 2)
        product2 = Product("P2", "D2", 200.0, 3)
        category = Category("Test", "Test", [product1, product2])
        assert category.total_cost() == (100 * 2 + 200 * 3)
