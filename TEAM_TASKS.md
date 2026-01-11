# Распределение задач по команде (экосистема Housler)

**Дата:** 2026-01-11
**Синхронизировано с:** BACKLOG.md (housler-crypto)

---

## Схема ID задач

Префиксы по проектам для уникальности:
- `HC-` — housler-crypto (см. BACKLOG.md)
- `AG-` — agent.housler.ru
- `LK-` — lk.housler.ru
- `SHARED-` — общая инфраструктура

---

## Сводка задач

| Приоритет | Всего | Done | In Progress | Blocked | Todo |
|-----------|-------|------|-------------|---------|------|
| HIGH | 10 | 6 | 3 | 2 | 0 |
| MEDIUM | 5 | 0 | 0 | 0 | 5 |
| LOW | 5 | 2 | 0 | 0 | 3 |
| **Итого** | **20** | **8** | **3** | **2** | **7** |

---

## HIGH Priority (10 задач)

### housler-crypto (HC-)

| ID | Задача | Effort | Статус | Ответственный |
|----|--------|--------|--------|---------------|
| HC-TEST-001 | Тесты Python | 6h | `done` | — |
| HC-TEST-002 | Тесты TypeScript | 4h | `done` | — |
| HC-TEST-004 | CI/CD Pipeline | 3h | `done` | — |
| HC-INFRA-001 | Версионирование | 1h | `done` | — |
| HC-PUB-001 | Публикация PyPI | 0.5h | `blocked` | nikita-tita |
| HC-PUB-002 | Публикация npm | 0.5h | `blocked` | nikita-tita |

### agent.housler.ru (AG-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| AG-TEST-001 | Тесты auth.service.ts | 6h | `in_progress` | Dev1 | Rev1 |
| AG-TEST-002 | Тесты encryption.ts | 3h | `in_progress` | Dev2 | Rev1 |
| AG-INFRA-001 | CI/CD для agent | 3h | `done` | — | — |

### lk.housler.ru (LK-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| LK-TEST-001 | Тесты auth (FastAPI) | 6h | `in_progress` | Dev3 | Rev1 |
| LK-INFRA-001 | CI/CD для lk | 3h | `in_progress` | Dev6 | Rev2 |

### Общая инфраструктура (SHARED-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| SHARED-INFRA-001 | Бэкапы PostgreSQL | 2h | `done` | — | — |

---

## MEDIUM Priority (5 задач)

### housler-crypto (HC-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| HC-TEST-003 | Cross-platform tests | 4h | `todo` | Dev7 | Rev1 |
| HC-DOC-001 | Примеры интеграции | 3h | `todo` | Dev4 | Rev3 |
| HC-DOC-002 | API Reference | 3h | `todo` | Dev4 | Rev3 |

### agent.housler.ru (AG-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| AG-CRYPTO-001 | Интеграция housler-crypto | 4h | `blocked` | Dev2 | Rev3 |
| AG-DOC-001 | ARCHITECTURE.md | 3h | `todo` | Dev6 | Rev3 |

### lk.housler.ru (LK-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| LK-CRYPTO-001 | Интеграция housler-crypto | 4h | `blocked` | Dev4 | Rev3 |

### Общая инфраструктура (SHARED-)

| ID | Задача | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|-----|----------|
| SHARED-INFRA-002 | Health endpoints | 2h | `todo` | Dev2 | Rev2 |

---

## LOW Priority (4 задачи)

| ID | Задача | Проект | Effort | Статус | Dev | Reviewer |
|----|--------|--------|--------|--------|-----|----------|
| HC-DOC-003 | CHANGELOG.md | housler-crypto | 0.5h | `done` | — | — |
| HC-INFRA-002 | SECURITY.md | housler-crypto | 0.5h | `done` | — | — |
| AG-DOC-002 | API Docs (Swagger) | agent | 4h | `todo` | Dev1 | Rev3 |
| LK-DOC-001 | API Docs (OpenAPI) | lk | 4h | `todo` | Dev3 | Rev3 |
| SHARED-INFRA-003 | Structured logging | all | 6h | `todo` | Dev5 | Rev2 |

---

## Распределение по разработчикам

