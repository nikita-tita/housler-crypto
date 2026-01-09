/**
 * Tests for core HouslerCrypto encryption/decryption.
 */

import { HouslerCrypto } from '../src/index';

// Test key (32 bytes = 64 hex chars)
const TEST_KEY = 'a'.repeat(64);

describe('HouslerCrypto', () => {
  describe('initialization', () => {
    it('should accept valid 64-char hex key', () => {
      const crypto = new HouslerCrypto({ masterKey: TEST_KEY });
      expect(crypto).toBeDefined();
    });

    it('should reject empty key', () => {
      expect(() => new HouslerCrypto({ masterKey: '' })).toThrow('masterKey is required');
    });

    it('should reject key with wrong length', () => {
      expect(() => new HouslerCrypto({ masterKey: 'a'.repeat(32) })).toThrow('must be 64 hex characters');
    });

    it('should generate valid 64-char hex key', () => {
      const key = HouslerCrypto.generateKey();
      expect(key.length).toBe(64);
      // Verify it's valid hex
      expect(() => Buffer.from(key, 'hex')).not.toThrow();
      // Verify it can be used
      const crypto = new HouslerCrypto({ masterKey: key });
      expect(crypto).toBeDefined();
    });
  });

  describe('encrypt/decrypt', () => {
    let crypto: HouslerCrypto;

    beforeEach(() => {
      crypto = new HouslerCrypto({ masterKey: TEST_KEY });
    });

    it('should encrypt and decrypt basic string', () => {
      const plaintext = 'test@example.com';
      const encrypted = crypto.encrypt(plaintext, 'email');
      const decrypted = crypto.decrypt(encrypted, 'email');
      expect(decrypted).toBe(plaintext);
    });

    it('should handle unicode (Cyrillic)', () => {
      const plaintext = 'Иван Иванов';
      const encrypted = crypto.encrypt(plaintext, 'name');
      const decrypted = crypto.decrypt(encrypted, 'name');
      expect(decrypted).toBe(plaintext);
    });

    it('should handle special characters', () => {
      const plaintext = 'test+special@exam-ple.com';
      const encrypted = crypto.encrypt(plaintext, 'email');
      const decrypted = crypto.decrypt(encrypted, 'email');
      expect(decrypted).toBe(plaintext);
    });

    it('should handle long text', () => {
      const plaintext = 'A'.repeat(10000);
      const encrypted = crypto.encrypt(plaintext, 'data');
      const decrypted = crypto.decrypt(encrypted, 'data');
      expect(decrypted).toBe(plaintext);
    });

    it('should return empty string for empty input', () => {
      expect(crypto.encrypt('', 'email')).toBe('');
      expect(crypto.decrypt('', 'email')).toBe('');
    });

    it('should have hc1: prefix', () => {
      const encrypted = crypto.encrypt('test', 'email');
      expect(encrypted.startsWith('hc1:')).toBe(true);
    });

    it('should be idempotent (not double encrypt)', () => {
      const encrypted = crypto.encrypt('test', 'email');
      const doubleEncrypted = crypto.encrypt(encrypted, 'email');
      expect(doubleEncrypted).toBe(encrypted);
    });

    it('should pass through plaintext on decrypt', () => {
      const plaintext = 'not encrypted';
      const decrypted = crypto.decrypt(plaintext, 'email');
      expect(decrypted).toBe(plaintext);
    });
  });

  describe('field isolation', () => {
    let crypto: HouslerCrypto;

    beforeEach(() => {
      crypto = new HouslerCrypto({ masterKey: TEST_KEY });
    });

    it('should produce different ciphertexts for different fields', () => {
      const plaintext = 'test@example.com';
      const encryptedEmail = crypto.encrypt(plaintext, 'email');
      const encryptedPhone = crypto.encrypt(plaintext, 'phone');

      expect(encryptedEmail).not.toBe(encryptedPhone);

      // Both should decrypt correctly
      expect(crypto.decrypt(encryptedEmail, 'email')).toBe(plaintext);
      expect(crypto.decrypt(encryptedPhone, 'phone')).toBe(plaintext);
    });

    it('should fail to decrypt with wrong field', () => {
      const encrypted = crypto.encrypt('test', 'email');

      expect(() => crypto.decrypt(encrypted, 'phone')).toThrow('Decryption failed');
    });

    it('should produce different ciphertexts for same plaintext (random IV)', () => {
      const plaintext = 'test@example.com';
      const encrypted1 = crypto.encrypt(plaintext, 'email');
      const encrypted2 = crypto.encrypt(plaintext, 'email');

      expect(encrypted1).not.toBe(encrypted2);

      // Both should decrypt to same value
      expect(crypto.decrypt(encrypted1, 'email')).toBe(plaintext);
      expect(crypto.decrypt(encrypted2, 'email')).toBe(plaintext);
    });
  });

  describe('blindIndex', () => {
    let crypto: HouslerCrypto;

    beforeEach(() => {
      crypto = new HouslerCrypto({ masterKey: TEST_KEY });
    });

    it('should be deterministic', () => {
      const value = 'test@example.com';
      const hash1 = crypto.blindIndex(value, 'email');
      const hash2 = crypto.blindIndex(value, 'email');
      expect(hash1).toBe(hash2);
    });

    it('should return hex string of 64 chars', () => {
      const hash = crypto.blindIndex('test', 'email');
      expect(hash.length).toBe(64);
      // Verify it's valid hex
      expect(() => Buffer.from(hash, 'hex')).not.toThrow();
    });

    it('should be case insensitive', () => {
      const hash1 = crypto.blindIndex('Test@Example.COM', 'email');
      const hash2 = crypto.blindIndex('test@example.com', 'email');
      expect(hash1).toBe(hash2);
    });

    it('should normalize whitespace', () => {
      const hash1 = crypto.blindIndex('  test@example.com  ', 'email');
      const hash2 = crypto.blindIndex('test@example.com', 'email');
      expect(hash1).toBe(hash2);
    });

    it('should produce different hashes for different fields', () => {
      const hashEmail = crypto.blindIndex('test', 'email');
      const hashPhone = crypto.blindIndex('test', 'phone');
      expect(hashEmail).not.toBe(hashPhone);
    });

    it('should return empty string for empty input', () => {
      expect(crypto.blindIndex('', 'email')).toBe('');
    });
  });

  describe('isEncrypted', () => {
    let crypto: HouslerCrypto;

    beforeEach(() => {
      crypto = new HouslerCrypto({ masterKey: TEST_KEY });
    });

    it('should return true for encrypted values', () => {
      const encrypted = crypto.encrypt('test', 'email');
      expect(crypto.isEncrypted(encrypted)).toBe(true);
    });

    it('should return false for plaintext', () => {
      expect(crypto.isEncrypted('test@example.com')).toBe(false);
    });

    it('should return false for empty string', () => {
      expect(crypto.isEncrypted('')).toBe(false);
    });
  });

  describe('custom config', () => {
    it('should produce different keys with different salt', () => {
      const crypto1 = new HouslerCrypto({ masterKey: TEST_KEY, salt: 'salt1' });
      const crypto2 = new HouslerCrypto({ masterKey: TEST_KEY, salt: 'salt2' });

      const encrypted1 = crypto1.encrypt('test', 'email');

      // Should fail to decrypt with different salt
      expect(() => crypto2.decrypt(encrypted1, 'email')).toThrow('Decryption failed');
    });

    it('should produce different keys with different iterations', () => {
      const crypto1 = new HouslerCrypto({ masterKey: TEST_KEY, iterations: 1000 });
      const crypto2 = new HouslerCrypto({ masterKey: TEST_KEY, iterations: 2000 });

      const encrypted1 = crypto1.encrypt('test', 'email');

      // Should fail to decrypt with different iterations
      expect(() => crypto2.decrypt(encrypted1, 'email')).toThrow('Decryption failed');
    });
  });

  describe('cross-instance', () => {
    it('should work across different instances with same key', () => {
      const crypto1 = new HouslerCrypto({ masterKey: TEST_KEY });
      const crypto2 = new HouslerCrypto({ masterKey: TEST_KEY });

      const encrypted = crypto1.encrypt('test', 'email');
      const decrypted = crypto2.decrypt(encrypted, 'email');

      expect(decrypted).toBe('test');
    });

    it('should produce same blind index across instances', () => {
      const crypto1 = new HouslerCrypto({ masterKey: TEST_KEY });
      const crypto2 = new HouslerCrypto({ masterKey: TEST_KEY });

      const hash1 = crypto1.blindIndex('test', 'email');
      const hash2 = crypto2.blindIndex('test', 'email');

      expect(hash1).toBe(hash2);
    });
  });
});
