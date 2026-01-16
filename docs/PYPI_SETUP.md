# PyPI Trusted Publishing Setup

## Обзор

PyPI Trusted Publishing позволяет публиковать пакеты через GitHub Actions без секретных токенов. Используется OIDC (OpenID Connect) для аутентификации.

## Шаги настройки

### 1. Создать проект на PyPI (если не существует)

1. Зайти на https://pypi.org
2. Войти или зарегистрироваться
3. Проект создастся автоматически при первой публикации

### 2. Настроить Trusted Publishing на PyPI

1. Перейти: https://pypi.org/manage/account/publishing/
2. Нажать "Add a new pending publisher" (для нового проекта)

   Или если проект уже существует:
   - https://pypi.org/manage/project/housler-crypto/settings/publishing/

3. Заполнить форму:
   ```
   PyPI Project Name: housler-crypto
   Owner:             nikita-tita
   Repository name:   housler-crypto
   Workflow name:     release.yml
   Environment name:  release
   ```

4. Нажать "Add"

### 3. Создать GitHub Environment

1. Перейти: https://github.com/nikita-tita/housler-crypto/settings/environments
2. Нажать "New environment"
3. Имя: `release`
4. (Опционально) Добавить protection rules:
   - Required reviewers
   - Deployment branches: `main` only

### 4. Проверить workflow

Файл `.github/workflows/release.yml` уже настроен:

```yaml
jobs:
  publish-python:
    runs-on: ubuntu-latest
    environment: release          # ← Совпадает с PyPI
    permissions:
      id-token: write             # ← Обязательно для OIDC

    steps:
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: python/dist/
```

### 5. Создать Release

```bash
# Убедиться что версия в pyproject.toml обновлена
git tag v1.0.0
git push origin v1.0.0

# Затем на GitHub:
# 1. Releases → Create new release
# 2. Choose tag: v1.0.0
# 3. Generate release notes
# 4. Publish release
```

## Troubleshooting

### Ошибка "Trusted publishing not configured"

- Проверить что имя workflow точно совпадает: `release.yml`
- Проверить что environment name точно: `release`
- Проверить owner/repo: `nikita-tita/housler-crypto`

### Ошибка "Invalid OIDC token"

- Добавить `id-token: write` в permissions
- Проверить что используется `@release/v1` версия action

### Ошибка "Package already exists"

- Увеличить версию в `pyproject.toml`
- Удалить старый release и создать новый с новой версией

## TestPyPI (для тестирования)

Для тестирования можно сначала опубликовать на TestPyPI:

1. Настроить Trusted Publishing на https://test.pypi.org
2. Добавить в workflow:

```yaml
- name: Publish to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
    packages-dir: python/dist/
```

## Ссылки

- [PyPI Trusted Publishing Docs](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
