"""
Tests for core HouslerCrypto encryption/decryption.
"""

import pytest
from housler_crypto import HouslerCrypto


# Test key (32 bytes = 64 hex chars)
TEST_KEY = "a" * 64  # Simple test key


class TestHouslerCryptoInit:
    """Test initialization."""

    def test_valid_key(self):
        """Should accept valid 64-char hex key."""
        crypto = HouslerCrypto(master_key=TEST_KEY)
        assert crypto is not None

    def test_invalid_key_empty(self):
        """Should reject empty key."""
        with pytest.raises(ValueError, match="master_key is required"):
            HouslerCrypto(master_key="")

    def test_invalid_key_wrong_length(self):
        """Should reject key with wrong length."""
        with pytest.raises(ValueError, match="must be 32 bytes"):
            HouslerCrypto(master_key="a" * 32)  # Too short

    def test_invalid_key_not_hex(self):
        """Should reject non-hex characters."""
        with pytest.raises(ValueError, match="Invalid master_key"):
            HouslerCrypto(master_key="g" * 64)  # 'g' is not hex

    def test_generate_key(self):
        """Should generate valid 64-char hex key."""
        key = HouslerCrypto.generate_key()
        assert len(key) == 64
        # Verify it's valid hex
        int(key, 16)
        # Verify it can be used
        crypto = HouslerCrypto(master_key=key)
        assert crypto is not None


class TestEncryptDecrypt:
    """Test encrypt/decrypt roundtrip."""

    @pytest.fixture
    def crypto(self):
        return HouslerCrypto(master_key=TEST_KEY)

    def test_roundtrip_simple(self, crypto):
        """Basic encrypt/decrypt should work."""
        plaintext = "test@example.com"
        encrypted = crypto.encrypt(plaintext, field="email")
        decrypted = crypto.decrypt(encrypted, field="email")
        assert decrypted == plaintext

    def test_roundtrip_unicode(self, crypto):
        """Should handle unicode (Cyrillic)."""
        plaintext = "Иван Иванов"
        encrypted = crypto.encrypt(plaintext, field="name")
        decrypted = crypto.decrypt(encrypted, field="name")
        assert decrypted == plaintext

    def test_roundtrip_special_chars(self, crypto):
        """Should handle special characters."""
        plaintext = "test+special@exam-ple.com"
        encrypted = crypto.encrypt(plaintext, field="email")
        decrypted = crypto.decrypt(encrypted, field="email")
        assert decrypted == plaintext

    def test_roundtrip_long_text(self, crypto):
        """Should handle long text."""
        plaintext = "A" * 10000
        encrypted = crypto.encrypt(plaintext, field="data")
        decrypted = crypto.decrypt(encrypted, field="data")
        assert decrypted == plaintext

    def test_empty_string_encrypt(self, crypto):
        """Empty string should return empty string."""
        assert crypto.encrypt("", field="email") == ""

    def test_empty_string_decrypt(self, crypto):
        """Empty string should return empty string."""
        assert crypto.decrypt("", field="email") == ""

    def test_hc1_prefix(self, crypto):
        """Encrypted data should have hc1: prefix."""
        encrypted = crypto.encrypt("test", field="email")
        assert encrypted.startswith("hc1:")

    def test_idempotent_encrypt(self, crypto):
        """Encrypting already encrypted data should return same."""
        encrypted = crypto.encrypt("test", field="email")
        double_encrypted = crypto.encrypt(encrypted, field="email")
        assert double_encrypted == encrypted

    def test_plaintext_passthrough_decrypt(self, crypto):
        """Decrypting unencrypted data should return as-is."""
        plaintext = "not encrypted"
        decrypted = crypto.decrypt(plaintext, field="email")
        assert decrypted == plaintext


class TestFieldIsolation:
    """Test that different fields produce different ciphertexts."""

    @pytest.fixture
    def crypto(self):
        return HouslerCrypto(master_key=TEST_KEY)

    def test_different_fields_different_ciphertext(self, crypto):
        """Same value with different fields should produce different ciphertexts."""
        plaintext = "test@example.com"
        encrypted_email = crypto.encrypt(plaintext, field="email")
        encrypted_phone = crypto.encrypt(plaintext, field="phone")

        # Should be different
        assert encrypted_email != encrypted_phone

        # But both should decrypt correctly
        assert crypto.decrypt(encrypted_email, field="email") == plaintext
        assert crypto.decrypt(encrypted_phone, field="phone") == plaintext

    def test_wrong_field_fails_decrypt(self, crypto):
        """Decrypting with wrong field should fail."""
        encrypted = crypto.encrypt("test", field="email")

        with pytest.raises(ValueError, match="Decryption failed"):
            crypto.decrypt(encrypted, field="phone")

    def test_same_field_different_random(self, crypto):
        """Same plaintext encrypted twice should produce different ciphertexts (random IV)."""
        plaintext = "test@example.com"
        encrypted1 = crypto.encrypt(plaintext, field="email")
        encrypted2 = crypto.encrypt(plaintext, field="email")

        # Ciphertexts should be different (different IV)
        assert encrypted1 != encrypted2

        # But both should decrypt to same value
        assert crypto.decrypt(encrypted1, field="email") == plaintext
        assert crypto.decrypt(encrypted2, field="email") == plaintext


