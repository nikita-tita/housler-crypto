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
interface HouslerCryptoOptions {
    masterKey: string;
    salt?: string;
    iterations?: number;
}
/**
 * Unified PII encryption service for Housler ecosystem.
 *
 * Uses AES-256-GCM with per-field key derivation.
 */
export declare class HouslerCrypto {
    private masterKey;
    private salt;
    private iterations;
    private keyCache;
    constructor(options: HouslerCryptoOptions);
    /**
     * Derive a field-specific key from master key using PBKDF2.
     */
    private deriveKey;
    /**
     * Encrypt data using AES-256-GCM.
     *
     * @param plaintext - Data to encrypt
     * @param field - Field name for key derivation (e.g., "email", "phone")
     * @returns Encrypted string with "hc1:" prefix
     */
    encrypt(plaintext: string, field?: string): string;
    /**
     * Decrypt data encrypted with AES-256-GCM.
     *
     * @param ciphertext - Encrypted string (with "hc1:" prefix)
     * @param field - Field name for key derivation
     * @returns Decrypted plaintext
     */
    decrypt(ciphertext: string, field?: string): string;
    /**
     * Create a blind index (deterministic hash) for searchable encryption.
     *
     * Uses BLAKE2b-256 with keyed hashing.
     *
     * @param plaintext - Value to hash
     * @param field - Field name for key derivation
     * @returns Hex-encoded hash (64 characters)
     */
    blindIndex(plaintext: string, field?: string): string;
    /**
     * Check if value is encrypted with HouslerCrypto.
     */
    isEncrypted(value: string): boolean;
    /**
     * Generate a new 32-byte master key (64 hex chars).
     */
    static generateKey(): string;
}
/**
 * PII masking utilities for logging and display.
 */
export declare const mask: {
    /**
     * Mask email: te***@example.com
     */
    email(email: string): string;
    /**
     * Mask phone: +7***4567
     */
    phone(phone: string): string;
    /**
     * Mask name: Ив*** П***
     */
    name(name: string): string;
    /**
     * Mask INN: 77***1234
     */
    inn(inn: string): string;
    /**
     * Mask card: **** **** **** 1234
     */
    card(cardNumber: string): string;
};
/**
 * Normalize phone number to consistent format.
 */
export declare function normalizePhone(phone: string): string;
/**
 * Normalize email for consistent hashing.
 */
export declare function normalizeEmail(email: string): string;
export default HouslerCrypto;
