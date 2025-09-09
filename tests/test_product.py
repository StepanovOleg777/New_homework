import pytest
from src.product import Product, Category, ZeroQuantityError


@pytest.fixture
def sample_products():
    return [
        Product("Product1", "Desc1", 100.0, 5),
        Product("Product2", "Desc2", 200.0, 3),
        Product("Product3", "Desc3", 300.0, 2),
    ]


@pytest.fixture
def sample_category(sample_products):
    return Category("Test Category", "Test Description", sample_products)


class TestProduct:
    def test_product_creation_with_zero_quantity(self):
        """Тест создания продукта с нулевым количеством"""
        with pytest.raises(
            ZeroQuantityError,
            match="Товар с нулевым количеством не может быть добавлен",
        ):
            Product("Test", "Desc", 100.0, 0)

    def test_product_creation_with_positive_quantity(self):
        """Тест создания продукта с положительным количеством"""
        product = Product("Test", "Desc", 100.0, 5)
        assert product.name == "Test"
        assert product.price == 100.0
        assert product.quantity == 5

    def test_product_str_representation(self):
        """Тест строкового представления продукта"""
        product = Product("Test", "Desc", 150.0, 10)
        expected = "Test, 150.0 руб. Остаток: 10 шт."
        assert str(product) == expected


class TestCategory:
    def test_middle_price_with_products(self, sample_category):
        """Тест среднего ценника с товарами"""
        # (100 + 200 + 300) / 3 = 200
        assert sample_category.middle_price() == 200.0

    def test_middle_price_empty_category(self):
        """Тест среднего ценника пустой категории"""
        empty_category = Category("Empty", "Empty", [])
        assert empty_category.middle_price() == 0

    def test_middle_price_single_product(self):
        """Тест среднего ценника с одним товаром"""
        product = Product("P1", "D1", 150.0, 5)
        category = Category("Single", "Single", [product])
        assert category.middle_price() == 150.0

    def test_category_creation(self, sample_category, sample_products):
        """Тест создания категории"""
        assert sample_category.name == "Test Category"
        assert sample_category.description == "Test Description"


def test_zero_quantity_error_inheritance():
    """Тест что ZeroQuantityError наследуется от ValueError"""
    assert issubclass(ZeroQuantityError, ValueError)
