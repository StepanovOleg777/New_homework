import pytest
from src.main import Product, Category


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 10)


@pytest.fixture
def sample_category():
    return Category("Test Category", "Test Description", [])


class TestProductAccess:
    def test_private_price_access(self, sample_product):
        """Тест приватного доступа к цене"""
        with pytest.raises(AttributeError):
            _ = sample_product.__price

    def test_price_getter(self, sample_product):
        """Тест геттера цены"""
        assert sample_product.price == 100.0


class TestCategoryAccess:
    def test_private_products_access(self, sample_category):
        """Тест приватного доступа к продуктам"""
        with pytest.raises(AttributeError):
            _ = sample_category.__products

    def test_add_product_method(self, sample_category, sample_product):
        """Тест метода add_product"""
        initial_count = Category.product_count
        sample_category.add_product(sample_product)
        assert Category.product_count == initial_count + 1
