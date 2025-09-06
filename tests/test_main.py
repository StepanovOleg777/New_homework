import pytest

from src.main import Product, Category


@pytest.fixture
def sample_products():
    """Фикстура для создания тестовых продуктов"""
    return [
        Product(
            "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
        ),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории"""
    return Category("Смартфоны", "Смартфоны как средство коммуникации", sample_products)


def test_product_creation():
    """Тест создания продукта"""
    product = Product("Test Product", "Test Description", 100.0, 10)

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_creation(sample_category, sample_products):
    """Тест создания категории"""
    products_str = sample_category.products
    assert "Samsung Galaxy S23 Ultra" in products_str
    assert "Iphone 15" in products_str
    assert "Xiaomi Redmi Note 11" in products_str
    assert "180000.0 руб." in products_str
    assert "Остаток: 5 шт." in products_str
