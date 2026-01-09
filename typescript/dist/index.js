"use strict";
/**
 * Housler Crypto - Unified PII Encryption for 152-FZ Compliance
 *
 * TypeScript implementation compatible with Python version.
 *
 * Features:
 * - AES-256-GCM authenticated encryption
 * - Per-field key derivation (PBKDF2-SHA256)
 * - BLAKE2b keyed blind index for searchable encryption
 * - Cross-platform format (compatible with Python version)
 *
 * Usage:
 *   import { HouslerCrypto, mask, normalizePhone } from '@housler/crypto';
 *
 *   const crypto = new HouslerCrypto({ masterKey: '<64-hex-chars>' });
 *
 *   // Encrypt PII
 *   const encrypted = crypto.encrypt('user@example.com', 'email');
 *
 *   // Decrypt
 *   const decrypted = crypto.decrypt(encrypted, 'email');
 *
 *   // Blind index for search
 *   const hashValue = crypto.blindIndex('user@example.com', 'email');
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.mask = exports.HouslerCrypto = void 0;
exports.normalizePhone = normalizePhone;
exports.normalizeEmail = normalizeEmail;
const crypto_1 = __importDefault(require("crypto"));
// Constants matching Python implementation
const VERSION_GCM = 0x01;
const IV_LENGTH = 12; // 96 bits for GCM
const TAG_LENGTH = 16; // 128 bits
const KEY_LENGTH = 32; // 256 bits
const ENCRYPTED_PREFIX = 'hc1:'; // housler-crypto v1
/**
 * Unified PII encryption service for Housler ecosystem.
 *
 * Uses AES-256-GCM with per-field key derivation.
 */
class HouslerCrypto {
    masterKey;
    salt;
    iterations;
    keyCache = new Map();
    constructor(options) {
        if (!options.masterKey) {
            throw new Error('masterKey is required');
        }
        if (options.masterKey.length !== KEY_LENGTH * 2) {
            throw new Error(`masterKey must be ${KEY_LENGTH * 2} hex characters`);
        }
        this.masterKey = Buffer.from(options.masterKey, 'hex');
        this.salt = Buffer.from(options.salt ?? 'housler_crypto_v1', 'utf-8');
        this.iterations = options.iterations ?? 100_000;
    }
    /**
     * Derive a field-specific key from master key using PBKDF2.
     */
    deriveKey(field) {
        const cached = this.keyCache.get(field);
        if (cached) {
            return cached;
        }
        const fieldSalt = Buffer.concat([
            this.salt,
            Buffer.from(':'),
            Buffer.from(field, 'utf-8'),
        ]);
        const derivedKey = crypto_1.default.pbkdf2Sync(this.masterKey, fieldSalt, this.iterations, KEY_LENGTH, 'sha256');
        this.keyCache.set(field, derivedKey);
        return derivedKey;
    }
    /**
     * Encrypt data using AES-256-GCM.
     *
     * @param plaintext - Data to encrypt
     * @param field - Field name for key derivation (e.g., "email", "phone")
     * @returns Encrypted string with "hc1:" prefix
     */
    encrypt(plaintext, field = 'default') {
        if (!plaintext) {
            return '';
        }
        // Skip if already encrypted
        if (plaintext.startsWith(ENCRYPTED_PREFIX)) {
            return plaintext;
        }
        const key = this.deriveKey(field);
        const iv = crypto_1.default.randomBytes(IV_LENGTH);
        const cipher = crypto_1.default.createCipheriv('aes-256-gcm', key, iv, {
            authTagLength: TAG_LENGTH,
        });
        const encrypted = Buffer.concat([
            cipher.update(plaintext, 'utf8'),
            cipher.final(),
        ]);
        const tag = cipher.getAuthTag();
        // Pack: version (1) + iv (12) + tag (16) + ciphertext
        const packed = Buffer.concat([
            Buffer.from([VERSION_GCM]),
            iv,
            tag,
            encrypted,
        ]);
        return ENCRYPTED_PREFIX + packed.toString('base64');
    }
    /**
     * Decrypt data encrypted with AES-256-GCM.
     *
     * @param ciphertext - Encrypted string (with "hc1:" prefix)
     * @param field - Field name for key derivation
     * @returns Decrypted plaintext
     */
    decrypt(ciphertext, field = 'default') {
        if (!ciphertext) {
            return '';
        }
        // Not encrypted (legacy data)
        if (!ciphertext.startsWith(ENCRYPTED_PREFIX)) {
            return ciphertext;
        }
        try {
            const encoded = ciphertext.slice(ENCRYPTED_PREFIX.length);
            const packed = Buffer.from(encoded, 'base64');
            // Minimum size check
            if (packed.length < 1 + IV_LENGTH + TAG_LENGTH + 1) {
                throw new Error('Ciphertext too short');
            }
            const version = packed[0];
            if (version !== VERSION_GCM) {
                throw new Error(`Unsupported version: ${version}`);
            }
            const iv = packed.subarray(1, 1 + IV_LENGTH);
            const tag = packed.subarray(1 + IV_LENGTH, 1 + IV_LENGTH + TAG_LENGTH);
            const encryptedData = packed.subarray(1 + IV_LENGTH + TAG_LENGTH);
            const key = this.deriveKey(field);
            const decipher = crypto_1.default.createDecipheriv('aes-256-gcm', key, iv, {
                authTagLength: TAG_LENGTH,
            });
            decipher.setAuthTag(tag);
            const decrypted = Buffer.concat([
                decipher.update(encryptedData),
                decipher.final(),
            ]);
            return decrypted.toString('utf8');
        }
        catch (error) {
            throw new Error(`Decryption failed: ${error}`);
        }
    }
    /**
     * Create a blind index (deterministic hash) for searchable encryption.
     *
     * Uses BLAKE2b-256 with keyed hashing.
     *
     * @param plaintext - Value to hash
     * @param field - Field name for key derivation
     * @returns Hex-encoded hash (64 characters)
     */
    blindIndex(plaintext, field = 'default') {
        if (!plaintext) {
            return '';
        }
        // Normalize
        const normalized = plaintext.toLowerCase().trim();
        // Derive hash key
        const hashKey = this.deriveKey(field + ':blind_index').subarray(0, 32);
        // Node.js doesn't have native BLAKE2b, use SHA-256 HMAC as fallback
        // For full compatibility, use @noble/hashes or similar
        const hmac = crypto_1.default.createHmac('sha256', hashKey);
        hmac.update(normalized);
        return hmac.digest('hex');
    }
    /**
     * Check if value is encrypted with HouslerCrypto.
     */
    isEncrypted(value) {
        return Boolean(value && value.startsWith(ENCRYPTED_PREFIX));
    }
    /**
     * Generate a new 32-byte master key (64 hex chars).
     */
    static generateKey() {
        return crypto_1.default.randomBytes(KEY_LENGTH).toString('hex');
    }
}
exports.HouslerCrypto = HouslerCrypto;
/**
 * PII masking utilities for logging and display.
 */
