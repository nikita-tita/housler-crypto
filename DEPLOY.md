# Deployment Guide - housler-crypto

## Overview

This repository contains shared libraries for the Housler ecosystem:

| Package | Type | Registry | Auto-publish |
|---------|------|----------|--------------|
| `housler-crypto` (Python) | Library | PyPI | On release |
| `@housler/crypto` (TypeScript) | Library | npm | On release |
| `@housler/auth` | Library | npm | On push to main |

## Automatic Publishing

### @housler/auth (Auto on push)

Changes to `auth/` directory trigger automatic publishing:

```
push to main (auth/**) → test → bump version → publish to npm
```

### Python/TypeScript crypto (On release)

```
create GitHub release → publish to PyPI + npm
```

## GitHub Secrets Required

Add these in: **Settings → Secrets and variables → Actions**

| Secret | Description | Where to get |
|--------|-------------|--------------|
| `NPM_TOKEN` | npm access token | npmjs.com → Access Tokens → Generate New Token (Automation) |

**Note:** PyPI uses trusted publishing (no token needed).

## Setup Instructions

### 1. Create npm Token

1. Go to https://www.npmjs.com/settings/YOUR_USERNAME/tokens
2. Click "Generate New Token" → "Automation"
3. Copy the token

### 2. Add GitHub Secret

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `NPM_TOKEN`
5. Value: paste the npm token
6. Click "Add secret"

### 3. Create GitHub Environment

1. Settings → Environments → New environment
2. Name: `release`
3. (Optional) Add protection rules

## Manual Publishing

### @housler/auth

```bash
cd auth
npm version patch  # or minor/major
npm publish --access public
```

### Python package

```bash
cd python
pip install build twine
python -m build
twine upload dist/*
```

### TypeScript package

```bash
cd typescript
npm run build
npm publish --access public
```

## Workflow Files

- `.github/workflows/ci.yml` - Tests on every push/PR
- `.github/workflows/publish-auth.yml` - Auto-publish auth on push to main
- `.github/workflows/release.yml` - Publish all packages on GitHub release

## Versioning

- `@housler/auth`: Auto-incremented patch version on each push
- Python/TypeScript crypto: Manual version bump before release

## Consuming Updates

After publishing, update in dependent projects:

```bash
# In lk or agent project
npm update @housler/auth
```

Or pin specific version in `package.json`:

```json
{
  "dependencies": {
    "@housler/auth": "^1.0.0"
  }
}
```
