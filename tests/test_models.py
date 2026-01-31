import pytest
from your_module.models import User, Product, validate_data, process_data

@pytest.fixture
def valid_user_data():
    return {"username": "testuser", "email": "test@example.com", "age": 30, "is_active": True}

@pytest.fixture
def invalid_user_data():
    return {"username": 123, "email": "invalid", "age": "thirty", "is_active": "true"}

@pytest.fixture
def valid_product_data():
    return {"name": "Laptop", "price": 999.99, "stock": 100}

@pytest.fixture
def invalid_product_data():
    return {"name": "Laptop", "price": "invalid", "stock": 100}

class TestDataValidation:
    def test_user_model_valid_data(self, valid_user_data):
        user = User(**valid_user_data)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.age == 30
        assert user.is_active is True

    def test_user_model_invalid_data(self, invalid_user_data):
        with pytest.raises(ValueError):
            User(**invalid_user_data)

    def test_user_model_missing_required_field(self):
        with pytest.raises(ValueError):
            User(username="testuser", email="test@example.com")

    def test_user_model_invalid_age(self):
        with pytest.raises(ValueError):
            User(username="test", email="test@example.com", age=17)

    def test_product_model_valid_data(self, valid_product_data):
        product = Product(**valid_product_data)
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.stock == 100

    def test_product_model_invalid_data(self, invalid_product_data):
        with pytest.raises(ValueError):
            Product(**invalid_product_data)

    def test_product_model_invalid_stock(self):
        with pytest.raises(ValueError):
            Product(name="Laptop", price=999.99, stock=-1)

class TestErrorHandling:
    @pytest.mark.parametrize("data,expected_exception", [
        ({"username": 123, "email": "invalid"}, ValueError),
        ({"username": "test", "email": "invalid"}, ValueError),
        ({"username": "test", "email": "test@example.com", "age": "thirty"}, ValueError)
    ])
    def test_validate_data_failure(self, data, expected_exception):
        with pytest.raises(expected_exception):
            validate_data(data)

    def test_process_data_invalid_input(self):
        with pytest.raises(ValueError):
            process_data({"invalid_key": "value"})

    def test_invalid_enum_value(self):
        with pytest.raises(ValueError):
            User(role="admin")  # Assuming role is an enum with allowed values

class TestUtilityFunctions:
    @pytest.mark.parametrize("data,expected", [
        ({"username": "a", "email": "a@a.com"}, True),
        ({"username": "b", "email": "b@b.com"}, True),
        ({"username": "", "email": "c@c.com"}, False),
    ])
    def test_validate_data_success(self, data, expected):
        assert validate_data(data) is True

    def test_process_data_success(self):
        result = process_data({"data": "valid"})
        assert result == "processed"

    def test_process_data_failure(self):
        with pytest.raises(ValueError):
            process_data({"data": 123})

    def test_process_data_edge_case(self):
        result = process_data({"data": "edge_case"})
        assert result == "processed"