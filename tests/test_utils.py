import pytest
from utils import validate_email, is_valid_url, sanitize_string, format_currency, slugify, trim_whitespace, StringProcessor

class TestStringValidation:
    @pytest.mark.parametrize("input_str, expected", [
        ("test@example.com", True),
        ("invalid@example", False),
        ("user@domain.com", True),
        ("", False),
        (None, False),
    ])
    def test_validate_email(self, input_str, expected):
        assert validate_email(input_str) == expected

    @pytest.mark.parametrize("input_str, expected", [
        ("http://example.com", True),
        ("https://example.org/path?query=1", True),
        ("example.com", False),
        ("http://", False),
        ("http://example", False),
        ("", False),
        (None, False),
    ])
    def test_is_valid_url(self, input_str, expected):
        assert is_valid_url(input_str) == expected

    @pytest.mark.parametrize("input_str, expected", [
        ("This is a test string", "This is a test string"),
        ("This is a test string with <b>HTML</b> and special #chars!", "This is a test string with HTML and special chars"),
        ("", ""),
        (None, None),
    ])
    def test_sanitize_string(self, input_str, expected):
        assert sanitize_string(input_str) == expected

class TestStringFormatting:
    @pytest.mark.parametrize("value, currency, expected", [
        (123.45, "USD", "$123.45"),
        (1234.56, "EUR", "€1,234.56"),
        (0, "GBP", "£0.00"),
        (-100, "USD", "-$100.00"),
        ("invalid", "USD", "Invalid input"),
        (None, "USD", "Invalid input"),
    ])
    def test_format_currency(self, value, currency, expected):
        assert format_currency(value, currency) == expected

    @pytest.mark.parametrize("input_str, expected", [
        ("Hello World", "hello-world"),
        ("This is a test string", "this-is-a-test-string"),
        ("", ""),
        (None, None),
    ])
    def test_slugify(self, input_str, expected):
        assert slugify(input_str) == expected

    @pytest.mark.parametrize("input_str, expected", [
        ("  Leading and trailing spaces  ", "Leading and trailing spaces"),
        ("   Multiple   spaces   ", "Multiple spaces"),
        ("", ""),
        (None, None),
    ])
    def test_trim_whitespace(self, input_str, expected):
        assert trim_whitespace(input_str) == expected

class TestStringProcessing:
    def setup_method(self):
        self.processor = StringProcessor()

    def test_process_string(self):
        assert self.processor.process_string("test") == "processed test"

    def test_validate(self):
        assert self.processor.validate("valid") == True

    def test_process_string_invalid_input(self):
        with pytest.raises(TypeError):
            self.processor.process_string(123)