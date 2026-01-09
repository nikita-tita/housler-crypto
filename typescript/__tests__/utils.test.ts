/**
 * Tests for utility functions: masking, normalization.
 */

import { mask, normalizePhone, normalizeEmail } from '../src/index';

describe('mask', () => {
  describe('email', () => {
    it('should mask normal email', () => {
      expect(mask.email('test@example.com')).toBe('te***@example.com');
    });

    it('should mask short local part', () => {
      expect(mask.email('ab@example.com')).toBe('***@example.com');
    });

    it('should return *** for empty', () => {
      expect(mask.email('')).toBe('***');
    });

    it('should return *** for no @ sign', () => {
      expect(mask.email('notanemail')).toBe('***');
    });

    it('should handle long local part', () => {
      expect(mask.email('verylongemail@domain.com')).toBe('ve***@domain.com');
    });
  });

  describe('phone', () => {
    it('should mask Russian phone', () => {
      expect(mask.phone('+79991234567')).toBe('+7***4567');
    });

    it('should mask phone without +', () => {
      expect(mask.phone('79991234567')).toBe('7***4567');
    });

    it('should return *** for short', () => {
      expect(mask.phone('123')).toBe('***');
    });

    it('should return *** for empty', () => {
      expect(mask.phone('')).toBe('***');
    });
  });

  describe('name', () => {
    it('should mask two-word name', () => {
      expect(mask.name('Иван Иванов')).toBe('Ив*** Ив***');
    });

    it('should mask single word', () => {
      expect(mask.name('Иван')).toBe('Ив***');
    });

    it('should mask short word', () => {
      expect(mask.name('Ян')).toBe('***');
    });

    it('should return *** for empty', () => {
      expect(mask.name('')).toBe('***');
    });
  });

  describe('inn', () => {
    it('should mask 10-digit INN', () => {
      expect(mask.inn('7707083893')).toBe('77***3893');
    });

    it('should mask 12-digit INN', () => {
      expect(mask.inn('772012345678')).toBe('77***5678');
    });

    it('should return *** for short', () => {
      expect(mask.inn('12345')).toBe('***');
    });

    it('should return *** for empty', () => {
      expect(mask.inn('')).toBe('***');
    });
  });

  describe('card', () => {
    it('should mask card number', () => {
      expect(mask.card('4111111111111111')).toBe('**** **** **** 1111');
    });

    it('should handle formatted card', () => {
      expect(mask.card('4111 1111 1111 1111')).toBe('**** **** **** 1111');
    });

    it('should return *** for short', () => {
      expect(mask.card('123')).toBe('***');
    });

    it('should return *** for empty', () => {
      expect(mask.card('')).toBe('***');
    });
  });
});

describe('normalizePhone', () => {
  it('should normalize formatted phone', () => {
    expect(normalizePhone('+7 (999) 123-45-67')).toBe('79991234567');
  });

  it('should convert 8 prefix to 7', () => {
    expect(normalizePhone('8-999-123-45-67')).toBe('79991234567');
  });

  it('should add 7 prefix to 10 digits', () => {
    expect(normalizePhone('9991234567')).toBe('79991234567');
  });

  it('should keep already normalized', () => {
    expect(normalizePhone('79991234567')).toBe('79991234567');
  });

  it('should return empty for empty', () => {
    expect(normalizePhone('')).toBe('');
  });
});

describe('normalizeEmail', () => {
  it('should lowercase', () => {
    expect(normalizeEmail('Test@Example.COM')).toBe('test@example.com');
  });

  it('should strip whitespace', () => {
    expect(normalizeEmail('  test@example.com  ')).toBe('test@example.com');
  });

  it('should return empty for empty', () => {
    expect(normalizeEmail('')).toBe('');
  });
});
