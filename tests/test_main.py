import pytest
from src.main import Product, Smartphone, LawnGrass, Category

@pytest.fixture
def sample_smartphone():
    return Smartphone("Test Phone", "Test Desc", 1000.0, 5, 90.0, "Model X", 128, "Black")

@pytest.fixture
def sample_lawn_grass():
    return LawnGrass("Test Grass", "Grass Desc", 50.0, 10, "Russia", "7 days", "Green")

@pytest.fixture
def sample_product():
    return Product("Test Product", "Product Desc", 100.0, 3)

class TestInheritance:
    def test_smartphone_inheritance(self, sample_smartphone):
        """Тест что Smartphone наследуется от Product"""
        assert isinstance(sample_smartphone, Product)
        assert hasattr(sample_smartphone, 'name')
        assert hasattr(sample_smartphone, 'price')
        assert hasattr(sample_smartphone, 'efficiency')
        assert hasattr(sample_smartphone, 'model')

    def test_lawn_grass_inheritance(self, sample_lawn_grass):
        """Тест что LawnGrass наследуется от Product"""
        assert isinstance(sample_lawn_grass, Product)
        assert hasattr(sample_lawn_grass, 'name')
        assert hasattr(sample_lawn_grass, 'price')
        assert hasattr(sample_lawn_grass, 'country')
        assert hasattr(sample_lawn_grass, 'germination_period')

    def test_smartphone_attributes(self, sample_smartphone):
        """Тест атрибутов Smartphone"""
        assert sample_smartphone.efficiency == 90.0
        assert sample_smartphone.model == "Model X"
        assert sample_smartphone.memory == 128
        assert sample_smartphone.color == "Black"

    def test_lawn_grass_attributes(self, sample_lawn_grass):
        """Тест атрибутов LawnGrass"""
        assert sample_lawn_grass.country == "Russia"
        assert sample_lawn_grass.germination_period == "7 days"
        assert sample_lawn_grass.color == "Green"

class TestAdditionRestrictions:
    def test_same_type_addition(self, sample_smartphone):
        """Тест сложения объектов одного типа"""
        smartphone2 = Smartphone("Phone 2", "Desc 2", 800.0, 3, 85.0, "Model Y", 64, "White")
        result = sample_smartphone + smartphone2
        expected = (1000.0 * 5) + (800.0 * 3)  # 5000 + 2400 = 7400
        assert result == expected

    def test_different_type_addition_error(self, sample_smartphone, sample_lawn_grass):
        """Тест ошибки при сложении разных типов"""
        with pytest.raises(TypeError, match="Нельзя складывать продукты разных типов"):
            sample_smartphone + sample_lawn_grass

    def test_product_with_smartphone_addition_error(self, sample_product, sample_smartphone):
        """Тест ошибки при сложении Product и Smartphone"""
        with pytest.raises(TypeError, match="Нельзя складывать продукты разных типов"):
            sample_product + sample_smartphone

class TestCategoryRestrictions:
    def test_add_valid_product(self, sample_smartphone):
        """Тест добавления валидного продукта"""
        category = Category("Test", "Test")
        initial_count = Category.product_count
        category.add_product(sample_smartphone)
        assert Category.product_count == initial_count + 1

    def test_add_invalid_product_error(self):
        """Тест ошибки при добавлении не продукта"""
        category = Category("Test", "Test")
        with pytest.raises(TypeError, match="Можно добавлять только объекты Product или его наследников"):
            category.add_product("not a product")

    def test_add_lawn_grass_to_category(self, sample_lawn_grass):
        """Тест добавления LawnGrass в категорию"""
        category = Category("Test", "Test")
        category.add_product(sample_lawn_grass)
        assert len(category.get_products_list()) == 1

    def test_initial_products_validation(self, sample_smartphone, sample_lawn_grass):
        """Тест валидации продуктов при инициализации категории"""
        category = Category("Test", "Test", [sample_smartphone, sample_lawn_grass])
        assert len(category.get_products_list()) == 2

class TestStringRepresentation:
    def test_smartphone_str(self, sample_smartphone):
        """Тест строкового представления Smartphone"""
        result = str(sample_smartphone)
        assert "Test Phone" in result
        assert "Model X" in result
        assert "128GB" in result
        assert "Black" in result

    def test_lawn_grass_str(self, sample_lawn_grass):
        """Тест строкового представления LawnGrass"""
        result = str(sample_lawn_grass)
        assert "Test Grass" in result
        assert "Russia" in result
        assert "7 days" in result
        assert "Green" in result

def test_main_execution():
    """Тест, что main.py выполняется без ошибок"""
    import subprocess
    import sys
    result = subprocess.run([sys.executable, "src/main.py"], capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, f"Main execution failed: {result.stderr}"