exports.mask = {
    /**
     * Mask email: te***@example.com
     */
    email(email) {
        if (!email || !email.includes('@')) {
            return '***';
        }
        const [local, domain] = email.split('@');
        const maskedLocal = local.length > 2 ? local.substring(0, 2) + '***' : '***';
        return `${maskedLocal}@${domain}`;
    },
    /**
     * Mask phone: +7***4567
     */
    phone(phone) {
        if (!phone) {
            return '***';
        }
        const digits = phone.replace(/\D/g, '');
        if (digits.length < 4) {
            return '***';
        }
        const prefix = phone.startsWith('+') ? '+' : '';
        return `${prefix}${digits[0]}***${digits.slice(-4)}`;
    },
    /**
     * Mask name: Ив*** П***
     */
    name(name) {
        if (!name) {
            return '***';
        }
        return name
            .split(' ')
            .map((part) => (part.length > 2 ? part.substring(0, 2) + '***' : '***'))
            .join(' ');
    },
    /**
     * Mask INN: 77***1234
     */
    inn(inn) {
        if (!inn) {
            return '***';
        }
        const digits = inn.replace(/\D/g, '');
        if (digits.length < 6) {
            return '***';
        }
        return `${digits.substring(0, 2)}***${digits.slice(-4)}`;
    },
    /**
     * Mask card: **** **** **** 1234
     */
    card(cardNumber) {
        if (!cardNumber) {
            return '***';
        }
        const digits = cardNumber.replace(/\D/g, '');
        if (digits.length < 4) {
            return '***';
        }
        return `**** **** **** ${digits.slice(-4)}`;
    },
};
/**
 * Normalize phone number to consistent format.
 */
function normalizePhone(phone) {
    if (!phone) {
        return '';
    }
    let digits = phone.replace(/\D/g, '');
    // Convert 8 to 7 for Russian numbers
    if (digits.length === 11 && digits.startsWith('8')) {
        digits = '7' + digits.slice(1);
    }
    // Add 7 for 10-digit numbers
    if (digits.length === 10) {
        digits = '7' + digits;
    }
    return digits;
}
/**
 * Normalize email for consistent hashing.
 */
function normalizeEmail(email) {
    if (!email) {
        return '';
    }
    return email.toLowerCase().trim();
}
exports.default = HouslerCrypto;
