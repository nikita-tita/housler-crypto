"""
Tests for utility functions: masking, normalization, validation.
"""

import pytest
from housler_crypto import mask, normalize_phone, normalize_email
from housler_crypto.utils import validate_email, validate_phone, validate_inn


class TestMaskEmail:
    """Test email masking."""

    def test_normal_email(self):
        """Should mask local part, keep domain."""
        assert mask.email("test@example.com") == "te***@example.com"

    def test_short_local(self):
        """Short local part should show ***."""
        assert mask.email("ab@example.com") == "***@example.com"

    def test_single_char_local(self):
        """Single char local should show ***."""
        assert mask.email("a@example.com") == "***@example.com"

    def test_empty_email(self):
        """Empty email should return ***."""
        assert mask.email("") == "***"

    def test_none_email(self):
        """None should return ***."""
        assert mask.email(None) == "***"

    def test_no_at_sign(self):
        """Email without @ should return ***."""
        assert mask.email("notanemail") == "***"

    def test_long_local(self):
        """Long local part should show first 2 chars."""
        assert mask.email("verylongemail@domain.com") == "ve***@domain.com"


class TestMaskPhone:
    """Test phone masking."""

    def test_russian_phone(self):
        """Russian phone should mask middle."""
        assert mask.phone("+79991234567") == "+7***4567"

    def test_phone_without_plus(self):
        """Phone without + should still work."""
        assert mask.phone("79991234567") == "7***4567"

    def test_formatted_phone(self):
        """Formatted phone should be processed."""
        result = mask.phone("+7 (999) 123-45-67")
        assert result.endswith("4567")
        assert "***" in result

    def test_short_phone(self):
        """Short phone should return ***."""
        assert mask.phone("123") == "***"

    def test_empty_phone(self):
        """Empty phone should return ***."""
        assert mask.phone("") == "***"


class TestMaskName:
    """Test name masking."""

    def test_two_word_name(self):
        """Two-word name should mask each word."""
        assert mask.name("Иван Иванов") == "Ив*** Ив***"

    def test_single_word_name(self):
        """Single word name."""
        assert mask.name("Иван") == "Ив***"

    def test_short_word(self):
        """Short word (<=2 chars) should show ***."""
        assert mask.name("Ян") == "***"

    def test_three_word_name(self):
        """Three-word name."""
        result = mask.name("Иван Иванович Иванов")
        parts = result.split()
        assert len(parts) == 3
        assert all("***" in p for p in parts)

    def test_empty_name(self):
        """Empty name should return ***."""
        assert mask.name("") == "***"


class TestMaskInn:
    """Test INN masking."""

    def test_10_digit_inn(self):
        """10-digit INN (company)."""
        assert mask.inn("7707083893") == "77***3893"

    def test_12_digit_inn(self):
        """12-digit INN (individual)."""
        assert mask.inn("772012345678") == "77***5678"

    def test_short_inn(self):
        """Short INN should return ***."""
        assert mask.inn("12345") == "***"

    def test_empty_inn(self):
        """Empty INN should return ***."""
        assert mask.inn("") == "***"


class TestMaskCard:
    """Test card number masking (PCI DSS compliant)."""

    def test_normal_card(self):
        """Should show only last 4 digits."""
        assert mask.card("4111111111111111") == "**** **** **** 1111"

    def test_formatted_card(self):
        """Formatted card should work."""
        assert mask.card("4111 1111 1111 1111") == "**** **** **** 1111"

    def test_short_card(self):
        """Short number should return ***."""
        assert mask.card("123") == "***"

    def test_empty_card(self):
        """Empty card should return ***."""
        assert mask.card("") == "***"


class TestMaskPassport:
    """Test passport masking."""

    def test_full_mask(self):
        """Passport should be fully masked."""
        assert mask.passport("1234", "567890") == "** ** ******"


class TestNormalizePhone:
    """Test phone normalization."""

    def test_formatted_phone(self):
        """+7 (999) 123-45-67 -> 79991234567"""
        assert normalize_phone("+7 (999) 123-45-67") == "79991234567"

    def test_8_prefix(self):
        """8-999-123-45-67 -> 79991234567"""
        assert normalize_phone("8-999-123-45-67") == "79991234567"

    def test_10_digits(self):
        """10 digits should add 7 prefix."""
        assert normalize_phone("9991234567") == "79991234567"

    def test_already_normalized(self):
        """Already normalized should stay same."""
        assert normalize_phone("79991234567") == "79991234567"

    def test_with_spaces(self):
        """Should remove spaces."""
        assert normalize_phone("7 999 123 45 67") == "79991234567"

    def test_empty(self):
        """Empty should return empty."""
        assert normalize_phone("") == ""


class TestNormalizeEmail:
    """Test email normalization."""

    def test_lowercase(self):
        """Should lowercase."""
        assert normalize_email("Test@Example.COM") == "test@example.com"

    def test_strip_whitespace(self):
        """Should strip whitespace."""
        assert normalize_email("  test@example.com  ") == "test@example.com"

    def test_empty(self):
        """Empty should return empty."""
        assert normalize_email("") == ""


class TestValidateEmail:
    """Test email validation."""

    def test_valid_email(self):
        """Valid email should return True."""
        assert validate_email("test@example.com") is True

    def test_valid_email_with_plus(self):
        """Email with + should be valid."""
        assert validate_email("test+tag@example.com") is True

    def test_invalid_no_at(self):
        """Email without @ is invalid."""
        assert validate_email("testexample.com") is False

    def test_invalid_no_domain(self):
        """Email without domain is invalid."""
        assert validate_email("test@") is False

    def test_empty(self):
        """Empty is invalid."""
        assert validate_email("") is False


class TestValidatePhone:
    """Test phone validation."""

    def test_valid_11_digits(self):
        """11 digits is valid."""
        assert validate_phone("79991234567") is True

    def test_valid_10_digits(self):
        """10 digits is valid."""
        assert validate_phone("9991234567") is True

    def test_valid_formatted(self):
        """Formatted phone is valid."""
        assert validate_phone("+7 (999) 123-45-67") is True

    def test_invalid_short(self):
        """Too short is invalid."""
        assert validate_phone("12345") is False

    def test_invalid_long(self):
        """Too long is invalid."""
        assert validate_phone("123456789012345") is False

    def test_empty(self):
        """Empty is invalid."""
        assert validate_phone("") is False


class TestValidateInn:
    """Test INN validation."""

    def test_valid_10_digit(self):
        """10-digit INN is valid."""
        assert validate_inn("7707083893") is True

    def test_valid_12_digit(self):
        """12-digit INN is valid."""
        assert validate_inn("772012345678") is True

    def test_invalid_length(self):
        """Wrong length is invalid."""
        assert validate_inn("12345") is False
        assert validate_inn("12345678901") is False  # 11 digits

    def test_empty(self):
        """Empty is invalid."""
        assert validate_inn("") is False
