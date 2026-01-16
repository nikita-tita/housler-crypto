# npm Publishing Setup

## Обзор

Публикация `@housler/crypto` на npm через GitHub Actions с использованием NPM_TOKEN.

## Шаги настройки

### 1. Создать npm аккаунт/организацию

Если организация `@housler` ещё не существует:

1. Зайти на https://www.npmjs.com
2. Sign Up или Log In
3. Создать организацию: https://www.npmjs.com/org/create
   - Name: `housler`
   - Type: Unlimited public packages (free)

### 2. Создать Access Token

1. Перейти: https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Нажать "Generate New Token" → "Classic Token"
3. Выбрать тип: **Automation** (для CI/CD)
4. Скопировать токен (показывается только один раз!)

### 3. Добавить NPM_TOKEN в GitHub Secrets

1. Перейти: https://github.com/nikita-tita/housler-crypto/settings/secrets/actions
2. Нажать "New repository secret"
3. Заполнить:
   ```
   Name:   NPM_TOKEN
   Value:  npm_xxxxxxxxxxxxxxxxxxxx
   ```
4. Нажать "Add secret"

### 4. Проверить workflow

Файл `.github/workflows/release.yml` уже настроен:

```yaml
publish-npm:
  runs-on: ubuntu-latest
  environment: release

  steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        registry-url: 'https://registry.npmjs.org'

    - name: Install dependencies
      working-directory: typescript
      run: npm ci

    - name: Build
      working-directory: typescript
      run: npm run build

    - name: Publish to npm
      working-directory: typescript
      run: npm publish --access public
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 5. Создать Release

После настройки секретов:

```bash
# Убедиться что версия в package.json обновлена
git tag v1.0.0
git push origin v1.0.0
```

Затем на GitHub → Releases → Create release → Publish

## Альтернатива: npm Granular Access Tokens

npm теперь поддерживает более безопасные granular tokens:

1. https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. "Generate New Token" → "Granular Access Token"
3. Настроить:
   - Token name: `github-actions-housler-crypto`
   - Expiration: 365 days (или по необходимости)
   - Packages: `@housler/crypto` only
   - Permissions: Read and write

## Troubleshooting

### Ошибка "403 Forbidden"

- Проверить что токен имеет права на публикацию
- Проверить что организация `@housler` существует
- Проверить `publishConfig.access: "public"` в package.json

### Ошибка "404 Not Found" при первой публикации

- Для scoped packages (`@housler/*`) нужен `--access public`
- Или организация должна быть оплачена для private packages

### Ошибка "Package name already exists"

- Проверить не занято ли имя пакета
- Увеличить версию в package.json

### Ошибка "You must be logged in"

- Проверить что NPM_TOKEN добавлен в secrets
- Проверить что environment `release` существует в GitHub

## Локальное тестирование

```bash
cd typescript

# Проверить что собирается
npm run build

# Проверить содержимое пакета (без публикации)
npm pack --dry-run

# Опубликовать локально для теста
npm publish --dry-run
```

## Версионирование

```bash
# Patch release (1.0.0 → 1.0.1)
npm version patch

# Minor release (1.0.0 → 1.1.0)
npm version minor

# Major release (1.0.0 → 2.0.0)
npm version major
```

## Ссылки

- [npm Access Tokens](https://docs.npmjs.com/creating-and-viewing-access-tokens)
- [Publishing scoped packages](https://docs.npmjs.com/creating-and-publishing-scoped-public-packages)
- [GitHub Actions + npm](https://docs.github.com/en/actions/publishing-packages/publishing-nodejs-packages)
