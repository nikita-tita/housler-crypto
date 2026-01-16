# Housler Crypto - AI Instructions

## Project Overview

Unified PII encryption library for Housler ecosystem (152-FZ compliant).

**Tech Stack:**
- Python 3.10+ (cryptography, blake3)
- TypeScript/Node.js 18+ (native crypto)
- Jest (TS tests), pytest (Python tests)
- GitHub Actions CI/CD

## Key Files

- `python/housler_crypto/core.py` - Main encryption class
- `typescript/src/index.ts` - TypeScript implementation
- `python/housler_crypto/migration.py` - Legacy Fernet migration
- `team/TASKS_*.md` - Current tasks

## Commands

```bash
# Python
cd python && pip install -e . && pytest

# TypeScript
cd typescript && npm install && npm test

# Both
npm run build && pytest
```

## Current Blockers

1. **PUBLISH-001**: PyPI Trusted Publishing not configured
2. **PUBLISH-002**: NPM_TOKEN secret missing

## Skills Available

Skills в `.claude/skills/`:

| Skill | Use Case |
|-------|----------|
| `python-packaging` | PyPI publishing, pyproject.toml |
| `python-testing-patterns` | pytest, fixtures, mocking |
| `async-python-patterns` | asyncio, concurrent code |
| `github-actions-templates` | CI/CD workflows |
| `javascript-testing-patterns` | Jest, Testing Library |
| `typescript-advanced-types` | Generics, utility types |

## Coding Standards

- Python: Black, isort, flake8
- TypeScript: ESLint, Prettier
- Commits: Conventional Commits format
- Coverage: >= 90%

## Security Rules

1. Never hardcode encryption keys
2. Use environment variables for secrets
3. Mask PII in logs (use `mask.*` functions)
4. Per-field key derivation required
