# Бэклог проекта housler-crypto

Единый источник правды для задач проекта housler-crypto.

**Последнее обновление:** 2026-01-11
**Источник:** Синхронизация с TEAM_TASKS.md

---

## Схема ID задач

Все задачи housler-crypto имеют префикс `HC-` для уникальности в экосистеме:
- `HC-TEST-XXX` — тестирование
- `HC-PUB-XXX` — публикация
- `HC-DOC-XXX` — документация
- `HC-INFRA-XXX` — инфраструктура

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
| Тестирование (HC-TEST) | 4 | 3 | 0 | 0 | 1 |
| Публикация (HC-PUB) | 2 | 0 | 0 | 2 | 0 |
| Документация (HC-DOC) | 3 | 1 | 0 | 0 | 2 |
| Инфраструктура (HC-INFRA) | 2 | 2 | 0 | 0 | 0 |
| **Итого** | **11** | **6** | **0** | **2** | **3** |

### Репозиторий
- **GitHub:** https://github.com/nikita-tita/housler-crypto
- **CI:** Все 8 jobs passing (lint + tests: Python 3.10-3.12, Node 18-22)
- **Release:** v1.0.0 создан (не опубликован в PyPI/npm)

---

## BLOCKER — Критические задачи

### HC-TEST-001: Тесты для Python
- **Статус:** `done`
- **Приоритет:** BLOCKER
- **Описание:** Криптографическая библиотека без тестов — критический риск
- **Путь:** `python/tests/`
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
  - [x] Coverage >= 90%
- **Артефакты:**
  - `python/tests/test_core.py` — 264 строки
  - `python/tests/test_utils.py` — 257 строк
  - `python/tests/test_migration.py` — 227 строк
  - 90 тестов passing
- **Завершено:** 2026-01-09

### HC-TEST-002: Тесты для TypeScript
- **Статус:** `done`
- **Приоритет:** BLOCKER
- **Путь:** `typescript/__tests__/`
- **DoD:**
  - [x] core.test.ts: encrypt/decrypt roundtrip
  - [x] core.test.ts: different fields = different ciphertexts
  - [x] core.test.ts: blind_index deterministic
  - [x] core.test.ts: invalid key handling
  - [x] utils.test.ts: masking functions
  - [x] Coverage >= 90%
- **Артефакты:**
  - `typescript/__tests__/core.test.ts`
  - `typescript/__tests__/utils.test.ts`
  - 57 тестов passing
- **Завершено:** 2026-01-09

---

## HIGH — Первый месяц

### HC-TEST-003: Cross-platform compatibility tests
- **Статус:** `todo`
- **Приоритет:** HIGH
- **Описание:** Убедиться что Python и TypeScript полностью совместимы
- **DoD:**
  - [ ] Тест: Python encrypt → TypeScript decrypt
  - [ ] Тест: TypeScript encrypt → Python decrypt
  - [ ] Тест: blind_index идентичен
  - [ ] Тест: одинаковый key → одинаковый derived key
  - [x] CI запускает оба языка (см. HC-TEST-004)
- **Сложность:** M (3-4 часа)
- **Примечание:** Требуется создать явный cross-platform тест

### HC-TEST-004: CI/CD Pipeline
- **Статус:** `done`
- **Приоритет:** HIGH
- **Описание:** CI для запуска тестов и линтинга
- **DoD:**
  - [x] .github/workflows/ci.yml создан
  - [x] Python: pytest + coverage (Python 3.10, 3.11, 3.12)
  - [x] TypeScript: jest + coverage (Node 18, 20, 22)
  - [x] Lint: ruff (Python), tsc --noEmit (TypeScript)
  - [x] CI полностью зелёный (все 8 jobs passing)
- **Артефакты:**
  - `.github/workflows/ci.yml` — тесты и линтинг
  - `.github/workflows/release.yml` — автопубликация при создании release
- **Завершено:** 2026-01-10

### HC-PUB-001: Публикация в PyPI
- **Статус:** `blocked`
- **Приоритет:** HIGH
- **Описание:** Библиотека не опубликована в PyPI
- **DoD:**
  - [x] pyproject.toml настроен
  - [x] Версия 1.0.0
  - [x] GitHub release v1.0.0 создан
  - [ ] Trusted Publisher настроен на PyPI
  - [ ] Загружено в PyPI (housler-crypto)
  - [ ] `pip install housler-crypto` работает
- **Блокер:** Требуется настроить PyPI Trusted Publishing:
  1. https://pypi.org/manage/account/publishing/
  2. Добавить publisher: owner=nikita-tita, repo=housler-crypto, workflow=release.yml, environment=release
- **Зависимости:** HC-TEST-001 (done)
- **Сложность:** S (15 минут ручной настройки)
- **Ответственный:** nikita-tita (владелец репо)

