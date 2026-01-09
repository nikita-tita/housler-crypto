# HOUSLER ECOSYSTEM REVIEW REPORT

**Дата:** 2026-01-09
**Автор:** Principal Engineer / Security & Architecture Reviewer

---

## EXECUTIVE SUMMARY

### Обзор экосистемы

Housler — распределённая экосистема из 6 проектов для недвижимости:

| Проект | Домен | Стек | Состояние |
|--------|-------|------|-----------|
| **agent.housler.ru** | CRM для агентов | Node.js/TypeScript + Next.js | Production |
| **lk.housler.ru** | Личный кабинет сделок | Python/FastAPI | Backend MVP |
| **club.housler.ru** | Сообщество (форк vas3k.club) | Django + Vue.js | Production |
| **calendar.housler.ru** | AI-календарь | Python/FastAPI + Telegram Bot | Production |
| **housler.ru** | Аналитика цен | Python/Flask | Production |
| **housler-crypto** | Криптобиблиотека | Python + TypeScript | Ready |

### Локальные пути проектов

| Проект | Локальный путь |
|--------|----------------|
| agent.housler.ru | `~/Desktop/housler_pervichka` |
| lk.housler.ru | `~/Desktop/lk` |
| club.housler.ru | `~/Desktop/club/vas3k.club` |
| calendar.housler.ru | `~/Desktop/AI-Calendar-Project/ai-calendar-assistant` |
| housler.ru | `~/Desktop/cian-analyzer` |
| housler-crypto | `~/Desktop/housler-crypto` |

### Ключевые метрики

```
ПРОБЛЕМЫ ПО КРИТИЧНОСТИ:
┌──────────────────────────────────────────────────────────────────┐
│ BLOCKER:   4  │ Скомпрометированные секреты, пароли в README    │
│ HIGH:     12  │ Отсутствие тестов, Redis без пароля             │
│ MEDIUM:   15  │ N+1 queries, отсутствие CI/CD, документация     │
│ LOW:       8  │ Code style, health checks, logging              │
└──────────────────────────────────────────────────────────────────┘
```

### Главные риски

1. **SEC-001: Скомпрометированные секреты** — .env файлы были в git, пароли в README (calendar)
2. **SEC-002: Shared secrets между сервисами** — JWT_SECRET и ENCRYPTION_KEY одинаковые в agent и lk
3. **TEST-001: Критически низкое покрытие тестами** — auth.service.ts и encryption.ts без тестов
4. **ARCH-001: Tight coupling через shared DB** — lk напрямую подключается к БД agent

### Рекомендация

**Приоритет 1:** Немедленная ротация всех скомпрометированных секретов и очистка git history.

---

## PROBLEM CLUSTERS

### Cluster 1: SECURITY — Безопасность (4 BLOCKER + 5 HIGH)

