# Housler Crypto

Unified PII encryption library for the Housler ecosystem. Compliant with Russian 152-FZ personal data protection law.

## Features

- **AES-256-GCM** authenticated encryption
- **Per-field key derivation** from master key (PBKDF2-SHA256)
- **Blind index** for searchable encryption (BLAKE2b/SHA256-HMAC)
- **Cross-platform** - Python and TypeScript with compatible formats
- **Migration tools** for legacy Fernet encryption

## Installation

### Python

```bash
pip install housler-crypto
# or
pip install -e /path/to/housler-crypto/python
```

### TypeScript/Node.js

```bash
npm install @housler/crypto
# or
npm install /path/to/housler-crypto/typescript
```

## Usage

### Generate a Master Key

```python
# Python
from housler_crypto import HouslerCrypto
print(HouslerCrypto.generate_key())
# Output: 64-character hex string
```

```typescript
// TypeScript
import { HouslerCrypto } from '@housler/crypto';
console.log(HouslerCrypto.generateKey());
// Output: 64-character hex string
```

### Encrypt/Decrypt PII

```python
# Python
from housler_crypto import HouslerCrypto

crypto = HouslerCrypto(master_key="your-64-char-hex-key")

# Encrypt
encrypted_email = crypto.encrypt("user@example.com", field="email")
encrypted_phone = crypto.encrypt("+79991234567", field="phone")

# Decrypt
email = crypto.decrypt(encrypted_email, field="email")
phone = crypto.decrypt(encrypted_phone, field="phone")
```

```typescript
// TypeScript
import { HouslerCrypto } from '@housler/crypto';

const crypto = new HouslerCrypto({ masterKey: 'your-64-char-hex-key' });

// Encrypt
const encryptedEmail = crypto.encrypt('user@example.com', 'email');
const encryptedPhone = crypto.encrypt('+79991234567', 'phone');

// Decrypt
const email = crypto.decrypt(encryptedEmail, 'email');
const phone = crypto.decrypt(encryptedPhone, 'phone');
```

### Blind Index for Search

Blind index allows searching encrypted data without decryption:

```python
# Python
from housler_crypto import HouslerCrypto

crypto = HouslerCrypto(master_key="your-key")

# Create blind index for search
email_hash = crypto.blind_index("user@example.com", field="email")

# Store encrypted email + hash in database:
# INSERT INTO users (email_encrypted, email_hash) VALUES (?, ?)

# Search by hash:
# SELECT * FROM users WHERE email_hash = ?
search_hash = crypto.blind_index("user@example.com", field="email")
# search_hash == email_hash (deterministic)
```

### Masking for Logs

```python
# Python
from housler_crypto import mask

print(mask.email("user@example.com"))  # us***@example.com
print(mask.phone("+79991234567"))      # +7***4567
print(mask.name("Иван Иванов"))        # Ив*** Ив***
print(mask.inn("7707083893"))          # 77***3893
print(mask.card("4111111111111111"))   # **** **** **** 1111
```

```typescript
// TypeScript
import { mask } from '@housler/crypto';

console.log(mask.email('user@example.com'));  // us***@example.com
console.log(mask.phone('+79991234567'));      // +7***4567
console.log(mask.name('Иван Иванов'));        // Ив*** Ив***
```

### Phone Normalization

```python
# Python
from housler_crypto import normalize_phone

normalize_phone("+7 (999) 123-45-67")  # "79991234567"
normalize_phone("8-999-123-45-67")     # "79991234567"
normalize_phone("9991234567")          # "79991234567"
```

## Migration from Legacy Encryption

### From lk (Fernet with single key)

```python
from housler_crypto import HouslerCrypto, FernetMigrator

# Old encryption config from lk project
old_migrator = FernetMigrator.from_lk_config(
    encryption_key="your-old-encryption-key",
    encryption_salt="your-old-salt"
)

# New HouslerCrypto instance
new_crypto = HouslerCrypto(master_key="new-64-char-hex-key")

# Migrate single value
new_encrypted = old_migrator.migrate(
    old_encrypted_email,
    field="email",
    new_crypto=new_crypto
)
```

### From club (Fernet with per-field keys)

```python
from housler_crypto import HouslerCrypto, FernetMigrator

old_migrator = FernetMigrator.from_club_config(
    master_key="your-old-master-key"
)

new_crypto = HouslerCrypto(master_key="new-64-char-hex-key")

# Migrate
new_encrypted = old_migrator.migrate(old_value, field="email", new_crypto=new_crypto)
```

### From agent (AES-GCM direct)

```python
from housler_crypto import HouslerCrypto, FernetMigrator

old_migrator = FernetMigrator.from_agent_config(
    encryption_key="your-old-agent-key"
)

new_crypto = HouslerCrypto(master_key="new-64-char-hex-key")

# Migrate
new_encrypted = old_migrator.migrate(old_value, field="email", new_crypto=new_crypto)
```

## Environment Variables

```bash
# Master key (required)
HOUSLER_CRYPTO_KEY=<64-hex-characters>

# Optional: custom salt (default: housler_crypto_v1)
HOUSLER_CRYPTO_SALT=your_custom_salt

# Optional: PBKDF2 iterations (default: 100000)
HOUSLER_CRYPTO_ITERATIONS=100000
```

## Data Format

Encrypted data format: `hc1:<base64-encoded-data>`

Where base64-encoded data contains:
- Version: 1 byte (0x01 for GCM)
- IV: 12 bytes (96 bits)
- Auth Tag: 16 bytes (128 bits)
- Ciphertext: variable length

This format is compatible between Python and TypeScript implementations.

## Security Notes

1. **Store master key securely** - use secrets management (Vault, AWS Secrets Manager, etc.)
2. **Use per-field encryption** - each field type gets a unique derived key
3. **Blind index is deterministic** - same input = same hash (enables search, but leaks equality)
4. **Never log plaintext PII** - use masking functions for logging
5. **Rotate keys periodically** - migrate data when rotating master key

## 152-FZ Compliance

This library helps achieve compliance with Russian Federal Law 152-FZ:

- ✅ AES-256 encryption (approved cryptographic algorithm)
- ✅ Per-field key isolation
- ✅ Authenticated encryption (GCM mode)
- ✅ PII masking for logs
- ✅ Searchable encryption without decryption

## License

MIT