class TestBlindIndex:
    """Test blind index (deterministic hash for search)."""

    @pytest.fixture
    def crypto(self):
        return HouslerCrypto(master_key=TEST_KEY)

    def test_deterministic(self, crypto):
        """Same input should always produce same hash."""
        value = "test@example.com"
        hash1 = crypto.blind_index(value, field="email")
        hash2 = crypto.blind_index(value, field="email")
        assert hash1 == hash2

    def test_hex_format(self, crypto):
        """Hash should be hex string."""
        hash_value = crypto.blind_index("test", field="email")
        assert len(hash_value) == 64  # 32 bytes = 64 hex chars
        int(hash_value, 16)  # Should be valid hex

    def test_case_insensitive(self, crypto):
        """Hash should be case-insensitive."""
        hash1 = crypto.blind_index("Test@Example.COM", field="email")
        hash2 = crypto.blind_index("test@example.com", field="email")
        assert hash1 == hash2

    def test_whitespace_normalized(self, crypto):
        """Hash should ignore leading/trailing whitespace."""
        hash1 = crypto.blind_index("  test@example.com  ", field="email")
        hash2 = crypto.blind_index("test@example.com", field="email")
        assert hash1 == hash2

    def test_different_fields_different_hash(self, crypto):
        """Same value with different fields should produce different hashes."""
        hash_email = crypto.blind_index("test", field="email")
        hash_phone = crypto.blind_index("test", field="phone")
        assert hash_email != hash_phone

    def test_empty_string(self, crypto):
        """Empty string should return empty string."""
        assert crypto.blind_index("", field="email") == ""


class TestIsEncrypted:
    """Test is_encrypted helper."""

    @pytest.fixture
    def crypto(self):
        return HouslerCrypto(master_key=TEST_KEY)

    def test_encrypted_value(self, crypto):
        """Should return True for encrypted values."""
        encrypted = crypto.encrypt("test", field="email")
        assert crypto.is_encrypted(encrypted) is True

    def test_plaintext_value(self, crypto):
        """Should return False for plaintext."""
        assert crypto.is_encrypted("test@example.com") is False

    def test_empty_value(self, crypto):
        """Should return False for empty string."""
        assert crypto.is_encrypted("") is False

    def test_none_value(self, crypto):
        """Should return False for None."""
        assert crypto.is_encrypted(None) is False


class TestCustomConfig:
    """Test custom configuration."""

    def test_custom_salt(self):
        """Different salt should produce different keys."""
        crypto1 = HouslerCrypto(master_key=TEST_KEY, salt="salt1")
        crypto2 = HouslerCrypto(master_key=TEST_KEY, salt="salt2")

        encrypted1 = crypto1.encrypt("test", field="email")

        # Should fail to decrypt with different salt
        with pytest.raises(ValueError):
            crypto2.decrypt(encrypted1, field="email")

    def test_custom_iterations(self):
        """Different iterations should produce different keys."""
        crypto1 = HouslerCrypto(master_key=TEST_KEY, iterations=1000)
        crypto2 = HouslerCrypto(master_key=TEST_KEY, iterations=2000)

        encrypted1 = crypto1.encrypt("test", field="email")

        # Should fail to decrypt with different iterations
        with pytest.raises(ValueError):
            crypto2.decrypt(encrypted1, field="email")


class TestCrossInstance:
    """Test that different instances with same key work together."""

    def test_different_instances_same_key(self):
        """Two instances with same key should interoperate."""
        crypto1 = HouslerCrypto(master_key=TEST_KEY)
        crypto2 = HouslerCrypto(master_key=TEST_KEY)

        encrypted = crypto1.encrypt("test", field="email")
        decrypted = crypto2.decrypt(encrypted, field="email")

        assert decrypted == "test"

    def test_blind_index_same_across_instances(self):
        """Blind index should be same across instances."""
        crypto1 = HouslerCrypto(master_key=TEST_KEY)
        crypto2 = HouslerCrypto(master_key=TEST_KEY)

        hash1 = crypto1.blind_index("test", field="email")
        hash2 = crypto2.blind_index("test", field="email")

        assert hash1 == hash2
