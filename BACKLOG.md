# Бэклог проекта housler-crypto

Единый источник правды для задач проекта.

**Последнее обновление:** 2026-01-10
**Источник:** Q1 2026 Ecosystem Review

---

## Статусы задач

| Статус | Описание |
|--------|----------|
| `backlog` | В очереди, не приоритизировано |
| `todo` | Готово к взятию в работу |
| `in_progress` | В работе (указан исполнитель) |
| `blocked` | Заблокировано (указан блокер) |
| `review` | На ревью/тестировании |
| `done` | Выполнено, есть артефакт |

---

## Сводка

| Категория | Всего | Done | In Progress | Blocked | Todo |
|-----------|-------|------|-------------|---------|------|
| Тестирование (TEST) | 4 | 3 | 0 | 0 | 1 |
| Публикация (PUB) | 2 | 0 | 0 | 0 | 2 |
| Документация (DOC) | 2 | 0 | 0 | 0 | 2 |
| Инфраструктура (INFRA) | 2 | 0 | 0 | 0 | 2 |
| **Итого** | **10** | **3** | **0** | **0** | **7** |

---

## BLOCKER — Критические задачи

### TEST-001: Добавить тесты для Python
- **Статус:** `done`
- **Приоритет:** BLOCKER
- **Связь:** ECO-TEST-001
- **Описание:** Криптографическая библиотека без тестов — критический риск
- **Путь:** `python/`
- **DoD:**
  - [x] test_core.py: encrypt/decrypt roundtrip
  - [x] test_core.py: different fields = different ciphertexts
  - [x] test_core.py: blind_index deterministic
  - [x] test_core.py: invalid key handling
  - [x] test_core.py: empty string handling
  - [x] test_utils.py: masking functions (email, phone, name, inn)
  - [x] test_utils.py: phone normalization
  - [x] test_migration.py: Fernet migration (from lk)
  - [x] test_migration.py: AES-GCM migration (from agent)
  - [ ] test_compat.py: cross-platform (Python ↔ TypeScript) — см. TEST-003
  - [x] Coverage >= 90%
- **Артефакты:**
  - `python/tests/test_core.py` — 264 строки
  - `python/tests/test_utils.py` — 257 строк
  - `python/tests/test_migration.py` — 227 строк
  - ~90 тестов
- **Завершено:** 2026-01-09
- **Ответственный:** Backend

### TEST-002: Добавить тесты для TypeScript
- **Статус:** `done`
- **Приоритет:** BLOCKER
- **Путь:** `typescript/`
- **DoD:**
  - [x] core.test.ts: encrypt/decrypt roundtrip
  - [x] core.test.ts: different fields = different ciphertexts
  - [x] core.test.ts: blind_index deterministic
  - [x] core.test.ts: invalid key handling
  - [x] utils.test.ts: masking functions
  - [ ] compat.test.ts: decrypt Python-encrypted data — см. TEST-003
  - [x] Coverage >= 90%
- **Артефакты:**
  - `typescript/__tests__/core.test.ts`
  - `typescript/__tests__/utils.test.ts`
  - 57 тестов passing
- **Завершено:** 2026-01-09

---

## HIGH — Первый месяц

### TEST-003: Cross-platform compatibility tests
- **Статус:** `todo`
- **Приоритет:** HIGH
- **Описание:** Убедиться что Python и TypeScript полностью совместимы
- **DoD:**
  - [ ] Тест: Python encrypt → TypeScript decrypt
  - [ ] Тест: TypeScript encrypt → Python decrypt
  - [ ] Тест: blind_index идентичен
  - [ ] Тест: одинаковый key → одинаковый derived key
  - [x] CI запускает оба языка (см. TEST-004)
- **Сложность:** M (3-4 часа)
- **Примечание:** Требуется создать явный cross-platform тест (compat.test.ts или test_compat.py)

### TEST-004: Настроить CI/CD
- **Статус:** `done`
- **Приоритет:** HIGH
- **Описание:** Нет CI для запуска тестов
- **DoD:**
  - [x] .github/workflows/ci.yml создан
  - [x] Python: pytest + coverage (Python 3.9-3.12)
  - [x] TypeScript: jest + coverage (Node 18, 20, 22)
  - [ ] Cross-platform tests — см. TEST-003
  - [x] Lint: ruff (Python), tsc --noEmit (TypeScript)