```
СКОМПРОМЕТИРОВАНО:
┌─────────────────────────────────────────────────────────────┐
│ calendar.housler.ru README.md содержит:                     │
│   - Root пароль сервера: $SERVER_PASSWORD                   │
│   - IP сервера: 95.163.227.26                               │
│   - SSH команды с паролем в открытом виде                   │
├─────────────────────────────────────────────────────────────┤
│ agent.housler.ru:                                           │
│   - .env был в git (JWT_SECRET, ENCRYPTION_KEY, DB_PASSWORD)│
│   - YANDEX_GPT_API_KEY скомпрометирован                     │
├─────────────────────────────────────────────────────────────┤
│ lk.housler.ru:                                              │
│   - requirements.txt: локальный путь `-e file:///...`       │
│   - Shared secrets с agent (cross-service vulnerability)    │
├─────────────────────────────────────────────────────────────┤
│ Все проекты:                                                │
│   - Redis без пароля (port 6379 внутренний, но риск)        │
└─────────────────────────────────────────────────────────────┘
```

### Cluster 2: TESTING — Тестирование (8 HIGH)

```
ПОКРЫТИЕ ТЕСТАМИ:
┌────────────────────────┬────────────┬──────────────────────┐
│ Проект                 │ Coverage   │ Критичные файлы      │
├────────────────────────┼────────────┼──────────────────────┤
│ agent.housler.ru       │ ~10%       │ auth.service.ts: 0%  │
│                        │            │ encryption.ts: 0%    │
├────────────────────────┼────────────┼──────────────────────┤
│ lk.housler.ru          │ 0%         │ auth/service.py: 0%  │
│                        │            │ encryption.py: 0%    │
├────────────────────────┼────────────┼──────────────────────┤
│ club.housler.ru        │ ~40%       │ Значительно улучшено │
├────────────────────────┼────────────┼──────────────────────┤
│ calendar.housler.ru    │ <5%        │ Минимальное          │
├────────────────────────┼────────────┼──────────────────────┤
│ housler-crypto         │ ~70%       │ Хорошо покрыто       │
└────────────────────────┴────────────┴──────────────────────┘
```

### Cluster 3: ARCHITECTURE — Архитектура (3 HIGH + 4 MEDIUM)

```
ПРОБЛЕМЫ СВЯЗНОСТИ:

   agent.housler.ru <──────── lk.housler.ru
   (Auth Provider)    shared   (Tight coupling!)
        │             secrets
        │             shared DB
        v
   housler_agent DB <────────────────────────────┐
   (PostgreSQL)       direct connection          │
                      no API layer               │
                                                 │
   club.housler.ru ─────────────────────────────>│
   (Separate DB)      vas3k_club DB              │

   calendar.housler.ru ──────────────────────────>│
   (JSON files)       No proper DB!

