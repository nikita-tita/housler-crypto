# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in housler-crypto, please report it responsibly.

### How to Report

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please report security issues via email:

- **Email:** security@housler.ru
- **Subject:** `[SECURITY] housler-crypto: <brief description>`

### What to Include

Please provide:

1. **Description** of the vulnerability
2. **Steps to reproduce** (proof of concept if possible)
3. **Impact assessment** (what could an attacker do?)
4. **Affected versions**
5. **Suggested fix** (if you have one)

### Response Timeline

| Stage | Timeline |
|-------|----------|
| Initial response | Within 48 hours |
| Vulnerability assessment | Within 7 days |
| Fix development | Depends on severity |
| Public disclosure | After fix is released |

### Severity Levels

| Severity | Description | Response |
|----------|-------------|----------|
| **Critical** | Remote code execution, key disclosure | Immediate patch |
| **High** | Authentication bypass, data leak | Patch within 7 days |
| **Medium** | Information disclosure, DoS | Patch within 30 days |
| **Low** | Minor issues | Next scheduled release |

## Security Best Practices

When using housler-crypto:

1. **Store master key securely**
   - Use secrets management (HashiCorp Vault, AWS Secrets Manager, etc.)
   - Never commit keys to version control
   - Rotate keys periodically

2. **Use environment variables**
   ```bash
   export HOUSLER_CRYPTO_KEY=<your-64-char-hex-key>
   ```

3. **Never log plaintext PII**
   - Use provided masking functions for logs
   - Audit log outputs regularly

4. **Keep dependencies updated**
   ```bash
   # Python
   pip install --upgrade housler-crypto

   # TypeScript
   npm update @housler/crypto
   ```

5. **Validate inputs**
   - Use validation functions before encryption
   - Sanitize data at system boundaries

## Cryptographic Details

| Parameter | Value | Notes |
|-----------|-------|-------|
| Algorithm | AES-256-GCM | NIST approved |
| Key Derivation | PBKDF2-SHA256 | 100,000 iterations |
| IV Size | 96 bits | Random per encryption |
| Auth Tag | 128 bits | Tamper detection |
| Blind Index | BLAKE2b / SHA256-HMAC | Platform-specific |

## Compliance

This library is designed to help achieve compliance with:

- **152-FZ** (Russian Federal Law on Personal Data)
- **GDPR** (encryption of personal data)
- **PCI DSS** (encryption of cardholder data)

**Note:** Using this library alone does not guarantee compliance. You must implement appropriate organizational and technical measures.

## Acknowledgments

We appreciate responsible disclosure and will acknowledge security researchers who report valid vulnerabilities (unless they prefer to remain anonymous).

---

*Last updated: 2026-01-11*