### HC-PUB-002: Публикация в npm
- **Статус:** `blocked`
- **Приоритет:** HIGH
- **Описание:** Библиотека не опубликована в npm
- **DoD:**
  - [x] package.json настроен
  - [x] Версия 1.0.0
  - [x] GitHub release v1.0.0 создан
  - [ ] NPM_TOKEN secret добавлен в GitHub
  - [ ] Загружено в npm (@housler/crypto)
  - [ ] `npm install @housler/crypto` работает
- **Блокер:** Требуется добавить NPM_TOKEN:
  1. Создать токен: https://www.npmjs.com/settings/tokens (Automation)
  2. `gh secret set NPM_TOKEN --repo nikita-tita/housler-crypto`
- **Зависимости:** HC-TEST-002 (done)
- **Сложность:** S (15 минут ручной настройки)
- **Ответственный:** nikita-tita (владелец репо)

---

## MEDIUM — Месяц 2-3

### HC-DOC-001: Примеры интеграции
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Добавить примеры для каждого проекта экосистемы
- **DoD:**
  - [ ] examples/agent-integration.ts
  - [ ] examples/lk-integration.py
  - [ ] examples/club-migration.py
  - [ ] README обновлён
- **Сложность:** S (2-3 часа)

### HC-DOC-002: API Reference
- **Статус:** `todo`
- **Приоритет:** MEDIUM
- **Описание:** Автоматически генерируемая документация
- **DoD:**
  - [ ] Python: sphinx или pdoc
  - [ ] TypeScript: typedoc
  - [ ] Hosted на GitHub Pages
- **Сложность:** S (2-3 часа)

### HC-DOC-003: CHANGELOG.md
- **Статус:** `done`
- **Приоритет:** MEDIUM
- **Описание:** Журнал изменений по версиям
- **DoD:**
  - [x] CHANGELOG.md создан
  - [x] Версия 1.0.0 описана
  - [x] Формат Keep a Changelog
- **Артефакты:**
  - `CHANGELOG.md`
- **Завершено:** 2026-01-11

### HC-INFRA-001: Версионирование
- **Статус:** `done`
- **Приоритет:** MEDIUM
- **Описание:** Система версионирования
- **DoD:**
  - [x] Semantic versioning (v1.0.0)
  - [x] Git tags для релизов
  - [x] GitHub Releases (v1.0.0 опубликован)
- **Артефакты:**
  - https://github.com/nikita-tita/housler-crypto/releases/tag/v1.0.0
- **Завершено:** 2026-01-10

### HC-INFRA-002: SECURITY.md
- **Статус:** `done`
- **Приоритет:** MEDIUM
- **Описание:** Процесс для security issues
- **DoD:**
  - [x] SECURITY.md создан
  - [x] Процесс responsible disclosure
  - [x] Контактный email для security (security@housler.ru)
- **Артефакты:**
  - `SECURITY.md`
- **Завершено:** 2026-01-11

---

## Архитектура

### Структура проекта

```
housler-crypto/
├── .github/workflows/
│   ├── ci.yml             # Тесты + линтинг
│   └── release.yml        # Автопубликация
├── python/
│   ├── housler_crypto/
│   │   ├── __init__.py
│   │   ├── core.py        # HouslerCrypto class
│   │   ├── utils.py       # Masking + normalization
│   │   └── migration.py   # Legacy format migration
│   ├── tests/
│   │   ├── test_core.py   # 90 тестов
│   │   ├── test_utils.py
│   │   └── test_migration.py
│   └── pyproject.toml
├── typescript/
│   ├── src/
│   │   └── index.ts       # Вся логика (TODO: разделить)
│   ├── __tests__/
│   │   ├── core.test.ts   # 57 тестов
│   │   └── utils.test.ts
│   └── package.json
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

При публикации HC-PUB-001/002 нужно интегрировать в:

| Проект | Задача интеграции | ID в TEAM_TASKS |
|--------|-------------------|-----------------|
| agent.housler.ru | Заменить encryption.ts | AG-CRYPTO-001 |
| lk.housler.ru | Заменить encryption.py | LK-CRYPTO-001 |
| club.housler.ru | Миграция с Fernet | (не запланировано) |

---

## Связи с экосистемными задачами

| Задача housler-crypto | Связанная задача экосистемы |
|-----------------------|---------------------------|
| HC-PUB-001, HC-PUB-002 | AG-CRYPTO-001, LK-CRYPTO-001 (blocked by) |
| HC-TEST-003 | — |
| HC-DOC-001 | — |

---

*Этот файл — источник правды для задач housler-crypto*
*Синхронизирован с TEAM_TASKS.md от 2026-01-11*