РИСКИ:
- lk подключается напрямую к БД agent — миграции конфликтуют
- JWT_SECRET shared — компрометация одного = компрометация обоих
- calendar хранит данные в JSON файлах — нет ACID
```

### Cluster 4: INFRASTRUCTURE — Инфраструктура (6 MEDIUM)

```
ПРОБЛЕМЫ:
┌──────────────────────────────────────────────────────────────┐
│ CI/CD:                                                        │
│   - agent: нет CI/CD                                         │
│   - lk: нет CI/CD                                            │
│   - club: GitHub Actions настроен, но StrictHostKeyChecking   │
│   - calendar: нет CI/CD                                      │
│   - housler-crypto: нет CI/CD                                │
├──────────────────────────────────────────────────────────────┤
│ Monitoring:                                                   │
│   - Только club имеет Prometheus + Grafana                   │
│   - Health endpoints: частичные                              │
│   - Centralized logging: отсутствует                         │
├──────────────────────────────────────────────────────────────┤
│ Backups:                                                      │
│   - club: pg_dump каждые 24h                                 │
│   - agent/lk: НЕТ автоматических бэкапов!                    │
└──────────────────────────────────────────────────────────────┘
```

### Cluster 5: CODE QUALITY — Качество кода (5 MEDIUM + 5 LOW)

```
ПРОБЛЕМЫ:
┌──────────────────────────────────────────────────────────────┐
│ Линтеры/Форматтеры:                                          │
│   - agent: ESLint настроен частично                          │
│   - lk: black, flake8, mypy в requirements, не в CI          │
│   - club: pre-commit настроен                                │
│   - housler-crypto: ruff + mypy (Python), нет ESLint (TS)    │
├──────────────────────────────────────────────────────────────┤
│ Type Safety:                                                  │
│   - agent: TypeScript strict, но много `any`                 │
│   - lk: Pydantic schemas, SQLAlchemy models                  │
│   - housler-crypto: строгий TypeScript                       │
├──────────────────────────────────────────────────────────────┤
│ Документация:                                                 │
│   - README: есть во всех проектах                            │
│   - API docs: отсутствует Swagger/OpenAPI                    │
│   - ARCHITECTURE.md: отсутствует                             │
└──────────────────────────────────────────────────────────────┘
```

---

## PROBLEM CARDS

### [SEC-001] Скомпрометированные секреты в git

| Поле | Значение |
|------|----------|
| **Критичность** | BLOCKER |
| **Проект** | agent.housler.ru, lk.housler.ru, calendar.housler.ru |
| **Файлы** | `.env`, `README.md`, `DEPLOY.md` |
| **Описание** | Секреты (JWT_SECRET, ENCRYPTION_KEY, DB_PASSWORD, root пароль) были закоммичены в git и/или опубликованы в README |
| **Impact** | Полный доступ к серверу, базам данных, возможность подделки JWT токенов |
| **DoD** | 1) Все секреты ротированы 2) Git history очищена 3) .gitignore обновлён 4) Secrets manager внедрён |
| **Effort** | M (4-8 часов) |

### [SEC-002] Shared secrets между сервисами

| Поле | Значение |
|------|----------|
| **Критичность** | BLOCKER |
| **Проект** | agent.housler.ru, lk.housler.ru |
| **Файлы** | `.env.example` оба проекта |
| **Описание** | JWT_SECRET и ENCRYPTION_KEY одинаковые в обоих проектах. Комментарии в .env.example предупреждают, но на практике используются общие |
| **Impact** | Компрометация одного сервиса = компрометация обоих |
| **DoD** | 1) Уникальные JWT_SECRET для каждого сервиса 2) Cross-service auth через OAuth2/OIDC 3) Документация обновлена |
| **Effort** | L (1-2 дня) |

### [SEC-003] Hardcoded пароли в документации

| Поле | Значение |
|------|----------|
| **Критичность** | BLOCKER |
| **Проект** | calendar.housler.ru |
| **Файлы** | `README.md:151-167` |
| **Описание** | Root пароль сервера в открытом виде в README вместе с командами деплоя |
| **Impact** | Любой с доступом к репозиторию имеет root-доступ к серверу |
| **DoD** | 1) Пароль изменён 2) SSH-ключ как единственный метод 3) README очищен 4) Git history очищена |
| **Effort** | S (1-2 часа) |

### [SEC-004] Redis без аутентификации

| Поле | Значение |
|------|----------|
| **Критичность** | HIGH |
| **Проект** | agent.housler.ru, lk.housler.ru |
| **Файлы** | `docker-compose.prod.yml` |
| **Описание** | Redis работает без пароля. Хотя порт не экспортирован наружу, это нарушает defense-in-depth |
| **Impact** | При компрометации Docker network — полный доступ к кешу и сессиям |
| **DoD** | 1) REDIS_PASSWORD добавлен 2) `--requirepass` в docker-compose 3) URL обновлён в коде |
| **Effort** | S (30 минут) |

### [TEST-001] Auth service без тестов

| Поле | Значение |
|------|----------|
| **Критичность** | HIGH |
| **Проект** | agent.housler.ru |
| **Файлы** | `backend/src/services/auth.service.ts` |
| **Описание** | Критический путь авторизации (SMS коды, JWT токены) не покрыт тестами. Auth используется другими проектами (lk) |
| **Impact** | Изменения могут сломать авторизацию во всей экосистеме |
| **DoD** | 1) Unit tests 80%+ coverage 2) Integration tests 3) CI запускает тесты |
| **Effort** | M (4-6 часов) |

### [TEST-002] Encryption без тестов

| Поле | Значение |
|------|----------|
| **Критичность** | HIGH |
| **Проект** | agent.housler.ru, lk.housler.ru |
| **Файлы** | `encryption.ts`, `encryption.py` |
| **Описание** | PII шифрование (152-ФЗ compliance) не тестируется. Нет тестов совместимости форматов |
| **Impact** | Риск потери данных при изменениях, проблемы миграции |
| **DoD** | 1) Unit tests 90%+ coverage 2) Cross-platform compatibility tests 3) Migration tests |
| **Effort** | S (2-3 часа на проект) |

### [ARCH-001] Shared database без API layer

| Поле | Значение |
|------|----------|
| **Критичность** | HIGH |
| **Проект** | agent.housler.ru, lk.housler.ru |
| **Файлы** | `lk/docker-compose.prod.yml` (external network) |
| **Описание** | lk подключается напрямую к PostgreSQL agent через Docker network. Нет API границы, миграции могут конфликтовать |
| **Impact** | Изменение схемы в одном проекте ломает другой. Нет версионирования контракта |
| **DoD** | 1) API layer для shared data 2) Документация shared tables 3) Migration coordination process |
| **Effort** | XL (2-3 недели) |

### [ARCH-002] housler-crypto не интегрирован

| Поле | Значение |
|------|----------|
| **Критичность** | MEDIUM |
| **Проект** | Все проекты |
| **Файлы** | `housler-crypto/` |
| **Описание** | Библиотека готова, но: 1) Не опубликована в npm/PyPI 2) lk использует локальный путь 3) agent имеет свою реализацию |
| **Impact** | Дублирование кода, риск несовместимости форматов |
| **DoD** | 1) Публикация в npm + PyPI 2) Интеграция во все проекты 3) Миграция данных |
| **Effort** | L (1-2 недели) |

### [INFRA-001] Отсутствие CI/CD

| Поле | Значение |
|------|----------|
| **Критичность** | MEDIUM |
| **Проект** | agent, lk, calendar, housler-crypto |
| **Файлы** | `.github/workflows/` (отсутствует) |
| **Описание** | Нет автоматического тестирования, линтинга, деплоя |
| **Impact** | Ручной деплой подвержен ошибкам, тесты не запускаются |
| **DoD** | 1) GitHub Actions для всех проектов 2) Lint -> Test -> Build -> Deploy 3) Coverage gates |
| **Effort** | M (2-4 часа на проект) |

### [INFRA-002] Нет автоматических бэкапов

| Поле | Значение |
|------|----------|
| **Критичность** | HIGH |
| **Проект** | agent.housler.ru, lk.housler.ru |
| **Файлы** | N/A |
| **Описание** | PostgreSQL БД не бэкапятся автоматически. Только club имеет скрипты бэкапов |
| **Impact** | Потеря данных при сбое |
| **DoD** | 1) pg_dump cron job 2) Retention policy (7 дней) 3) Offsite backup 4) Restore test |
| **Effort** | M (2-4 часа) |

---

## FIX PLAN — Roadmap

### Sprint 1: BLOCKER (Неделя 1)

```
ДЕНЬ 1-2: Ротация секретов
┌──────────────────────────────────────────────────────────────┐
│ [ ] Сменить root пароль сервера                              │
│ [ ] Настроить SSH-only (disable password auth)               │
│ [ ] Ротировать JWT_SECRET в agent -> обновить lk             │
│ [ ] Ротировать ENCRYPTION_KEY (ВНИМАНИЕ: миграция данных!)   │
│ [ ] Ротировать DB_PASSWORD                                   │
│ [ ] Отозвать YANDEX_GPT_API_KEY, создать новый               │
│ [ ] Перезапустить все сервисы                                │
└──────────────────────────────────────────────────────────────┘

