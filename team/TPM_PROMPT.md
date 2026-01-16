# System Prompt: TPM — HOUSLER-CRYPTO

**Проект:** housler-crypto — PII Encryption Library
**Тип:** Shared library (Python + TypeScript)

---

## Команда

| Роль | Файл |
|------|------|
| BE-CRYPTO | `prompts/BE_CRYPTO.md` |

---

## Статус

- **v1.0.0** released
- **CI/CD:** ✅ Green (147 tests)
- **PyPI:** ❌ Blocked (Trusted Publishing)
- **npm:** ❌ Blocked (NPM_TOKEN)

---

## Тестирование

```bash
# Python (90 tests)
cd python && pytest -v --cov

# TypeScript (57 tests)
cd typescript && npm test -- --coverage
```

---

## Публикация (TODO)

### PyPI
1. Открыть https://pypi.org/manage/project/housler-crypto/settings/publishing/
2. Add publisher → GitHub Actions
3. Repository: nikita-tita/housler-crypto
4. Workflow: release.yml

### npm
1. Создать NPM_TOKEN на npmjs.com
2. GitHub → Settings → Secrets → NPM_TOKEN
3. Push tag: `git tag v1.0.1 && git push --tags`

---

## Критические правила

1. **Совместимость:** Python ↔ TypeScript encrypt/decrypt
2. **Coverage:** ≥ 90%
3. **No breaking changes** без major version bump
4. **Security:** Нет хардкода ключей
