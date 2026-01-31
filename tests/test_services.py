import pytest
from services import validate_data, process_data, DataProcessor, calculate_summary, handle_error

@pytest.fixture
def valid_data():
    return {"key": "value", "number": 42}

@pytest.fixture
def invalid_data():
    return {"key": "value"}

@pytest.fixture
def empty_data():
    return {}

@pytest.fixture
def invalid_type_data():
    return {"key": 123}

@pytest.fixture
def complex_data():
    return {"key": "value", "number": 42, "list": [1, 2, 3]}

class TestDataValidation:
    def test_valid_data(self, valid_data):
        assert validate_data(valid_data)

    def test_invalid_data_missing_key(self, invalid_data):
        assert not validate_data(invalid_data)

    def test_empty_data(self, empty_data):
        assert not validate_data(empty_data)

    def test_invalid_type(self, invalid_type_data):
        assert not validate_data(invalid_type_data)

    @pytest.mark.parametrize("data, expected", [
        ({"key": "value", "number": 42}, True),
        ({"key": "value"}, False),
        ({}, False),
        ({"key": 123}, False),
        ({"key": "value", "number": "forty-two"}, False),
    ])
    def test_validate_data_parametrized(self, data, expected):
        assert validate_data(data) == expected

class TestDataProcessing:
    def test_process_data_valid(self, valid_data):
        result = process_data(valid_data)
        assert result == {"processed": "value", "number": 42}

    def test_process_data_invalid(self, invalid_data):
        with pytest.raises(ValueError):
            process_data(invalid_data)

    def test_process_data_empty(self, empty_data):
        with pytest.raises(ValueError):
            process_data(empty_data)

    def test_data_processor_validate(self, valid_data):
        processor = DataProcessor()
        assert processor.validate(valid_data)

    def test_data_processor_invalid(self, invalid_data):
        processor = DataProcessor()
        assert not processor.validate(invalid_data)

    def test_data_processor_process_valid(self, valid_data):
        processor = DataProcessor()
        result = processor.process(valid_data)
        assert result == {"processed": "value", "number": 42}

    def test_data_processor_process_invalid(self, invalid_data):
        processor = DataProcessor()
        with pytest.raises(ValueError):
            processor.process(invalid_data)

class TestErrorHandling:
    def test_handle_error_with_exception(self):
        with pytest.raises(ValueError):
            handle_error(ValueError("Test error"))

    def test_handle_error_with_other_exception(self):
        with pytest.raises(TypeError):
            handle_error(TypeError("Another error"))

    def test_handle_error_returns_message(self):
        result = handle_error(ValueError("Test error"))
        assert result == "Test error"

    def test_handle_error_unknown_exception(self):
        with pytest.raises(Exception):
            handle_error(Exception("Unknown error"))

    @pytest.mark.parametrize("exception_type, expected_message", [
        (ValueError, "Invalid data"),
        (TypeError, "Data type mismatch"),
        (KeyError, "Missing required key"),
    ])
    def test_handle_error_parametrized(self, exception_type, expected_message):
        try:
            raise exception_type(expected_message)
        except exception_type as e:
            result = handle_error(e)
            assert result == expected_message

    def test_handle_error_no_exception(self):
        result = handle_error(None)
        assert result is None

class TestDataSummary:
    def test_calculate_summary_valid(self, valid_data):
        result = calculate_summary(valid_data)
        assert result == {"total": 42, "items": 1}

    def test_calculate_summary_empty(self, empty_data):
        result = calculate_summary(empty_data)
        assert result == {"total": 0, "items": 0}

    def test_calculate_summary_invalid(self, invalid_data):
        with pytest.raises(ValueError):
            calculate_summary(invalid_data)

    def test_calculate_summary_complex_data(self, complex_data):
        result = calculate_summary(complex_data)
        assert result == {"total": 42, "items": 1, "list_length": 3}