ДЕНЬ 3: Очистка git history
┌──────────────────────────────────────────────────────────────┐
│ [ ] BFG Repo-Cleaner: удалить .env из истории                │
│ [ ] Удалить пароли из README/DEPLOY.md                       │
│ [ ] Force push (координация с командой!)                     │
│ [ ] Уведомить разработчиков о re-clone                       │
└──────────────────────────────────────────────────────────────┘

ДЕНЬ 4-5: Redis + Secrets Manager
┌──────────────────────────────────────────────────────────────┐
│ [ ] Добавить REDIS_PASSWORD во все проекты                   │
│ [ ] Настроить 1Password CLI или HashiCorp Vault              │
│ [ ] Документировать secrets management                       │
└──────────────────────────────────────────────────────────────┘
```

### Sprint 2: HIGH (Неделя 2-3)

```
ТЕСТИРОВАНИЕ:
┌──────────────────────────────────────────────────────────────┐
│ [ ] TEST-001: Тесты для auth.service.ts (agent)              │
│ [ ] TEST-002: Тесты для encryption.ts (agent)                │
│ [ ] TEST-003: Тесты для auth/service.py (lk)                 │
│ [ ] TEST-004: Тесты для encryption.py (lk)                   │
│ [ ] TEST-005: Cross-platform encryption compatibility        │
└──────────────────────────────────────────────────────────────┘