| Dev | Специализация | Задачи | Статус |
|-----|---------------|--------|--------|
| **Dev1** | Frontend/TS | AG-TEST-001, AG-DOC-002 | AG-TEST-001 in progress |
| **Dev2** | Frontend/TS | AG-TEST-002, AG-CRYPTO-001, SHARED-INFRA-002 | AG-TEST-002 in progress |
| **Dev3** | Backend/Python | LK-TEST-001, LK-DOC-001 | LK-TEST-001 in progress |
| **Dev4** | Backend/Python | LK-CRYPTO-001, HC-DOC-001, HC-DOC-002 | Ждёт публикации |
| **Dev5** | DevOps | AG-INFRA-001, SHARED-INFRA-001, SHARED-INFRA-003 | AG-INFRA-001 in progress |
| **Dev6** | DevOps | LK-INFRA-001, AG-DOC-001 | LK-INFRA-001 in progress |
| **Dev7** | Crypto/Full-stack | HC-TEST-003 | Готов к работе |

---

## Распределение по ревьюерам

| Reviewer | Зона | Задачи |
|----------|------|--------|
| **Rev1** | Security & Tests | AG-TEST-001, AG-TEST-002, LK-TEST-001, HC-TEST-003 |
| **Rev2** | Infrastructure | AG-INFRA-001, LK-INFRA-001, SHARED-INFRA-*, HC-INFRA-002 |
| **Rev3** | Integration & Docs | AG-CRYPTO-001, LK-CRYPTO-001, *-DOC-* |

---

## Блокеры и зависимости

```
HC-PUB-001, HC-PUB-002 (blocked: требуется ручная настройка токенов)
         │
         ▼
AG-CRYPTO-001, LK-CRYPTO-001 (blocked by HC-PUB-*)
```

**Действия для разблокировки:**

1. **PyPI** (HC-PUB-001):
   - Владелец: nikita-tita
   - Действие: https://pypi.org/manage/account/publishing/ → Trusted Publisher
   - Параметры: owner=nikita-tita, repo=housler-crypto, workflow=release.yml

2. **npm** (HC-PUB-002):
   - Владелец: nikita-tita
   - Действие: создать токен на npmjs.com, затем:
   ```bash
   gh secret set NPM_TOKEN --repo nikita-tita/housler-crypto
   ```

---

## Порядок выполнения

### Этап 1 — Критический (сейчас)

| # | Задача | Dev | Блокирует |
|---|--------|-----|-----------|
| 1 | Настроить PyPI/npm токены | nikita-tita | HC-PUB-001, HC-PUB-002 |
| 2 | AG-INFRA-001 (CI/CD agent) | Dev5 | Все PR в agent |
| 3 | LK-INFRA-001 (CI/CD lk) | Dev6 | Все PR в lk |
| 4 | AG-TEST-001 (auth.service.ts) | Dev1 | — |
| 5 | AG-TEST-002 (encryption.ts) | Dev2 | — |
| 6 | LK-TEST-001 (auth lk) | Dev3 | — |

### Этап 2 — После CI и публикации

| # | Задача | Dev | Зависит от |
|---|--------|-----|------------|
| 7 | HC-PUB-001 (PyPI) | — | Токены |
| 8 | HC-PUB-002 (npm) | — | Токены |
| 9 | HC-TEST-003 (cross-platform) | Dev7 | — |
| 10 | SHARED-INFRA-001 (бэкапы) | Dev5 | — |

### Этап 3 — Интеграция

| # | Задача | Dev | Зависит от |
|---|--------|-----|------------|
| 11 | AG-CRYPTO-001 | Dev2 | HC-PUB-001, HC-PUB-002 |
| 12 | LK-CRYPTO-001 | Dev4 | HC-PUB-001, HC-PUB-002 |
| 13 | SHARED-INFRA-002 (health) | Dev2 | — |

### Этап 4 — Документация

| # | Задача | Dev |
|---|--------|-----|
| 14 | AG-DOC-001 (ARCHITECTURE.md) | Dev6 |
| 15 | HC-DOC-001 (примеры) | Dev4 |
| 16 | HC-DOC-002 (API Reference) | Dev4 |
| 17 | AG-DOC-002 (Swagger) | Dev1 |
| 18 | LK-DOC-001 (OpenAPI) | Dev3 |
| ~~19~~ | ~~HC-DOC-003 (CHANGELOG)~~ | done |
| ~~20~~ | ~~HC-INFRA-002 (SECURITY.md)~~ | done |
| 21 | SHARED-INFRA-003 (logging) | Dev5 |

---

## Связи с бэклогами проектов

| Проект | Файл бэклога | Префикс |
|--------|--------------|---------|
| housler-crypto | `BACKLOG.md` | HC- |
| agent | (отдельный репозиторий) | AG- |
| lk | (отдельный репозиторий) | LK- |
| shared | (этот файл) | SHARED- |

---

*Последнее обновление: 2026-01-11*
*Синхронизирован с housler-crypto/BACKLOG.md*