- **Артефакты:**
  - `.github/workflows/ci.yml` — тесты и линтинг
  - `.github/workflows/release.yml` — автопубликация
- **Завершено:** 2026-01-09

### PUB-001: Опубликовать в PyPI
- **Статус:** `todo`
- **Приоритет:** HIGH
- **Описание:** Библиотека не опубликована
- **DoD:**
  - [ ] pyproject.toml настроен
  - [ ] Версия 0.1.0
  - [ ] Загружено в PyPI (housler-crypto)
  - [ ] pip install housler-crypto работает
- **Зависимости:** TEST-001 (сначала тесты)
- **Сложность:** S (1-2 часа)

### PUB-002: Опубликовать в npm
- **Статус:** `todo`
- **Приоритет:** HIGH
- **Описание:** Библиотека не опубликована
- **DoD:**
  - [ ] package.json настроен
  - [ ] Версия 0.1.0
  - [ ] Загружено в npm (@housler/crypto)
  - [ ] npm install @housler/crypto работает
- **Зависимости:** TEST-002 (сначала тесты)
- **Сложность:** S (1-2 часа)

---

## MEDIUM — Месяц 2-3

### DOC-001: Примеры интеграции
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Добавить примеры для каждого проекта экосистемы
- **DoD:**
  - [ ] examples/agent-integration.ts
  - [ ] examples/lk-integration.py
  - [ ] examples/club-migration.py
  - [ ] README обновлён
- **Сложность:** S (2-3 часа)

### DOC-002: API Reference
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Автоматически генерируемая документация
- **DoD:**
  - [ ] Python: sphinx или pdoc
  - [ ] TypeScript: typedoc
  - [ ] Hosted на GitHub Pages
- **Сложность:** S (2-3 часа)

### INFRA-001: Версионирование
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Нет системы версионирования
- **DoD:**
  - [ ] CHANGELOG.md создан
  - [ ] Semantic versioning
  - [ ] Git tags для релизов
  - [ ] GitHub Releases
- **Сложность:** S (1 час)

### INFRA-002: Security advisory process
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Процесс для security issues
- **DoD:**
  - [ ] SECURITY.md создан
  - [ ] Процесс responsible disclosure
  - [ ] Контактный email для security
- **Сложность:** S (30 минут)

---

## Архитектура

### Структура

```
housler-crypto/
├── python/
│   ├── housler_crypto/
│   │   ├── __init__.py
│   │   ├── core.py        # HouslerCrypto class
│   │   ├── mask.py        # Masking functions
│   │   ├── normalize.py   # Phone normalization
│   │   └── migration.py   # Legacy format migration
│   ├── tests/             # TODO: создать
│   ├── pyproject.toml
│   └── README.md
├── typescript/
│   ├── src/
│   │   ├── index.ts
│   │   ├── core.ts        # HouslerCrypto class
│   │   ├── mask.ts        # Masking functions
│   │   └── normalize.ts   # Phone normalization
│   ├── __tests__/         # TODO: создать
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

### Формат данных

```
hc1:<base64-encoded-data>
```

Где base64 содержит:
- Version: 1 byte (0x01)
- IV: 12 bytes
- Auth Tag: 16 bytes
- Ciphertext: variable

### Криптографические параметры

| Параметр | Значение |
|----------|----------|
| Algorithm | AES-256-GCM |
| Key Derivation | PBKDF2-SHA256 |
| KDF Iterations | 100,000 |
| IV Size | 96 bits |
| Tag Size | 128 bits |
| Blind Index | BLAKE2b (Python) / SHA256-HMAC (TS) |

---

## Зависимые проекты

При изменении API нужно обновить:

| Проект | Файл | Статус интеграции |
|--------|------|-------------------|
| agent.housler.ru | `src/utils/encryption.ts` | Dual-read (hc1: + legacy) |
| lk.housler.ru | `app/core/encryption.py` | Dual-read (hc1: + Fernet) |
| club.housler.ru | `utils/encryption.py` | Dual-read (hc1: + Fernet) |

---

## Связи с другими бэклогами

| Экосистемная задача | Связанная задача |
|---------------------|------------------|
| ECO-TEST-001 | TEST-001, TEST-002 |
| ECO-ARCH-002 | PUB-001, PUB-002 |

---

*Этот файл — источник правды для задач housler-crypto*