CI/CD:
┌──────────────────────────────────────────────────────────────┐
│ [ ] INFRA-001: GitHub Actions для agent                      │
│ [ ] INFRA-001: GitHub Actions для lk                         │
│ [ ] INFRA-001: GitHub Actions для housler-crypto             │
│ [ ] INFRA-002: Автоматические бэкапы PostgreSQL              │
└──────────────────────────────────────────────────────────────┘
```

### Sprint 3: MEDIUM (Неделя 4-6)

```
HOUSLER-CRYPTO INTEGRATION:
┌──────────────────────────────────────────────────────────────┐
│ [ ] Публикация в PyPI                                        │
│ [ ] Публикация в npm                                         │
│ [ ] Интеграция в agent (заменить свою реализацию)            │
│ [ ] Интеграция в lk (убрать локальный путь)                  │
│ [ ] Миграция данных на hc1: формат                           │
└──────────────────────────────────────────────────────────────┘

ARCHITECTURE IMPROVEMENTS:
┌──────────────────────────────────────────────────────────────┐
│ [ ] Документировать shared database contract                 │
│ [ ] Создать API layer для auth (или OAuth2)                  │
│ [ ] Health check endpoints для всех сервисов                 │
│ [ ] Structured logging (winston/structlog)                   │
└──────────────────────────────────────────────────────────────┘
```

---

## LOCAL DEVELOPMENT SETUP — Архитектура workspace

Рекомендуется **workspace approach** вместо монорепо:

### Структура

```
~/housler-workspace/
├── .env.shared                    # Shared environment vars
├── docker-compose.shared.yml      # Shared infrastructure (postgres, redis)
├── Makefile                       # Orchestration commands
├── README.md                      # Workspace documentation
│
├── agent.housler.ru/              # symlink -> ~/Desktop/housler_pervichka
├── lk.housler.ru/                 # symlink -> ~/Desktop/lk
├── club.housler.ru/               # symlink -> ~/Desktop/club/vas3k.club
├── calendar.housler.ru/           # symlink -> ~/Desktop/AI-Calendar-Project
├── housler.ru/                    # symlink -> ~/Desktop/cian-analyzer
└── housler-crypto/                # symlink -> ~/Desktop/housler-crypto
```

### Makefile

```makefile
# ~/housler-workspace/Makefile

.PHONY: setup start stop logs

# Setup workspace
setup:
	ln -sf ~/Desktop/housler_pervichka agent.housler.ru
	ln -sf ~/Desktop/lk lk.housler.ru
	ln -sf ~/Desktop/club/vas3k.club club.housler.ru
	ln -sf ~/Desktop/AI-Calendar-Project/ai-calendar-assistant calendar.housler.ru
	ln -sf ~/Desktop/cian-analyzer housler.ru
	ln -sf ~/Desktop/housler-crypto housler-crypto

# Start shared infrastructure
infra-up:
	docker compose -f docker-compose.shared.yml up -d

# Start all services (development)
dev:
	@echo "Starting agent..."
	cd agent.housler.ru && npm run dev &
	@echo "Starting lk..."
	cd lk.housler.ru && uvicorn app.main:app --reload &
	@echo "Starting club..."
	cd club.housler.ru && docker compose up -d

# Stop all
stop:
	docker compose -f docker-compose.shared.yml down
	pkill -f "npm run dev" || true
	pkill -f "uvicorn" || true
```

### docker-compose.shared.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: housler-postgres
    environment:
      POSTGRES_USER: housler
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - housler-network

  redis:
    image: redis:7-alpine
    container_name: housler-redis
    command: redis-server --requirepass ${REDIS_PASSWORD}
    ports:
      - "6379:6379"
    networks:
      - housler-network

  minio:
    image: minio/minio
    container_name: housler-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    networks:
      - housler-network

volumes:
  postgres_data:
  minio_data:

networks:
  housler-network:
    driver: bridge
    name: housler_network
```

### Преимущества подхода

- Каждый проект остаётся независимым git репозиторием
- Общая инфраструктура (DB, Redis, MinIO) запускается один раз
- Проекты "видят" друг друга через Docker network
- housler-crypto используется как локальная зависимость:
  - Python: `pip install -e ../housler-crypto/python`
  - TypeScript: `npm link ../housler-crypto/typescript`
- Нет риска сломать один проект изменениями в другом
- Простой переход — ничего не нужно мигрировать

---

## PROJECT MANAGER VIEW — Декомпозиция задач

