# Команда проекта HOUSLER-CRYPTO

## Проект: Криптографическая библиотека PII

**Тип:** Shared library (Python + TypeScript)
**Версия:** v1.0.0
**Статус:** Ready for publish (PyPI/npm blocked)

---

## Назначение

Единая библиотека для шифрования персональных данных (PII) в экосистеме Housler.
Обеспечивает compliance с 152-ФЗ.

**Используется в:**
- agent.housler.ru (TypeScript)
- lk.housler.ru (Python)

---

## Криптографические параметры

| Компонент | Алгоритм | Параметры |
|-----------|----------|-----------|
| Encryption | AES-256-GCM | IV: 96 bits, Tag: 128 bits |
| Key Derivation | PBKDF2-SHA256 | 100,000 iterations |
| Blind Index | BLAKE2b (Py) / SHA256-HMAC (TS) | 32 bytes |

**Формат данных:** `hc1:<base64-encoded-ciphertext>`

---

## Структура проекта

```
housler-crypto/
├── python/
│   ├── housler_crypto/
│   │   ├── core.py           # HouslerCrypto class
│   │   ├── utils.py          # Masking, normalization
│   │   └── migration.py      # Legacy Fernet migration
│   └── tests/
│       ├── test_core.py      # 50+ tests
│       └── test_utils.py
├── typescript/
│   ├── src/
│   │   └── index.ts          # HouslerCrypto class
│   └── __tests__/
│       └── core.test.ts      # 57 tests
├── .github/workflows/
│   ├── ci.yml                # Tests: Py 3.10-3.12, Node 18-22
│   └── release.yml           # Auto-publish on release
└── BACKLOG.md                # Задачи экосистемы
```

---

## Команда проекта

### BE-CRYPTO: Crypto Developer
**Роль:** Primary разработчик библиотеки

**Специализация:**
- Криптография (AES-GCM, PBKDF2, HMAC)
- Python cryptography library
- Node.js crypto module
- Cross-language compatibility

**Обязанности:**
- Поддержка Python и TypeScript реализаций
- Обеспечение совместимости между языками
- Security review криптографического кода
- Публикация в PyPI и npm

**Текущий фокус:** Настройка Trusted Publishing для PyPI/npm

---

### QA-CRYPTO: QA Engineer
**Роль:** Тестирование библиотеки

**Coverage требования:** ≥ 90%

**Тесты:**
- Unit tests (encrypt/decrypt roundtrip)
- Cross-language compatibility tests
- Edge cases (empty strings, unicode, large data)
- Migration tests (legacy Fernet)

---

## API

### Python
```python
from housler_crypto import HouslerCrypto

crypto = HouslerCrypto(encryption_key="...", salt="...")

# Encrypt
encrypted = crypto.encrypt("user@example.com")
# => "hc1:AbCdEf..."

# Decrypt
plaintext = crypto.decrypt(encrypted)

# Blind index (для поиска)
index = crypto.hash("user@example.com")

# Masking
masked = crypto.mask_email("user@example.com")
# => "u***@example.com"
```

### TypeScript
```typescript
import { HouslerCrypto } from 'housler-crypto';

const crypto = new HouslerCrypto({ encryptionKey: '...', salt: '...' });

const encrypted = crypto.encrypt('user@example.com');
const plaintext = crypto.decrypt(encrypted);
const index = crypto.hash('user@example.com');
```

---

## Совместимость

**КРИТИЧНО:** Python и TypeScript реализации ДОЛЖНЫ быть совместимы!

```python
# Зашифровано в Python
encrypted = python_crypto.encrypt("test")

# Расшифровано в TypeScript
plaintext = ts_crypto.decrypt(encrypted)
assert plaintext == "test"  # MUST PASS!
```

---

## Тестирование

```bash
# Python
cd python && pytest -v --cov=housler_crypto --cov-report=term-missing

# TypeScript
cd typescript && npm test -- --coverage

# Все тесты (CI)
# Запускается автоматически через GitHub Actions
```

---

## Definition of Done

- [ ] Тесты проходят (Python + TypeScript)
- [ ] Coverage ≥ 90%
- [ ] Cross-language compatibility verified
- [ ] Type hints / TypeScript types корректны
- [ ] Нет breaking changes в API
- [ ] CHANGELOG обновлён

---

## Публикация (блокеры)

### PyPI
- Требуется настройка Trusted Publishing
- Settings → Publishing → Add GitHub Actions publisher

### npm
- Требуется NPM_TOKEN в GitHub Secrets
- Settings → Secrets → Actions → NPM_TOKEN

---

## Запрещено

- Использовать слабые алгоритмы (MD5, SHA1, DES, ECB mode)
- Хардкодить ключи в коде
- Логировать plaintext PII
- Менять формат `hc1:...` без миграции
- Breaking changes без major version bump
