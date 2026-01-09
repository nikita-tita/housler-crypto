"""
Tests for legacy encryption migration.
"""

import pytest
from housler_crypto import HouslerCrypto, FernetMigrator


# Test keys
TEST_MASTER_KEY = "a" * 64
TEST_ENCRYPTION_KEY = "b" * 64
TEST_SALT = "test_salt_v1"


class TestFernetMigratorLk:
    """Test migration from lk-style Fernet encryption."""

    @pytest.fixture
    def migrator(self):
        """Create migrator for lk config."""
        return FernetMigrator.from_lk_config(
            encryption_key=TEST_ENCRYPTION_KEY,
            encryption_salt=TEST_SALT,
        )

    @pytest.fixture
    def new_crypto(self):
        """Create new HouslerCrypto instance."""
        return HouslerCrypto(master_key=TEST_MASTER_KEY)

    def test_encrypt_decrypt_roundtrip(self, migrator):
        """Should be able to decrypt what lk-style encrypts."""
        # First, encrypt with Fernet (simulating lk)
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64

        key_bytes = bytes.fromhex(TEST_ENCRYPTION_KEY)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=TEST_SALT.encode("utf-8"),
            iterations=100_000,
        )
        fernet_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        fernet = Fernet(fernet_key)

        plaintext = "test@example.com"
        encrypted = fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

        # Now decrypt with migrator
        decrypted = migrator.decrypt(encrypted, field="email")
        assert decrypted == plaintext

    def test_migrate_to_housler_crypto(self, migrator, new_crypto):
        """Should migrate from Fernet to HouslerCrypto."""
        # Encrypt with Fernet
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64

        key_bytes = bytes.fromhex(TEST_ENCRYPTION_KEY)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=TEST_SALT.encode("utf-8"),
            iterations=100_000,
        )
        fernet_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        fernet = Fernet(fernet_key)

        plaintext = "test@example.com"
        old_encrypted = fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

        # Migrate
        new_encrypted = migrator.migrate(old_encrypted, field="email", new_crypto=new_crypto)

        # Verify
        assert new_encrypted.startswith("hc1:")
        decrypted = new_crypto.decrypt(new_encrypted, field="email")
        assert decrypted == plaintext

    def test_already_migrated_passthrough(self, migrator, new_crypto):
        """Already migrated data should pass through."""
        encrypted = new_crypto.encrypt("test", field="email")
        result = migrator.migrate(encrypted, field="email", new_crypto=new_crypto)
        assert result == encrypted

    def test_empty_value(self, migrator, new_crypto):
        """Empty value should return empty."""
        assert migrator.migrate("", field="email", new_crypto=new_crypto) == ""

    def test_plaintext_passthrough(self, migrator):
        """Invalid Fernet token should be treated as plaintext."""
        result = migrator.decrypt("not encrypted", field="email")
        assert result == "not encrypted"


class TestFernetMigratorClub:
    """Test migration from club-style Fernet encryption."""

    @pytest.fixture
    def migrator(self):
        """Create migrator for club config."""
        return FernetMigrator.from_club_config(
            master_key=TEST_ENCRYPTION_KEY,
            salt="vas3k_club_pii_salt_v1",
        )

    @pytest.fixture
    def new_crypto(self):
        """Create new HouslerCrypto instance."""
        return HouslerCrypto(master_key=TEST_MASTER_KEY)

    def test_per_field_keys(self, migrator):
        """Club uses per-field keys - different fields should work."""
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64

        master_key = bytes.fromhex(TEST_ENCRYPTION_KEY)
        salt = "vas3k_club_pii_salt_v1".encode("utf-8")

        # Encrypt email field
        kdf_email = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt + b"email",
            iterations=100_000,
        )
        fernet_email = Fernet(base64.urlsafe_b64encode(kdf_email.derive(master_key)))
        encrypted_email = fernet_email.encrypt(b"test@example.com").decode("utf-8")

        # Encrypt phone field
        kdf_phone = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt + b"phone",
            iterations=100_000,
        )
        fernet_phone = Fernet(base64.urlsafe_b64encode(kdf_phone.derive(master_key)))
        encrypted_phone = fernet_phone.encrypt(b"+79991234567").decode("utf-8")

        # Decrypt with migrator
        assert migrator.decrypt(encrypted_email, field="email") == "test@example.com"
        assert migrator.decrypt(encrypted_phone, field="phone") == "+79991234567"

    def test_enc_prefix_handling(self, migrator):
        """Club uses enc: prefix - should be handled."""
        # The migrator strips enc: prefix before decrypting
        # This test just verifies the code path doesn't crash
        result = migrator.decrypt("enc:notvalid", field="email")
        # Invalid Fernet returns as-is
        assert result is not None


class TestMigrationFlow:
    """Test complete migration flow."""

    def test_full_migration_flow(self):
        """Test complete migration from lk to housler-crypto."""
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        import base64

        # Step 1: Create old data (simulating lk)
        old_key = "c" * 64
        old_salt = "old_salt"

        key_bytes = bytes.fromhex(old_key)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=old_salt.encode("utf-8"),
            iterations=100_000,
        )
        fernet_key = base64.urlsafe_b64encode(kdf.derive(key_bytes))
        fernet = Fernet(fernet_key)

        test_data = {
            "email": "user@example.com",
            "phone": "+79991234567",
            "name": "Иван Иванов",
        }

        old_encrypted = {}
        for field, value in test_data.items():
            old_encrypted[field] = fernet.encrypt(value.encode("utf-8")).decode("utf-8")

        # Step 2: Create migrator and new crypto
        migrator = FernetMigrator.from_lk_config(
            encryption_key=old_key,
            encryption_salt=old_salt,
        )
        new_crypto = HouslerCrypto(master_key=TEST_MASTER_KEY)

        # Step 3: Migrate all fields
        new_encrypted = {}
        for field in test_data:
            new_encrypted[field] = migrator.migrate(
                old_encrypted[field],
                field=field,
                new_crypto=new_crypto,
            )

        # Step 4: Verify
        for field, original_value in test_data.items():
            # New format
            assert new_encrypted[field].startswith("hc1:")
            # Can decrypt
            decrypted = new_crypto.decrypt(new_encrypted[field], field=field)
            assert decrypted == original_value


class TestMigratorNotConfigured:
    """Test error handling when migrator not properly configured."""

    def test_decrypt_without_config(self):
        """Should raise error when not configured."""
        migrator = FernetMigrator()

        with pytest.raises(ValueError, match="not configured"):
            migrator.decrypt("something", field="email")