### EPIC 1: Security Remediation (BLOCKER)

**Срок:** 1 неделя | **Owner:** DevOps/Security

| Task ID | Название | Проект | Приоритет | Effort | Зависимости |
|---------|----------|--------|-----------|--------|-------------|
| SEC-001a | Сменить root пароль сервера | Infrastructure | BLOCKER | 30m | - |
| SEC-001b | Отключить password auth SSH | Infrastructure | BLOCKER | 15m | SEC-001a |
| SEC-001c | Ротация JWT_SECRET в agent | agent | BLOCKER | 1h | - |
| SEC-001d | Обновить JWT_SECRET в lk | lk | BLOCKER | 30m | SEC-001c |
| SEC-001e | Миграция ENCRYPTION_KEY | agent, lk | BLOCKER | 4h | SEC-001c |
| SEC-001f | Ротация DB_PASSWORD | Infrastructure | BLOCKER | 1h | - |
| SEC-001g | Отозвать Yandex API Key | agent | BLOCKER | 30m | - |
| SEC-002a | BFG очистка git history (agent) | agent | BLOCKER | 1h | SEC-001* |
| SEC-002b | BFG очистка git history (lk) | lk | BLOCKER | 1h | SEC-001* |
| SEC-002c | Очистка README (calendar) | calendar | BLOCKER | 30m | SEC-001a |
| SEC-003a | Redis пароль в agent | agent | HIGH | 30m | - |
| SEC-003b | Redis пароль в lk | lk | HIGH | 30m | - |
| SEC-004 | Настройка 1Password CLI | Infrastructure | HIGH | 2h | SEC-002* |

### EPIC 2: Testing Infrastructure (HIGH)

**Срок:** 2 недели | **Owner:** Backend Team

| Task ID | Название | Проект | Приоритет | Effort | Зависимости |
|---------|----------|--------|-----------|--------|-------------|
| TEST-001 | Jest setup + CI (agent) | agent | HIGH | 2h | - |
| TEST-002 | Тесты auth.service.ts | agent | HIGH | 6h | TEST-001 |
| TEST-003 | Тесты encryption.ts | agent | HIGH | 3h | TEST-001 |
| TEST-004 | API integration tests | agent | HIGH | 8h | TEST-002 |
| TEST-005 | pytest setup + CI (lk) | lk | HIGH | 2h | - |
| TEST-006 | Тесты auth/service.py | lk | HIGH | 6h | TEST-005 |
| TEST-007 | Тесты encryption.py | lk | HIGH | 3h | TEST-005 |
| TEST-008 | Cross-platform encryption tests | housler-crypto | HIGH | 4h | - |

### EPIC 3: housler-crypto Integration (MEDIUM)

**Срок:** 2 недели | **Owner:** Backend Team

| Task ID | Название | Проект | Приоритет | Effort | Зависимости |
|---------|----------|--------|-----------|--------|-------------|
| CRYPTO-001 | Публикация в PyPI | housler-crypto | MEDIUM | 2h | TEST-008 |
| CRYPTO-002 | Публикация в npm | housler-crypto | MEDIUM | 2h | TEST-008 |
| CRYPTO-003 | Интеграция в agent | agent | MEDIUM | 4h | CRYPTO-002 |
| CRYPTO-004 | Интеграция в lk | lk | MEDIUM | 4h | CRYPTO-001 |
| CRYPTO-005 | Миграция данных agent -> hc1: | agent | MEDIUM | 4h | CRYPTO-003 |
| CRYPTO-006 | Миграция данных lk -> hc1: | lk | MEDIUM | 4h | CRYPTO-004 |

### EPIC 4: CI/CD & Infrastructure (MEDIUM)

**Срок:** 2 недели | **Owner:** DevOps

