import pytest
from src.main import Product, Category, CategoryIterator


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
    def test_product_str_representation(self):
        product = Product("Test Product", "Test Desc", 150.0, 10)
        expected = "Test Product, 150.0 руб. Остаток: 10 шт."
        assert str(product) == expected

    def test_product_addition(self):
        product1 = Product("P1", "D1", 100.0, 5)
        product2 = Product("P2", "D2", 200.0, 3)
        result = product1 + product2
        assert result == 1100

    def test_product_addition_type_error(self):
        product = Product("P1", "D1", 100.0, 5)
        with pytest.raises(TypeError):
            product + "not a product"


class TestCategory:
    def test_category_str_representation(self, sample_category):
        expected = "Test Category, количество продуктов: 10 шт."
        assert str(sample_category) == expected

    def test_category_products_property(self, sample_category):
        products_str = sample_category.products
        assert "Product1" in products_str
        assert "100.0 руб." in products_str
        assert "5 шт." in products_str


class TestCategoryIterator:
    def test_iterator_usage(self, sample_category):
        products = list(CategoryIterator(sample_category))
        assert len(products) == 3
        assert products[0].name == "Product1"


def test_main_execution():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "src/main.py"], capture_output=True, text=True
    )
    assert result.returncode == 0
