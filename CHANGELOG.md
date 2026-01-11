# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Cross-platform compatibility tests (planned)
- Integration examples for agent/lk/club (planned)
- API reference documentation (planned)

## [1.0.0] - 2026-01-10

### Added

#### Core Encryption
- AES-256-GCM authenticated encryption
- Per-field key derivation using PBKDF2-SHA256 (100,000 iterations)
- Blind index for searchable encryption (BLAKE2b for Python, SHA256-HMAC for TypeScript)
- Cross-platform data format: `hc1:<base64-encoded-data>`

#### Python Package (`housler-crypto`)
- `HouslerCrypto` class with `encrypt()`, `decrypt()`, `blind_index()` methods
- `HouslerCrypto.generate_key()` for secure key generation
- Masking functions: `mask.email()`, `mask.phone()`, `mask.name()`, `mask.inn()`, `mask.card()`
- Phone normalization: `normalize_phone()`
- Validation functions: `validate_email()`, `validate_phone()`, `validate_inn()`

#### TypeScript Package (`@housler/crypto`)
- `HouslerCrypto` class with same API as Python
- `HouslerCrypto.generateKey()` for secure key generation
- Masking functions: `mask.email()`, `mask.phone()`, `mask.name()`
- Phone normalization: `normalizePhone()`

#### Migration Tools
- `FernetMigrator.from_lk_config()` - migrate from lk.housler.ru Fernet encryption
- `FernetMigrator.from_club_config()` - migrate from club.housler.ru Fernet encryption
- `FernetMigrator.from_agent_config()` - migrate from agent.housler.ru AES-GCM

#### Infrastructure
- CI/CD pipeline with GitHub Actions
- Python tests: 90 tests, coverage >= 90%
- TypeScript tests: 57 tests, coverage >= 90%
- Support for Python 3.10, 3.11, 3.12
- Support for Node.js 18, 20, 22
- Automated release workflow for PyPI and npm

### Security
- 152-FZ compliant encryption (Russian personal data protection law)
- Per-field key isolation prevents cross-field attacks
- Authenticated encryption prevents tampering
- No plaintext PII in logs (masking functions provided)

---

[Unreleased]: https://github.com/nikita-tita/housler-crypto/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nikita-tita/housler-crypto/releases/tag/v1.0.0