| Task ID | Название | Проект | Приоритет | Effort | Зависимости |
|---------|----------|--------|-----------|--------|-------------|
| INFRA-001 | GitHub Actions (agent) | agent | MEDIUM | 3h | TEST-001 |
| INFRA-002 | GitHub Actions (lk) | lk | MEDIUM | 3h | TEST-005 |
| INFRA-003 | GitHub Actions (housler-crypto) | housler-crypto | MEDIUM | 2h | - |
| INFRA-004 | PostgreSQL backup script | Infrastructure | HIGH | 2h | - |
| INFRA-005 | Health endpoints (agent) | agent | MEDIUM | 1h | - |
| INFRA-006 | Health endpoints (lk) | lk | MEDIUM | 1h | - |
| INFRA-007 | Structured logging (agent) | agent | LOW | 3h | - |
| INFRA-008 | Structured logging (lk) | lk | LOW | 3h | - |

### EPIC 5: Architecture Documentation (LOW)

**Срок:** 2 недели | **Owner:** Tech Lead

| Task ID | Название | Проект | Приоритет | Effort | Зависимости |
|---------|----------|--------|-----------|--------|-------------|
| DOC-001 | ARCHITECTURE.md (agent) | agent | LOW | 3h | - |
| DOC-002 | SHARED_DATABASE.md | agent/lk | MEDIUM | 2h | - |
| DOC-003 | API Documentation (Swagger) | agent | LOW | 4h | - |
| DOC-004 | API Documentation (OpenAPI) | lk | LOW | 4h | - |
| DOC-005 | Workspace setup guide | housler-workspace | LOW | 2h | - |

---

## SUMMARY

### Найдено проблем

```
┌─────────────────────────────────────────────────────────────────┐
│  BLOCKER: 4    │ Скомпрометированные секреты, пароли            │
│  HIGH:   12    │ Тесты, Redis, бэкапы                           │
│  MEDIUM: 15    │ CI/CD, интеграция, документация                │
│  LOW:     8    │ Logging, code style                            │
├─────────────────────────────────────────────────────────────────┤
│  ВСЕГО:  39 проблем                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Положительные моменты

- housler-crypto — отличная криптобиблиотека (1113 LOC, 0 dependencies в TS)
- club.housler.ru — 98/99 задач выполнено, хорошее покрытие тестами
- Единый дизайн-система (черно-белая, Inter font)
- 152-ФЗ compliance в crypto layer
- Хорошая документация (CLAUDE.md, BACKLOG.md во всех проектах)

### Следующие шаги

1. **Немедленно (сегодня):** Сменить root пароль, удалить из README
2. **Эта неделя:** Полная ротация секретов + BFG cleanup
3. **Следующие 2 недели:** Тестирование critical paths
4. **Месяц 2:** housler-crypto integration + CI/CD

---

## ТЕХНОЛОГИЧЕСКИЙ СТЕК (сводка)

### agent.housler.ru

- **Backend:** Node.js + Express + TypeScript
- **Frontend:** Next.js 16 + React 19
- **Database:** PostgreSQL 15 + PostGIS + pgvector
- **Cache:** Redis 7
- **Auth:** JWT + SMS (SMS.RU)
- **Encryption:** AES-256-GCM (dual-format)

### lk.housler.ru

- **Backend:** Python 3.11 + FastAPI
- **Database:** PostgreSQL 15 (shared with agent)
- **Cache:** Redis 7
- **Storage:** MinIO (S3-compatible)
- **Auth:** JWT (from agent) + Email
- **Encryption:** housler-crypto (local path)

### club.housler.ru

- **Backend:** Django 4.x
- **Frontend:** Vue.js + Webpack
- **Database:** PostgreSQL 14
- **Cache:** Redis 7
- **Real-time:** Centrifugo
- **Queue:** Celery + Redis

### calendar.housler.ru

- **Backend:** Python + FastAPI
- **Bot:** python-telegram-bot v21
- **Calendar:** Radicale CalDAV
- **AI:** Yandex GPT
- **Storage:** JSON files (!)

### housler.ru (cian-analyzer)

- **Backend:** Python + Flask 3.0
- **Scraping:** Playwright + BeautifulSoup
- **Cache:** Redis
- **Metrics:** Prometheus

### housler-crypto

- **Python:** cryptography >= 41.0.0
- **TypeScript:** Node.js crypto (built-in)
- **Algorithm:** AES-256-GCM + PBKDF2
- **Format:** `hc1:<base64>`

---

**Конец отчёта**

*Сгенерировано: 2026-01-09*
